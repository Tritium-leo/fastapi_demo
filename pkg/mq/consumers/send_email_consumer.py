import pika


def callback(ch: pika.adapters.blocking_connection.BlockingChannel, method, properties, body):
    print("send_email_consumer reveive msg!!!!!")
    print("Consume", ch, method, properties, body)
    print(body)
    try:
        raise Exception("123")
    except:
        ch.basic_recover(True)
    else:
        # ack
        ch.basic_ack(delivery_tag=method.delivery_tag)
