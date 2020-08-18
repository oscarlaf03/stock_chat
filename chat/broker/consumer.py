import pika
import time
from ast import literal_eval
from flask_socketio import SocketIO
import requests
from datetime import datetime
#from chat.app import socketio

socketio = SocketIO(message_queue='redis://localhost:6379')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='main_queue', durable=True)

def get_data(body):
    return literal_eval(body.decode("UTF-8"))

def bot_signal(message):
    return message.startswith('/')

def valid_command(message):
    return message.startswith('/stock=')

def get_stock_code(message):
    return message.split('=')[1].strip()

def csv_to_dict(csv, delimeter=','):
    csv = csv.split()
    keys = csv[0].split(delimeter)
    return {k: v for k, v in zip(keys, csv[1].split(delimeter))}

def get_stock_data(stock_code):
    url = f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcv&h&e=csv'
    r = requests.get(url)
    if r.status_code == 200:
        data = csv_to_dict(r.text)
        data['got_response'] = True
        return data
    else:
        return {'got_response':False}

def reply(room,message):
    socketio.emit('received_message', {
        'username': 'Bot_Master',
        'room': room,
        'message': message,
        'created_at': datetime.now().strftime('%d %b, %H:%M:%S')
    }, room=room)


def reply_valid_message(username,room,stock_data):
    if stock_data['got_response']:
        got_reponse_message = f'Hi {username}, {stock_data["Symbol"]} Open price is {stock_data["Open"]} per share, have a nice day'
        reply(room,got_reponse_message)
    else:
        system_issues_message = f'Sorry {username}, We had some issues contacting the stock market, please try again later'
        reply(room, system_issues_message)

def interpret_data(data):
    if bot_signal(data['message']):
        if valid_command(data['message']):
            stock_code = get_stock_code(data['message'])
            stock_data = get_stock_data(stock_code)
            reply_valid_message(data['username'], data['room'], stock_data)
        else:
            invalid_command_message = f'Sorry {data["username"]} I cannot understand: "{data["message"]}", but I can understand  a stock symbol preceded by: "/stock=" '
            reply(data['room'], invalid_command_message)


def callback(ch, method, properties, body):
    print(" [x] Received %r " % body)
    # time.sleep(body.count(b'.'))
    data = get_data(body)
    interpret_data(data)
    print(f'[x] Done should_act')
    ch.basic_ack(delivery_tag=method.delivery_tag)
