import threading
import socketio

def mail():
    sio = socketio.Client()

    @sio.event
    def connect():
        nomeusuario = input('Usuário> ')
        print('\nConectado')

    @sio.event
    def broadcast(message):
        print(message + '\n')

    sio.connect('http://localhost:5000', namespaces=['/'])

    t = threading.Thread(target=sendMessages, args=[sio])
    t.start()

def sendMessages(sio):
    while True:
        try:
            mensagem = input('\n')
            sio.emit('message', mensagem, namespace='/')
        except:
            return
        
def receiveMessages(cliente):
    while True:
        try:
            mensagem = cliente.recv(2048).decode('utf-8')
            socketio.emit('message', {'data': mensagem})  # Envia a mensagem para o servidor
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> para continuar...')
            cliente.close()
            break
        
mail()
