# Importa os módulos necessários
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread
import os

# Inicializa o aplicativo Flask
app = Flask(__name__)
# Inicializa o objeto SocketIO usando o aplicativo Flask
socketio = SocketIO(app)

# Dicionário para armazenar os usuários conectados
users = {}

# Função para lidar com a conexão de um usuário
def handle_connect(sid):
    # Cria uma nova thread para lidar com o usuário
    users[sid] = Thread(target=user_thread, args=(sid,))
    # Inicia a nova thread
    users[sid].start()

# Função executada em uma thread separada para cada usuário conectado
def user_thread(sid):
    while True:
        # Aguarda por mensagens do cliente
        message = socketio.wait(sid)
        # Verifica se a mensagem é nula (cliente desconectado)
        if message is None:
            break
        else:
            # Transmite a mensagem para todos os clientes conectados (exceto o emissor original)
            emit('broadcast', message, broadcast=True, include_self=False)

# Rota principal do aplicativo Flask
@app.route('/')
def index():
    return render_template('client.html')

# Evento de conexão do SocketIO
@socketio.on('connect')
def handle_connect_event():
    emit('connected', {'data': 'Connected'})

# Evento de desconexão do SocketIO
@socketio.on('disconnect')
def handle_disconnect_event():
    emit('disconnected', {'data': 'Disconnected'})

# Evento de mensagem do SocketIO
@socketio.on('message')
def handle_message(message):
    emit('broadcast', message, broadcast=True, include_self=False)

# Verifica se o arquivo Python está sendo executado diretamente
if __name__ == '__main__':
    # Executa o servidor Flask com suporte a SocketIO
    socketio.run(app, host='0.0.0.0', port=int(os.getenv("PORT")), allow_unsafe_werkzeug=True)
