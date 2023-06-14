from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os 

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('client.html')

@socketio.on('connect')
def handle_connect_event():
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect_event():
    emit('disconnected', {'data': 'Disconnected'})

@socketio.on('message')
def handle_message(message):
    emit('broadcast', message, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.getenv("PORT")), allow_unsafe_werkzeug=True)
