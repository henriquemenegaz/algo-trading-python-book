#
# Python Script
# with Online Trading Algorithm
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import datetime

import numpy as np
import pandas as pd
import zmq

# Configuração do socket ZMQ para receber dados
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://0.0.0.0:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, 'SYMBOL')

# Inicialização das variáveis
df = pd.DataFrame()  # DataFrame vazio para armazenar dados
MOM = 3  # Período para cálculo do momentum
MIN_LENGTH = MOM + 1  # Tamanho mínimo necessário de dados

while True:
    # Recebe e processa os dados do socket
    data = socket.recv_string()
    t = datetime.datetime.now()  # Timestamp atual
    sym, value = data.split()  # Separa símbolo e valor
    
    # Adiciona novo dado ao DataFrame
    df = pd.concat([df, pd.DataFrame({sym: float(value)}, index=[t])])
    
    # Reamostra os dados a cada 5 segundos
    dr = df.resample('5s', label='right').last()
    
    # Calcula os retornos logarítmicos
    dr['returns'] = np.log(dr / dr.shift(1))
    
    # Verifica se há dados suficientes para calcular o momentum
    if len(dr) > MIN_LENGTH:
        MIN_LENGTH += 1
        # Calcula o indicador de momentum
        dr['momentum'] = np.sign(dr['returns'].rolling(MOM).mean())
        
        # Exibe informações sobre o novo sinal
        print('\n' + '=' * 51)
        print('NEW SIGNAL | {}'.format(datetime.datetime.now()))
        print('=' * 51)
        print(dr.iloc[:-1].tail())
        
        # Verifica sinais de compra/venda
        if dr['momentum'].iloc[-2] == 1.0:
            print('\nLong market position.')
            # take some action (e.g., place buy order)
        elif dr['momentum'].iloc[-2] == -1.0:
            print('\nShort market position.')
            # take some action (e.g., place sell order)