import pika
from pika.exchange_type import ExchangeType
from config.init import config
from pydantic import BaseModel
from typing import *


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

    def __int__(self, conn: pika.BlockingConnection, config_name: str,
                ch: pika.adapters.blocking_connection.BlockingChannel):
        self._conn_ = conn
        self.config_name = config_name
        self.ch = ch
        if config_name not in config:
            raise Exception(f"Consumer No Config:{config_name}")
        self.conf = RabbitMQProducerConfig(**config[config_name])
        if self.conf.exchangeName != "" and self.conf.kind == "":
            raise Exception(f"load amqp producer {config_name} configuration fail, kind is empty")

    def publish(self, body: str) -> bool:
        # TODO IF FAILED , RETRY
        self.ch.basic_publish(exchange=self.conf.exchangeName,
                              routing_key=self.conf.queueName,
                              body=body,
                              properties=pika.BasicProperties(delivery_mode=2),
                              )
        return

    def close(self):
        self.ch.Close()


class RabbitMQConsumerConfig(BaseModel):
    exchangeName: str
    exchangeDurable: bool = False
    queueName: str
    queueDurable: bool = False
    kind: str
    parallel: int
    autoAck: bool = True
    prefetch: int = 1


class RabbitMQConsumer:
    _conn_: pika.BlockingConnection
    config_name: str
    ch: pika.adapters.blocking_connection.BlockingChannel
    conf: RabbitMQConsumerConfig

    def __int__(self, conn: pika.BlockingConnection, config_name: str, callback):
        self._conn_ = conn
        self.config_name = config_name
        self.callback = callback
        if config_name not in config:
            raise Exception(f"Consumer No Config:{config_name}")
        self.conf = RabbitMQConsumerConfig(**config[config_name])

    def start(self):
        self.ch = self._conn_.channel()
        self.ch.basic_qos(prefetch_count=self.conf.prefetch)

        self.ch.exchange_declare(exchange=self.conf.exchangeName, exchange_type=self.conf.kind,
                                 durable=self.conf.queueDurable)

        # self.ch.queue_declare(queue=self.conf.queueName, durable=self.conf.queueDurable)
        self.ch.basic_consumer(queue=self.conf.queueName,
                               auto_ack=self.conf.autoAck,
                               on_message_callback=self.callback,
                               arguments={})

    def close(self):
        self.ch.close()


class RabbitMQClient:
    conn: pika.BlockingConnection
    producers: Dict[str, RabbitMqProducer]
    consumers: Dict[str, RabbitMQConsumer]

    def __init__(self, conf: RabbitMQConfig):
        user_info = pika.PlainCredentials(username=conf.username, password=conf.password)
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=conf.host, port=conf.port, virtual_host="/", credentials=user_info)
        )

    def new_producer(self, config_name: str):
        if config_name in self.producers:
            raise Exception(f"producer quene already exists: name:{config_name}")
        ch = self._conn_.channel()
        if self.conf.queueName is None:
            consumer_conf = config.get(self.config_name.replace("producer", "consumer"))
            self.conf.queueName = consumer_conf.get("queueName")
        if self.conf.queueName is not None:
            ch.queue_declare(queue=self.conf.queueName, durable=self.conf.durable, exclusive=self.conf.exclusive)
        else:
            if self.conf.kind == "" or self.conf.kind is None:
                raise Exception("exchange kind is NOne")
            elif self.conf.kind == ExchangeType.direct:
                exchange = ExchangeType.direct
            elif self.conf.kind == ExchangeType.topic:
                exchange = ExchangeType.topic
            elif self.conf.kind == ExchangeType.fanout:
                exchange = ExchangeType.fanout
            elif self.conf.kind == ExchangeType.headers:
                exchange = ExchangeType.headers
            else:
                raise Exception(f"Undefined RabbitMQ Producer kind :{self.conf.kind}")
            ch.exchange_declare(exchange=self.conf.exchangeName,
                                exchange_type=ExchangeType(exchange),
                                auto_delete=self.conf.autoDelete)

        self.producers[config_name] = RabbitMqProducer(self.conn, config_name, ch)

    def new_consumer(self, config_name: str, callback):
        if config_name in self.consumers:
            raise Exception(f"Consumerr quene already exists: name:{config_name}")

        self.consumers[config_name] = RabbitMQConsumer(self.conn, config_name, callback)

    def close(self):
        for _, v in self.producers.items():
            v.close()
        for _, v in self.consumers.items():
            v.close()
        self.conn.close()

    def start(self):
        for _, v in self.consumers.items():
            v.start()


# callback
# def callback(ch, method, properties, body):
#     print("Consumer", ch, method, properties, body)

rc = RabbitMQConfig(**config["rabbitmq"])
rabbitmq_cli = RabbitMQClient(rc)
