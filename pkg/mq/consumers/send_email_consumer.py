import pika


def callback(ch: pika.adapters.blocking_connection.BlockingChannel, method, properties, body):
    try:
        logger.info(body)
        # raise Exception("123")
    except:
        ch.basic_recover(True)
    else:
        # ack
        ch.basic_ack(delivery_tag=method.delivery_tag)
