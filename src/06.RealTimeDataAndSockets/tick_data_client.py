#
# Python Script
# with Tick Data Client
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#

# Importando biblioteca ZMQ para comunicação via sockets
import zmq

# Criando contexto ZMQ
context = zmq.Context()

# Criando socket do tipo Subscriber
socket = context.socket(zmq.SUB)

# Conectando ao servidor na porta 5555
socket.connect('tcp://0.0.0.0:5555')

# Inscrevendo-se para receber mensagens com prefixo 'SYMBOL'
socket.setsockopt_string(zmq.SUBSCRIBE, 'SYMBOL')

# Loop infinito para receber dados
while True:
    # Recebe string com dados do servidor
    data = socket.recv_string()
    # Imprime os dados recebidos
    print(data)