from pkg.mq import rabbitmq
from . import send_email_consumer
import threading


# init
def init():
    rabbitmq.client.new_consumer("user-service-consumer", send_email_consumer.callback)

