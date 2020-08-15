from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, login_required
from flask_socketio import SocketIO, join_room

from db import get_user
from models.user import User

app = Flask(__name__)
app.secret_key = 'my_secret_key'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username )
        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = 'Bad login request'

    return render_template('login.html', message=message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))

@socketio.on('send_message')
def handle_send_message(data):
    app.logger.info(f'{data["username"]} has seen a message to the room: {data["room"]} : {data["message"]}')
    socketio.emit('received_message',data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info(f'{data["username"]} has joined the {data["room"]} room')
    join_room(data['room'])
    socketio.emit('join_room_notice', data)


@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == '__main__':
    socketio.run(app, debug=True)