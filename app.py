from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread
import os 

app = Flask(__name__)
socketio = SocketIO(app)

users = {}

def handle_connect(sid):
    users[sid] = Thread(target=user_thread, args=(sid,))
    users[sid].start()

def user_thread(sid):
    while True:
        message = socketio.wait(sid)
        if message is None:
            break
        else:
            emit('broadcast', message, broadcast=True, include_self=False)

@app.route('/')
def index():
    return render_template('client.html')

@socketio.on('connect')
def handle_connect_event():
    sid = socketio.eio_sid_map[request.namespace][request.sid]
    thread = Thread(target=handle_connect, args=(sid,))
    thread.start()

@socketio.on('disconnect')
def handle_disconnect_event():
    sid = socketio.eio_sid_map[request.namespace][request.sid]
    if sid in users:
        del users[sid]

@socketio.on('message')
def handle_message(message):
    emit('broadcast', message, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.getenv("PORT")), allow_unsafe_werkzeug=True)
