import multiprocessing
import threading
from typing import *

import loguru
import pika
from pika.exchange_type import ExchangeType
from pydantic import BaseModel

from config import model as config_model
from pkg.utils.threader_helper import stop_thread

local = threading.local()


class MQConsumerThread(threading.Thread):
    def __init__(self, threadId, name, delay):
        threading.Thread.__init__(self, name=name, daemon=True)
        self.threadId = threadId
        self.delay = delay

    def run(self):
        # while True:
        self.delay.start()


class MQConsumerProcess(multiprocessing.Process):
    def __init__(self, processId, name, delay):
        multiprocessing.Process.__init__(self, name=name, daemon=True)
        self.delay = delay

    def run(self):
        # while True:
        self.delay.start()


class RabbitMQConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str


class RabbitMQProducerConfig(BaseModel):
    queueName: Union[str, None]
    exchangeName: str
    durable: bool
    kind: str
    exclusive: bool = False
    autoDelete: bool = False


class RabbitMqProducer:
    _conn_: pika.BlockingConnection
    config_name: str
    ch: pika.adapters.blocking_connection.BlockingChannel
    conf: RabbitMQProducerConfig

    def __init__(self,
                 ch: pika.adapters.blocking_connection.BlockingChannel,
                 config_name: str,
                 conf: RabbitMQProducerConfig,
                 ):
        self.config_name = config_name
        self.ch = ch
        self.conf = conf

    def publish(self, headers: Dict[str, Any], body: str) -> bool:
        # TODO IF FAILED , RETRY
        if self.conf.queueName is not None:
            self.ch.basic_publish(
                routing_key=self.conf.queueName,
                body=body,
            )
        else:
            self.ch.basic_publish(
                routing_key="",
                exchange=self.conf.exchangeName,
                body=body,
                properties=pika.BasicProperties(delivery_mode=2),
            )
        return

    def close(self):
        if self.ch.is_open:
            self.ch.close()


class RabbitMQConsumerConfig(BaseModel):
    exchangeName: str
    exchangeDurable: bool = False
    queueName: str
    queueDurable: bool = False
    kind: str
    parallel: int
    autoAck: bool = True
    autoDelete: bool = False
    exclusive: bool = False
    prefetch: int = 1


class RabbitMQConsumer:
    config_name: str
    ch: pika.adapters.blocking_connection.BlockingChannel
    conf: RabbitMQConsumerConfig

    def __init__(self, ch: pika.adapters.blocking_connection.BlockingChannel,
                 config_name: str, conf):
        self.ch = ch
        self.config_name = config_name
        self.conf = conf

    def start(self):
        self.ch.start_consuming()

    def close(self):
        if self.ch.is_open:
            self.ch.close()


