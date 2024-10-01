import sys
import backtrader as bt
import yfinance as yf
from MyStrategy import MyStrategy

if __name__ == '__main__':
    # Instantiate Cerebro engine
    cerebro = bt.Cerebro()

    # Get data
    symbol = 'BTC-USD'
    df = yf.download(
        tickers=symbol,
        period=None,
        start='2022-09-28',
        end='2024-09-28',
        interval='1d'
    )
    # Quit if dataframe is empty
    if df.empty:
        print('\nDataframe is empty for symbol : <{}>'.format(symbol))
        print('Stop program execution')
        sys.exit(0)
    # Data feeds
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    # Add strategy to Cerebro
    cerebro.addstrategy(MyStrategy)

    # Run Cerebro Engine
    cerebro.run()