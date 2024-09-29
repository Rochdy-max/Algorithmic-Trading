import backtrader as bt
import yfinance as yf
from MyStrategy import MyStrategy

#Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Add data
df = yf.download(
    tickers='BTC',
    period=None,
    start='2022-09-28',
    end='2024-09-28',
    interval='1d'
)
data = bt.feeds.PandasData(dataname=df)
cerebro.adddata(data) 

#Add strategy to Cerebro
cerebro.addstrategy(MyStrategy)

#Run Cerebro Engine
cerebro.run()