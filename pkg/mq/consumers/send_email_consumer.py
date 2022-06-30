def callback(ch, method, properties, body):
    print("Consume", ch, method, properties, body)
    # ack
    ch.basic_ack(delivery_tag=method.delivery_tag)

