# financial_tick_client.py
import zmq
import time
import threading
import numpy as np
from collections import deque
from datetime import datetime
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Configuração do cliente ZMQ
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, 'SYMBOL')

# Buffers de dados
data_buffer = deque(maxlen=1000)
price_history = deque(maxlen=1000)
lock = threading.Lock()

def receive_data():
    """Recebe dados do servidor em segundo plano"""
    while True:
        try:
            msg = socket.recv_string()
            symbol, value = msg.split()
            timestamp = time.time()
            with lock:
                data_buffer.append((timestamp, float(value)))
                price_history.append(float(value))
        except Exception as e:
            print(f"Erro: {e}")

def calculate_sma(values, window):
    """Calcula a média móvel simples"""
    return [np.mean(values[i-window:i]) if i >= window else None 
            for i in range(1, len(values)+1)]

# Inicia thread de recebimento
thread = threading.Thread(target=receive_data)
thread.daemon = True
thread.start()

# Cria aplicativo Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Monitor de Preços em Tempo Real com SMA"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=500,
        n_intervals=0
    )
])

@app.callback(
    Output('live-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    with lock:
        if not data_buffer:
            return go.Figure()
        
        timestamps = [datetime.fromtimestamp(ts) for ts, _ in data_buffer]
        values = [val for _, val in data_buffer]
        sma5 = calculate_sma(values, 5)
        sma10 = calculate_sma(values, 10)

    traces = [
        go.Scatter(
            x=timestamps,
            y=values,
            mode='lines+markers',
            name='Preço',
            line=dict(color='#1f77b4', width=1)
        ),
        go.Scatter(
            x=timestamps,
            y=sma5,
            mode='lines',
            name='SMA 5',
            line=dict(color='#ff7f0e', width=2)
        ),
        go.Scatter(
            x=timestamps,
            y=sma10,
            mode='lines',
            name='SMA 10',
            line=dict(color='#2ca02c', width=2)
        )
    ]

    layout = go.Layout(
        title='Preço e Médias Móveis em Tempo Real',
        xaxis=dict(title='Horário'),
        yaxis=dict(title='Valor (USD)'),
        template='plotly_dark',
        showlegend=True,
        hovermode='x unified'
    )

    return {'data': traces, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)