import backtrader as bt

class MACrossover(bt.Strategy):
    params = (
        ('pfast', 2),
        ('pslow', 10),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        # Order details
        self.order = None
        self.order_executed = None
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
                self.order_executed = 'BUY'
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
                self.order_executed = 'SELL'
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Check for open orders
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Check if we're not at the end
            try:
                _ = self.dataclose[5]
            except:
                print('END OF TESTING')
                return
            # We are not in the market, look for a signal to OPEN trades
                
            # If the fast SMA is above the slow SMA -> BUY
            if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] <= self.slow_sma[-1]:
                self.log(f'BUY CREATED, {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            # Otherwise if the fast SMA is below the slow SMA -> SELL
            elif self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] >= self.slow_sma[-1]:
                self.log(f'SELL CREATED, {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        else:
            # We are already in the market, look for a signal to CLOSE trades
            # if len(self) >= (self.bar_executed + 5):
            #     self.log(f'CLOSE CREATED, {self.dataclose[0]:2f}')
            #     self.order = self.close()
            if not self.order_executed:
                return
            print('CHECK')
            # If BUY and in-market SMA is below fast SMA
            if self.order_executed == 'BUY' and self.dataclose[0] < self.fast_sma[0] and self.dataclose[-1] >= self.fast_sma[-1]:
                self.log(f'CLOSE CREATED, {self.dataclose[0]:2f}')
                self.order = self.close()
                self.order_executed = None
            # If SELL and in-market SMA is above fast SMA
            if self.order_executed == 'SELL' and self.dataclose[0] > self.fast_sma[0] and self.dataclose[-1] <= self.fast_sma[-1]:
                self.log(f'CLOSE CREATED, {self.dataclose[0]:2f}')
                self.order = self.close()
                self.order_executed = None
