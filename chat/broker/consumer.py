import pika
import time
from ast import literal_eval
from flask_socketio import SocketIO, emit


socketio = SocketIO( message_queue='main_queue')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# channel.queue_declare(queue='hello')
channel.queue_declare(queue='main_queue', durable=True)


def get_data(body):
    return literal_eval(body.decode("UTF-8"))


def should_act(body):
    data = get_data(body)
    if 'message' in data:
        return data['message'].startswith('/')
    else:
        return False


def reply(data):
    data = get_data(data)
    socketio.emit('bot_reply', {
        'username': 'Bot_Master',
        'room': data['room'],
        'message': 'This is bot master'
    })


def callback(ch, method, properties, body):
    print(" [x] Received %r " % body)
    # time.sleep(body.count(b'.'))
    bot = should_act(body)
    reply(body)
    print(f'[x] Done should_act {bot}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='main_queue', on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
