import eventlet
eventlet.monkey_patch()


from chat.app import app, socketio



if __name__ == '__main__':
    socketio.run(app, debug=True)