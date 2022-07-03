import threading
import time
from typing import *

import pika
from pika.exchange_type import ExchangeType
from pydantic import BaseModel

from config.init import config
from pkg.utils.threader_helper import stop_thread

local = threading.local()


class MQConsumerThread(threading.Thread):
    def __init__(self, threadId, name, delay):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.delay = delay

    def run(self):
        while True:
            self.delay.start()
            time.sleep(10)
        logger.info("exit xiancheng")


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

    def __init__(self, conn: pika.BlockingConnection, config_name: str,
                 ch: pika.adapters.blocking_connection.BlockingChannel):
        self._conn_ = conn
        self.config_name = config_name
        self.ch = ch
        if config_name not in config:
            raise Exception(f"Producer No Config:{config_name}")
        self.conf = RabbitMQProducerConfig(**config[config_name])
        if self.conf.exchangeName != "" and self.conf.kind == "":
            raise Exception(f"load amqp producer {config_name} configuration fail, kind is empty")

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
        if self._conn_.is_open:
            self._conn_.close()


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
    _conn_: pika.BlockingConnection
    config_name: str
    ch: pika.adapters.blocking_connection.BlockingChannel
    conf: RabbitMQConsumerConfig

    def __init__(self, conn: pika.BlockingConnection, ch: pika.adapters.blocking_connection.BlockingChannel,
                 config_name: str, callback):
        self._conn_ = conn
        self.ch = ch
        self.config_name = config_name
        self.callback = callback
        if config_name not in config:
            raise Exception(f"Consumer No Config:{config_name}")
        self.conf = RabbitMQConsumerConfig(**config[config_name])

    def start(self):
        try:
            self.ch.start_consuming()
        except KeyboardInterrupt:
            self.ch.stop_consuming()

    def close(self, consumer_tag: str):
        if self.ch.is_open:
            # self.ch.stop_consuming(consumer_tag=consumer_tag)
            self.ch.close() if self.ch.is_open else None
        if self._conn_.is_open:
            self._conn_.close()


class RabbitMQClient:
    conn: pika.BlockingConnection
    producers: Dict[str, RabbitMqProducer]
    consumers: Dict[str, RabbitMQConsumer]
    conf: RabbitMQConfig
    _treads = []

    def __init__(self, conf: RabbitMQConfig):
        self.conf = conf
        self.producers = {}
        self.consumers = {}

    def get_conn(self):
        conf = self.conf
        user_info = pika.PlainCredentials(username=conf.username, password=conf.password)
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=conf.host, port=conf.port, virtual_host="/", credentials=user_info,
                                      heartbeat=0)
        )
        return conn

    def new_producer(self, config_name: str):
        if config_name in self.producers:
            raise Exception(f"producer quene already exists: name:{config_name}")
        if config_name not in config:
            raise Exception(f"config doesn't exist this producer:{config_name},please check")
        conf = RabbitMQProducerConfig(**config[config_name])
        conn = self.get_conn()
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
        self.producers[config_name] = RabbitMqProducer(conn, config_name, ch)

    def publish_msg(self, producer: str, headers, body):
        if producer not in self.producers:
            raise Exception(f"This MQ Product Didn't registry,{producer}")
        self.producers[producer].publish(headers, body)

    def new_consumer(self, config_name: str, callback):
        if config_name in self.consumers:
            raise Exception(f"Consumer quene already exists: name:{config_name}")
        if config_name not in config:
            raise Exception(f"This Consumer Quene Config didn't exist :{config_name}")
        conn = self.get_conn()
        conf = RabbitMQConsumerConfig(**config[config_name])
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

        self.consumers[consumer_tag] = RabbitMQConsumer(conn, ch, config_name, callback)

    def close(self):
        # close thread
        for t in self._treads:
            stop_thread(t)
        for consumer_tag, v in self.consumers.items():
            v.close(consumer_tag)
        for _, v in self.producers.items():
            v.close()

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
