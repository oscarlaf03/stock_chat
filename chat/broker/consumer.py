import pika
import time
from ast import literal_eval
from flask_socketio import SocketIO
from datetime import datetime
from bot.bot import Bot

socketio = SocketIO(message_queue='redis://localhost:6379')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='main_queue', durable=True)

def get_data(body):
    return literal_eval(body.decode("UTF-8"))

def bot_signal(message):
    return message.startswith('/')

def reply(room,message,msg_from):
    socketio.emit('received_message', {
        'username': msg_from,
        'room': room,
        'message': message,
        'created_at': datetime.now().strftime('%d %b, %H:%M:%S')
    }, room=room)

# def see_bot(data):
#     if bot_signal(data['message']):
#         bot = Bot(data['message'], data['username'])
#         print('*****BOT MESSAGE******')
#         print(bot.reply_message())
#         print('*****END OF BOT MESSAGE******')

def run_data(data):
    if bot_signal(data['message']):
        bot = Bot(data['message'],data['username'])
        message = bot.reply_message()
        reply(data['room'], message, bot.bot_name)

def callback(ch, method, properties, body):
    print(" [x] Received %r " % body)
    data = get_data(body)
    run_data(data)
    # see_bot(data)
    print(f'[x] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)
