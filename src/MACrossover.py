import backtrader as bt

class MACrossover(bt.Strategy):
    params = (
        ('pfast', 50),
        ('pslow', 100),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        # Order details
        self.order = None
        self.fast_sma = bt.indicators.MovingAverageSimple(
            self.datas[0],
            period=self.params.pfast
        )

        self.slow_sma = bt.indicators.MovingAverageSimple(
            self.datas[0],
            period=self.params.pslow
        )

    def log(self, msg):
        dt = self.datetime.date()
        print('{} | {}'.format(dt, msg))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None

    def next(self):
        # Check for open orders
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # We are not in the market, look for a signal to OPEN trades
                
            # If the 20 SMA is above the 50 SMA -> BUY
            if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] <= self.slow_sma[-1]:
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            # Otherwise if the 20 SMA is below the 50 SMA -> SELL
            elif self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] >= self.slow_sma[-1]:
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        else:
            # We are already in the market, look for a signal to CLOSE trades
            if len(self) >= (self.bar_executed + 5):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
