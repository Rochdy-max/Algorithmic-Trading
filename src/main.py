import sys
import backtrader as bt
import yfinance as yf
from strategies import *

if __name__ == '__main__':
    # Instantiate Cerebro engine
    cerebro = bt.Cerebro()

    # Get data
    symbol = 'BTC-USD'
    df = yf.download(
        tickers=symbol,
        period=None,
        start='2021-01-01',
        end='2024-12-25',
        interval='1d'
    )
    # Quit if dataframe is empty
    if df.empty:
        print('\nDataframe is empty for symbol : <{}>'.format(symbol))
        print('Stop program execution')
        sys.exit(0)

    # Data feeds
    in_sample_fromdate = '2021-01-01'
    in_sample_todate = '2022-12-25'

    in_sample_data = bt.feeds.PandasData(
        dataname=df.loc[in_sample_fromdate:in_sample_todate],
    )
    cerebro.adddata(in_sample_data)

    # Set default position size
    cerebro.addsizer(bt.sizers.SizerFix, stake=3)

    # Add strategy to Cerebro
    cerebro.addstrategy(MyStrategy)

    # Get starting portfolio value
    start_portfolio_value = cerebro.broker.getvalue()

    # Run Cerebro Engine
    cerebro.run()

    # Get end portfolio value
    end_portfolio_value = cerebro.broker.getvalue()

    # Profit and Loss
    pnl = end_portfolio_value - start_portfolio_value

    # Log key info
    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')
