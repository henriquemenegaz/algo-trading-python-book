"""
Python Script with Long-Short Class
for Event-Based Backtesting

Python for Algorithmic Trading
(c) Dr. Yves J. Hilpisch
The Python Quants GmbH

Edited by Henrique Menegaz
"""

from backtesting_base import BacktestBase


class BacktestLongShort(BacktestBase):
    def go_long(self, bar, units=None, amount=None):
        # In addition to bar, the methods expect either a number for the units of the traded instrument or a currency amount.
        # If the position is short, the method places a buy order for the same number of units.
        if self.position == -1:
            self.place_buy_order(bar, units=-self.units)
        # If a number of units is provided, the method places a buy order for the given number of units.
        if units:
            self.place_buy_order(bar, units=units)
        # If a currency amount is provided, the method places a buy order for the given amount.
        elif amount:
            if amount == 'all':
                amount = self.amount
            self.place_buy_order(bar, amount=amount)

    def go_short(self, bar, units=None, amount=None):
        # If the position is long, the method places a sell order for the same number of units.
        if self.position == 1:
            self.place_sell_order(bar, units=self.units)
        # If a number of units is provided, the method places a sell order for the given number of units.
        if units:
            self.place_sell_order(bar, units=units)
        # If a currency amount is provided, the method places a sell order for the given amount.
        elif amount:
            if amount == 'all':
                amount = self.amount
            self.place_sell_order(bar, amount=amount)

    def run_sma_strategy(self, SMA_LENGTH1, SMA_LENGTH2):
        msg = f'\n\nRunning SMA strategy | SMA1={SMA_LENGTH1} & SMA2={SMA_LENGTH2}'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)

        self.position = 0  # initial neutral position
        self.trades = 0  # no trades yet
        self.amount = self.initial_amount  # reset initial capital

        self.data['SMA1'] = self.data['price'].rolling(SMA_LENGTH1).mean()
        self.data['SMA2'] = self.data['price'].rolling(SMA_LENGTH2).mean()

        # The strategy is implemented in a loop that iterates over all bars in the data set.
        for bar in range(SMA_LENGTH2, len(self.data)):
            # If the position is short or neutral, it is checked whether the short-term SMA is above the long-term SMA.
            if self.position in [0, -1]:
                if self.data['SMA1'].iloc[bar] > self.data['SMA2'].iloc[bar]:
                    self.go_long(bar, amount='all')
                    self.position = 1  # long position
            # If the position is long, it is checked whether the short-term SMA is below the long-term SMA.
            if self.position in [0, 1]:
                if self.data['SMA1'].iloc[bar] < self.data['SMA2'].iloc[bar]:
                    self.go_short(bar, amount='all')
                    self.position = -1  # short position
        self.close_out(bar)

    def run_momentum_strategy(self, MOMENTUM):
        msg = f'\n\nRunning momentum strategy | {MOMENTUM} days'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)

        self.position = 0  # initial neutral position
        self.trades = 0  # no trades yet
        self.amount = self.initial_amount  # reset initial capital

        self.data['momentum'] = self.data['return'].rolling(MOMENTUM).mean()

        # The strategy is implemented in a loop that iterates over all bars in the data set.
        for bar in range(MOMENTUM, len(self.data)):
            # If the position is short or neutral, it is checked whether the momentum is positive.
            if self.position in [0, -1]:
                if self.data['momentum'].iloc[bar] > 0:
                    self.go_long(bar, amount='all')
                    self.position = 1  # long position
            # If the position is long, it is checked whether the momentum is negative.
            if self.position in [0, 1]:
                if self.data['momentum'].iloc[bar] <= 0:
                    self.go_short(bar, amount='all')
                    self.position = -1  # short position
        self.close_out(bar)

    def run_mean_reversion_strategy(self, SMA_LENGTH, THRESHOLD):
        msg = '\n\nRunning mean reversion strategy | '
        msg += f'SMA={SMA_LENGTH} & thr={THRESHOLD}'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)

        self.position = 0  # initial neutral position
        self.trades = 0  # no trades yet
        self.amount = self.initial_amount  # reset initial capital

        self.data['SMA'] = self.data['price'].rolling(SMA_LENGTH).mean()

        # The strategy is implemented in a loop that iterates over all bars in the data set.    
        for bar in range(SMA_LENGTH, len(self.data)):
            # If the position is short or neutral, it is checked whether the price is below the SMA minus the threshold.
            if self.position == 0:
                if (self.data['price'].iloc[bar] < self.data['SMA'].iloc[bar] - THRESHOLD):
                    # If the price is below the SMA minus the threshold, the position is opened by placing a buy order.
                    self.go_long(bar, amount=self.initial_amount)
                    self.position = 1
                elif (self.data['price'].iloc[bar] > self.data['SMA'].iloc[bar] + THRESHOLD):
                    # If the price is above the SMA plus the threshold, the position is closed by placing a sell order.
                    self.go_short(bar, amount=self.initial_amount)
                    self.position = -1
            # If the position is long, it is checked whether the price is above the SMA.
            elif self.position == 1:
                if self.data['price'].iloc[bar] >= self.data['SMA'].iloc[bar]:
                    # If the price is above the SMA, the position is closed by placing a sell order.
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0
            # If the position is short, it is checked whether the price is below the SMA.
            elif self.position == -1:
                if self.data['price'].iloc[bar] <= self.data['SMA'].iloc[bar]:
                    # If the price is below the SMA, the position is closed by placing a buy order.
                    self.place_buy_order(bar, units=-self.units)
                    self.position = 0
        self.close_out(bar)


if __name__ == '__main__':
    def run_strategies():
        lsbt.run_sma_strategy(42, 252)
        lsbt.run_momentum_strategy(60)
        lsbt.run_mean_reversion_strategy(50, 5)

    lsbt = BacktestLongShort('EUR=', '2010-1-1', '2019-12-31', 10000,verbose=False)
    run_strategies()

    # transaction costs: 10 USD fix, 1% variable
    lsbt = BacktestLongShort('AAPL.O', '2010-1-1', '2019-12-31',10000, 10.0, 0.01, False)
    run_strategies()