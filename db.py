from pymongo import MongoClient
from werkzeug.security import  generate_password_hash
from models.user import User
from datetime import datetime

client = MongoClient('mongodb+srv://admin:admin@cluster0.dzbqz.gcp.mongodb.net/ChatDB?retryWrites=true&w=majority')

chat_db = client.get_database('ChatDB')
users_collection =  chat_db.get_collection('users')
rooms_collections = chat_db.get_collection('room_members')
room_members_collection = chat_db.get_collection('room_members')


def save_user(username, email, password):
    password_hash = generate_password_hash(password)
    users_collection.insert_one({'_id':username, 'email': email, 'password':password_hash})

def get_user(username):
    user_data = users_collection.find_one({'_id': username })
    return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None

def save_room(room_name,created_by, usernames):
    room_id =  rooms_collections.insert_one({'room_name':room_name, 'created_by':created_by, 'created_at': datetime.now()}).inserted_id
    add_room_member(room_id,room_name,created_by,created_by, is_admin=True)
    return room_id


def add_room_member(room_id, room_name, username,added_by, is_admin=False)
    pass