import yfinance as yf
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class StockPlotterMPL:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def get_data(self):
        # Download data
        data = yf.download(tickers = self.ticker, start = self.start_date, end = self.end_date)
        data = data.reset_index() 
        for i in ["Open", "High", "Close", "Low"]: 
            data[i] = data[i].astype("float64")
        self.data = data
        return data

    def calculate_technical_indicators(self):
        # Calculate EMA
        self.data['EMA_8'] = self.data['Close'].ewm(span=8, adjust=False).mean()
        self.data['EMA_21'] = self.data['Close'].ewm(span=21, adjust=False).mean()

        # Calculate SMA
        self.data['SMA_10'] = self.data['Close'].rolling(window=10).mean()

        # Calculate RSI
        delta = self.data['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI_14'] = 100 - (100 / (1 + rs))

        # Calculate MACD
        ema_12 = self.data['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = self.data['Close'].ewm(span=26, adjust=False).mean()
        self.data['MACD'] = ema_12 - ema_26
        self.data['MACD_Signal'] = self.data['MACD'].ewm(span=9, adjust=False).mean()

        return self.data

    def plot_with_indicators(self):
        # Create figure and grid
        fig = plt.figure(figsize=(12, 8))
        gs = GridSpec(2, 1, height_ratios=[2, 1], hspace=0.3)

        # Plot candlesticks
        ax1 = fig.add_subplot(gs[0])
        mpf.plot(self.data, type='candle', style='charles', ax=ax1, volume=False)

        # Add technical indicators to price subplot
        ax1.plot(self.data.index, self.data['EMA_8'], label='EMA 8', color='orange', linewidth=1)
        ax1.plot(self.data.index, self.data['EMA_21'], label='EMA 21', color='blue', linewidth=1)
        ax1.plot(self.data.index, self.data['SMA_10'], label='SMA 10', color='purple', linewidth=1)
        ax1.set_ylabel('Price (USD)')
        ax1.set_title(f'{self.ticker} Stock Price')
        ax1.legend(loc='upper left')
        ax1.grid(True, linestyle='--', alpha=0.7)

        # Plot indicators
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        ax2.plot(self.data.index, self.data['RSI_14'], label='RSI 14', color='gray', linewidth=1)
        ax2.plot(self.data.index, self.data['MACD'], label='MACD', color='blue', linewidth=1)
        ax2.plot(self.data.index, self.data['MACD_Signal'], label='MACD Signal', color='orange', linewidth=1)
        ax2.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax2.set_ylabel('Indicators')
        ax2.legend(loc='upper left')
        ax2.grid(True, linestyle='--', alpha=0.7)

        plt.show()

if __name__ == "__main__":
    start_date = '2022-01-01'
    end_date = '2022-12-30'

    plotter = StockPlotterMPL(ticker='AAPL', start_date=start_date, end_date=end_date)
    plotter.get_data()
    plotter.calculate_technical_indicators()
    plotter.plot_with_indicators()