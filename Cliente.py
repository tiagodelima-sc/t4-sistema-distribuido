import threading
import socket

from datetime import datetime, timedelta
from random import randint


def hora_aleatoria():
    segundos_random = randint(60, 10000)
    if segundos_random % 2 == 0:
        return datetime.now() + timedelta(seconds=segundos_random)
    else:
        return datetime.now() - timedelta(seconds=segundos_random)

data_atual = hora_aleatoria().replace(microsecond=0)

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 8000))

    thread_enviar = threading.Thread(target=enviarMensagem, args=[cliente, ])
    thread_receber = threading.Thread(target=receberMensagem, args=[cliente, ])

    thread_enviar.start()
    thread_receber.start()


def receberMensagem(cliente):
    while True:

        msg = cliente.recv(2048).decode('utf-8')
        if 'Digite' in msg:
            print("=/="*15)
            print(f'\nServidor: {msg}')
            global data_atual
            print(f'Cliente: Minha hora atual é: {data_atual}')
            enviarMensagem(cliente, str(data_atual))
        else:
            print(f'Servidor: Eu vou atualizar seu horário para {msg}')
            data_atual = datetime.strptime(msg, '%Y-%m-%d %H:%M:%S')
            print(f'Cliente: Minha hora atualizada é: {data_atual}\n')
            print("=/="*15)


def enviarMensagem(cliente, msg=None):
    if msg:
        cliente.send(msg.encode('utf-8'))
    else:
        print("Aguardando Sincronização!")
    return


main()
