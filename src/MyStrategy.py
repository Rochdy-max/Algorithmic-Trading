import backtrader as bt
from datetime import datetime

class MyStrategy(bt.Strategy):
    def __init__(self):
        pass

    def log(self, msg):
        dt = datetime.now()
        print('{} | {}'.format(dt, msg))

    def next(self):
        current_bar = self.datas[0]
        self.log('-' * 50)
        self.log(f'Datetime: {current_bar.datetime.datetime()}')
        self.log(f'Close size: {len(current_bar.close)}')
        self.log(f'Current close value: {current_bar.close[0]}')
