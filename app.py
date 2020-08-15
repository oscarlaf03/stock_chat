from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_socketio import SocketIO, join_room, leave_room
from pymongo.errors import DuplicateKeyError

from db import (add_room_members, get_room, get_room_members,
                get_rooms_for_user, get_user, is_room_admin, is_room_member,
                remove_room_members, save_room, save_user, update_room, save_message, get_messages)
from models.user import User

app = Flask(__name__)
app.secret_key = 'my_secret_key'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def home():
    rooms = []
    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)
    return render_template('index.html', rooms=rooms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)
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


@app.route('/create-room/', methods=['GET', 'POST'])
@login_required
def create_room():
    message = ''
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        usernames = [username.strip()
                     for username in request.form.get('members').split(',')]
        if len(room_name) and len(usernames):
            room_id = save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            add_room_members(room_id, room_name, usernames,
                             current_user.username)
        else:
            message = 'Failed to create room'

    return render_template('create_room.html', message=message)

@app.route('/rooms/<room_id>/edit', methods=['GET','POST'])
@login_required
def edit_room(room_id):
    room = get_room(room_id)
    if room and is_room_admin(room_id, current_user.username):
        room_members = [ member['_id']['username'] for member in get_room_members(room_id) ]
        room_members_str = ",".join(room_members)
        message =''
        if request.method == 'POST':
            room_name = request.form.get('room_name')
            room['name'] = room_name
            update_room(room_id, room_name)
            # room = get_room(room_id)
            request_members = [ username.strip() for username in request.form.get('members').split(',') ]
            members_to_add =  list(set(request_members) -  set(room_members))
            members_to_remove =  list(set(room_members) - set(request_members))
            if len(members_to_add):
                add_room_members(room_id,room_name, members_to_add, current_user.username)

            if len(members_to_remove):
                remove_room_members(room_id, members_to_remove)

            room_members_str = ",".join(request_members)
            message = 'Room edited succesfully'

        return render_template('edit_room.html', room=room, room_members_str=room_members_str, message=message)
    else:
        return "Room not found", 404



@app.route('/rooms/<room_id>/')
def view_room(room_id):
    # username = request.args.get('username')
    # room = request.args.get('room')
    username = current_user.username
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        room_members = get_room_members(room_id)
        messages = get_messages(room_id)
        return render_template('view_room.html', username=username, room=room, room_members=room_members, messages=messages)
    else:
        return "Room not found", 404

@socketio.on('send_message')
def handle_send_message(data):
    app.logger.info(
        f'{data["username"]} has sent a message to the room: {data["room"]} : {data["message"]}')
    save_message(data['room'],data['message'],data['username'])
    data['created_at'] = datetime.now().strftime('%d %b, %H:%M')
    socketio.emit('received_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info(f'{data["username"]} has joined the {data["room"]} room')
    join_room(data['room'])
    socketio.emit('join_room_notice', data)


@socketio.on('leave_room')
def handle_left_room_event(data):
    app.logger.info(f'{data["username"]} has left the {data["room"]} room')
    leave_room(data['room'])
    socketio.emit('left_room_notice', data)


@login_manager.user_loader
def load_user(username):
    return get_user(username)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            save_user(username, email, password)
        except DuplicateKeyError:
            message = 'Sorry, that user name is already taken'
    return render_template('signup.html', message=message)


if __name__ == '__main__':
    socketio.run(app, debug=True)
