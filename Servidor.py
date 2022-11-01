import threading
import socket
import time

from datetime import datetime, timedelta

clientes = []
clientes_tempo = {}
data_atual = datetime.now().replace(microsecond=0)


def main():

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 8000))
    servidor.listen()

    thread_mensagem_sincronizada = threading.Thread(target=loop_mensagem, args=[])
    thread_mensagem_sincronizada.start()

    while True:
        cliente, addr = servidor.accept()
        clientes.append(cliente)
        thread = threading.Thread(target=tratamento_Mensagens, args=[cliente,])
        thread.start()


def loop_mensagem():
    while True:
        opcao = int(input("1) Para sincronizar a hora.\n2) Para sair.\n"))
        if opcao == 1:
            for cliente in clientes:
                transmissao('Digite sua hora', cliente)
                time.sleep(1)
        else:
            break


def tratamento_Mensagens(cliente):
    while True:
         msg = cliente.recv(2048)
         mensagem_processada(cliente, msg.decode("utf-8"))


def sincronizando_Berkley():
    diferenca_tempo = []
    diferenca_clientes = {}
    global data_atual
    print("=/="*15)
    print("=/=/=/=/=/=/= NOVA SINCRONIZAÇÃO =/=/=/=/=/=/=")
    print("=/="*15)
    print(f"\nHora do Servidor: {data_atual}")
    contador = 0

    for cliente, cliente_tempo in clientes_tempo.items():
        contador += 1
        dif_tempo = cliente_tempo - data_atual
        diferenca_tempo.append(float(dif_tempo.total_seconds()))
        diferenca_clientes.update({cliente: dif_tempo.total_seconds()})
        print(f"Hora Cliente {contador}: {cliente_tempo}. Diferença de Tempo: {dif_tempo.total_seconds()/60} minutos")

    print("\n", "=/="*15)
    print(f"Número de Usuários Ativos: {contador}")
    tempo_medio = sum(diferenca_tempo) / (len(clientes) + 1)
    print(f"Tempo Médio: {tempo_medio/60} minutos")
    print("=/="*15, "\n")

    data_atual = (data_atual + timedelta(seconds=tempo_medio)).replace(microsecond=0)
    print(f"Hora do Servidor Atualizada: {data_atual}\n")

    contador_2 = 0

    for cliente, cliente_tempo in clientes_tempo.items():
        contador_2 += 1
        sincronizar_tempo = (cliente_tempo + timedelta(seconds=(diferenca_clientes[cliente] * - 1) + tempo_medio)).replace(microsecond=0)
        print(f"Cliente {contador_2} tempo atualizado é {sincronizar_tempo}")
        transmissao(str(sincronizar_tempo), cliente)

    print("\n")

def mensagem_processada(cliente, msg):
    clientes_tempo.update({cliente: datetime.strptime(msg, '%Y-%m-%d %H:%M:%S')})
    if len(clientes) == len(clientes_tempo):
        sincronizando_Berkley()
        clientes_tempo.clear()


def transmissao(msg, cliente):
    for clienteItem in clientes:
        if clienteItem == cliente:
            clienteItem.send(msg.encode('utf-8'))
            break

main()
