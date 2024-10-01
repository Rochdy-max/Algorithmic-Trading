import backtrader as bt
from datetime import datetime

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        # Another feed ?
        # self.otherclose = self.datas[1].close

    def log(self, msg):
        dt = datetime.now()
        print('{} | {}'.format(dt, msg))

    def next(self):
        self.log('=' * 50)
        self.log(f'Datetime: {self.datas[0].datetime.date()}')
        self.log(f'Close size: {len(self.datas[0].close)}')
        self.log(f'Current close value: {self.dataclose[0]}')

        # Another feed ?
        # self.log('-' * 50)
        # self.log(f'Datetime: {self.datas[1].datetime.date()}')
        # self.log(f'Close size: {len(self.datas[1].close)}')
        # self.log(f'Current close value: {self.otherclose[0]}')
