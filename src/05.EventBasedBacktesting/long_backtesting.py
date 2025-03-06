"""
Python Script with Long Only Class
for Event-Based Backtesting

Python for Algorithmic Trading
(c) Dr. Yves J. Hilpisch
The Python Quants GmbH

Edited by Henrique Menegaz
"""

# Importa a classe base para backtesting
from backtesting_base import BacktestBase


class BacktestLongOnly(BacktestBase):
    def run_sma_strategy(self, SMA_LENGTH1, SMA_LENGTH2):
        """Backtesting an SMA-based strategy.

        Parameters
        ----------
        sma1 : int
            Shorter term simple moving average (in days)
        sma2 : int 
            Longer term simple moving average (in days)
        """
        # Imprime mensagem inicial com parâmetros da estratégia
        msg = f'\n\nRunning SMA strategy | SMA1={SMA_LENGTH1} & SMA2={SMA_LENGTH2}'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)

        # Inicializa variáveis de controle
        self.position = 0  # posição inicial neutra
        self.trades = 0  # sem trades inicialmente
        self.amount = self.initial_amount  # reseta capital inicial

        # Calcula as médias móveis
        self.data['SMA1'] = self.data['price'].rolling(SMA_LENGTH1).mean()
        self.data['SMA2'] = self.data['price'].rolling(SMA_LENGTH2).mean()

        # Loop principal da estratégia
        for bar in range(SMA_LENGTH2, len(self.data)):
            if self.position == 0:  # Se não tem posição
                if self.data['SMA1'].iloc[bar] > self.data['SMA2'].iloc[bar]:
                    # Compra quando SMA curta cruza acima da SMA longa
                    self.place_buy_order(bar, amount=self.amount)
                    self.position = 1  # assume posição comprada
            elif self.position == 1:  # Se tem posição comprada
                if self.data['SMA1'].iloc[bar] < self.data['SMA2'].iloc[bar]:
                    # Vende quando SMA curta cruza abaixo da SMA longa
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0  # volta para neutro
        self.close_out(bar)  # Fecha posições no final

    def run_momentum_strategy(self, momentum):
        """Backtesting a momentum-based strategy.

        Parameters
        ----------
        momentum : int
            Number of days for mean return calculation
        """
        # Imprime mensagem inicial com parâmetros
        msg = f'\n\nRunning momentum strategy | {momentum} days'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)

        # Inicializa variáveis de controle
        self.position = 0  # posição inicial neutra
        self.trades = 0  # sem trades inicialmente
        self.amount = self.initial_amount  # reseta capital inicial

        # Calcula o momentum como média móvel dos retornos
        self.data['momentum'] = self.data['return'].rolling(momentum).mean()

        # Loop principal da estratégia
        for bar in range(momentum, len(self.data)):
            if self.position == 0:  # Se não tem posição
                if self.data['momentum'].iloc[bar] > 0:
                    # Compra quando momentum é positivo
                    self.place_buy_order(bar, amount=self.amount)
                    self.position = 1  # assume posição comprada
            elif self.position == 1:  # Se tem posição comprada
                if self.data['momentum'].iloc[bar] < 0:
                    # Vende quando momentum é negativo
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0  # volta para neutro
        self.close_out(bar)  # Fecha posições no final

    def run_mean_reversion_strategy(self, SMA_LENGTH, THRESHOLD):
        """Backtesting a mean reversion-based strategy.

        Parameters
        ----------
        sma : int
            Simple moving average in days
        threshold : float
            Absolute value for deviation-based signal relative to SMA
        """
        # Imprime mensagem inicial com parâmetros
        msg = '\n\nRunning mean reversion strategy | '
        msg += f'SMA={SMA_LENGTH} & thr={THRESHOLD}'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)

        # Inicializa variáveis de controle
        self.position = 0
        self.trades = 0
        self.amount = self.initial_amount

        # Calcula a média móvel simples
        self.data['SMA'] = self.data['price'].rolling(SMA_LENGTH).mean()

        # Loop principal da estratégia
        for bar in range(SMA_LENGTH, len(self.data)):
            if self.position == 0:
                # Se não tem posição, verifica se preço está abaixo da SMA - threshold
                if (self.data['price'].iloc[bar] < self.data['SMA'].iloc[bar] - THRESHOLD):
                    self.place_buy_order(bar, amount=self.amount)
                    self.position = 1
            elif self.position == 1:
                # Se tem posição comprada, verifica se preço retornou para SMA
                if self.data['price'].iloc[bar] >= self.data['SMA'].iloc[bar]:
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0
        self.close_out(bar)  # Fecha posições no final


if __name__ == '__main__':
    def run_strategies():
        # Executa as três estratégias em sequência
        lobt.run_sma_strategy(42, 252)
        lobt.run_momentum_strategy(60)
        lobt.run_mean_reversion_strategy(50, 5)

    # Teste sem custos de transação
    lobt = BacktestLongOnly('AAPL.O', '2010-1-1', '2019-12-31',10000, verbose=False)
    run_strategies()

    # Teste com custos de transação: 10 USD fixo, 1% variável
    lobt = BacktestLongOnly('AAPL.O', '2010-1-1', '2019-12-31',10000, 10.0, 0.01, False)
    run_strategies()