class RabbitMQClient:
    producer_conn: pika.BlockingConnection
    consumer_conn: pika.BlockingConnection
    producers: Dict[str, RabbitMqProducer]
    consumers: Dict[str, RabbitMQConsumer]
    conf: RabbitMQConfig
    _treads: List[MQConsumerThread] = []
    _mutil_process: List[MQConsumerProcess] = []

    def __init__(self, conf: RabbitMQConfig):
        self.conf = conf
        self.producers = {}
        self.consumers = {}
        self.producer_conn = self.get_conn()
        self.consumer_conn = self.get_conn()

    def get_conn(self):
        conf = self.conf
        user_info = pika.PlainCredentials(username=conf.username, password=conf.password)
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=conf.host, port=conf.port, virtual_host="/", credentials=user_info,
                                      retry_delay=3,
                                      heartbeat=0)
        )
        return conn

    def new_producer(self, config_name: str):
        if config_name in self.producers:
            raise Exception(f"producer quene already exists: name:{config_name}")
        if config_name not in config_model.config.data:
            raise Exception(f"config doesn't exist this producer:{config_name},please check")

        conf = config_model.config.struct_map(config_name, RabbitMQProducerConfig)
        if conf.exchangeName != "" and conf.kind == "":
            raise Exception(f"load amqp producer {config_name} configuration fail, kind is empty")

        conn = self.producer_conn
        ch = conn.channel()
        if conf.queueName is not None and conf.queueName != "":
            ch.queue_declare(queue=conf.queueName,
                             durable=conf.durable,
                             auto_delete=conf.autoDelete,
                             exclusive=conf.exclusive)
        elif conf.exchangeName is not None and conf.exchangeName != "":
            if conf.kind == "" or conf.kind is None:
                raise Exception("exchange kind is NOne")
            elif conf.kind in ExchangeType._value2member_map_:
                exchange = ExchangeType(conf.kind)
            else:
                raise Exception(f"Undefined RabbitMQ Producer kind :{conf.kind}")
            ch.exchange_declare(
                exchange=conf.exchangeName,
                durable=conf.durable,
                auto_delete=conf.autoDelete,
                exchange_type=exchange)
        else:
            raise Exception(f"Rabbitmq quene name or exchange name is not config。{config_name}")
        self.producers[config_name] = RabbitMqProducer(ch, config_name, conf)

    def publish_msg(self, producer: str, headers, body):
        if producer not in self.producers:
            raise Exception(f"This MQ Product Didn't registry,{producer}")
        self.producers[producer].publish(headers, body)

    def new_consumer(self, config_name: str, callback, thread_num: int = 1):
        if config_name in self.consumers:
            raise Exception(f"Consumer quene already exists: name:{config_name}")
        if config_name not in config_model.config.data:
            raise Exception(f"This Consumer Quene Config didn't exist :{config_name}")

        conn = self.consumer_conn

        conf = config_model.config.struct_map(config_name, RabbitMQConsumerConfig)

        ch = conn.channel()
        ch.basic_qos(prefetch_count=conf.prefetch)
        if conf.exchangeName != "" and conf.exchangeName is not None:
            if conf.kind == "" or conf.kind is None:
                raise Exception("exchange kind is NOne")
            elif conf.kind in ExchangeType._value2member_map_:
                exchange = ExchangeType(conf.kind)
            else:
                raise Exception(f"Undefined RabbitMQ Producer kind :{conf.kind}")

            ch.exchange_declare(exchange=conf.exchangeName,
                                exchange_type=exchange,
                                durable=conf.queueDurable,
                                auto_delete=conf.autoDelete)
            ch.queue_declare(queue=conf.queueName,
                             durable=conf.queueDurable,
                             auto_delete=conf.autoDelete,
                             exclusive=conf.exclusive)
            ch.queue_bind(
                queue=conf.queueName,
                exchange=conf.exchangeName,
                routing_key=conf.queueName
            )


        elif conf.queueName != "" and conf.queueName is not None:

            ch.queue_declare(queue=conf.queueName,
                             durable=conf.queueDurable,
                             auto_delete=conf.autoDelete,
                             exclusive=conf.exclusive)

        consumer_tag = ch.basic_consume(queue=conf.queueName,
                                        on_message_callback=callback,
                                        auto_ack=conf.autoAck,
                                        arguments={}
                                        )

        self.consumers[consumer_tag] = RabbitMQConsumer(ch, config_name, conf)

    def close(self):
        # close thread
        try:
            for t in self._treads:
                stop_thread(t)
            for p in self._mutil_process:
                p.kill()
            # close consumer channel
            for consumer_tag, v in self.consumers.items():
                v.close()
            # close producer channel
            for _, v in self.producers.items():
                v.close()
            # close conn
            self.consumer_conn.close() if self.consumer_conn.is_open else None
            self.producer_conn.close() if self.producer_conn.is_open else None
        except Exception as e:
            loguru.logger.error(f"RabbitMq Closed Failed,ERR:{e}")
        else:
            loguru.logger.info("RabbitMQ Closed Successfully")

    def start(self):
        idx = 0
        for consumer_tag, v in self.consumers.items():
            t1 = MQConsumerThread(idx, f"MQConsumerThread_{idx}", v)
            self._treads.append(t1)
            t1.start()
            idx += 1


client = None


def init_rabbitmq(conf: RabbitMQConfig):
    global client
    if client is None:
        client = RabbitMQClient(conf)
