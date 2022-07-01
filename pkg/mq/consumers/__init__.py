from pkg.mq.rabbitmq import rabbitmq_cli
from . import send_email_consumer
import threading


# init
def init():
    rabbitmq_cli.new_consumer("user-service-consumer", send_email_consumer.callback)



init()
