from chat.broker.consumer import channel, callback


if __name__ == '__main__':
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='main_queue', on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()