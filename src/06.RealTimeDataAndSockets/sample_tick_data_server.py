#
# Python Script to Simulate a
# Financial Tick Data Server
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#

# Importando bibliotecas necessárias
import zmq  # Para comunicação via sockets
import math  # Para cálculos matemáticos
import time  # Para controle de tempo
import random  # Para geração de números aleatórios

# Configurando o socket ZMQ para publicação de dados
context = zmq.Context()
socket = context.socket(zmq.PUB)  # Socket do tipo Publisher
socket.bind('tcp://0.0.0.0:5555')  # Vinculando à porta 5555

# The class InstrumentPrice is for the simulation of instrument price values over time.
class InstrumentPrice(object):
    def __init__(self):
        # Inicializando atributos da classe
        self.symbol = 'SYMBOL'  # Símbolo do instrumento financeiro
        self.t = time.time()  # Tempo inicial
        self.value = 100.  # Valor inicial do ativo
        self.sigma = 0.4  # Volatilidade do ativo
        self.r = 0.01  # Taxa livre de risco

    # The method .simulate_value() generates new values for the stock price given the
    # time passed since it has been called the last time and a random factor:
    def simulate_value(self):
        ''' Generates a new, random stock price using Euler discretization of geometric Brownian motion.
        '''
        t = time.time()  # Tempo atual
        # Calcula a diferença de tempo em anos, considerando dias úteis e horário comercial
        dt = (t - self.t) / (252 * 8 * 60 * 60)
        dt *= 500  # Fator de aceleração da simulação. To have larger instrument price movements, this line of code scales the dt variable (by an arbitrary factor)
        self.t = t  # Atualiza o tempo
        # Calcula novo preço usando a fórmula de Black-Scholes
        self.value *= math.exp((self.r - 0.5 * self.sigma ** 2) * dt +
                             self.sigma * math.sqrt(dt) * random.gauss(0, 1))
        return self.value


# Cria uma instância da classe InstrumentPrice
ip = InstrumentPrice()

# Loop infinito para gerar e enviar dados
while True:
    # Formata a mensagem com o símbolo e o valor simulado
    msg = '{} {:.2f}'.format(ip.symbol, ip.simulate_value())
    print(msg)  # Exibe a mensagem no console
    socket.send_string(msg)  # Envia a mensagem através do socket
    time.sleep(random.random() * 2)  # Aguarda um tempo aleatório entre 0 e 2 segundos