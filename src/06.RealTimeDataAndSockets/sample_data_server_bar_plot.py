#
# Python Script to Serve
# Random Bars Data
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#

# Importando bibliotecas necessárias
import zmq  # Para comunicação via sockets
import math  # Para operações matemáticas
import time  # Para controle de tempo
import random  # Para geração de números aleatórios

# Configurando o socket ZMQ para publicação de dados
context = zmq.Context()
socket = context.socket(zmq.PUB)  # Socket do tipo Publisher
socket.bind('tcp://0.0.0.0:5556')  # Vinculando à porta 5556

# Loop infinito para gerar e enviar dados
while True:
    # Gerando 8 valores aleatórios entre 0 e 100
    bars = [random.random() * 100 for _ in range(8)]
    
    # Convertendo os valores em string formatada com 3 casas decimais
    msg = ' '.join([f'{bar:.3f}' for bar in bars])
    
    # Imprimindo a mensagem no console
    print(msg)
    
    # Enviando a mensagem através do socket
    socket.send_string(msg)
    
    # Aguardando um tempo aleatório entre 0 e 2 segundos
    time.sleep(random.random() * 2)