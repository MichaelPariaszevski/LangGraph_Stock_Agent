import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.offline import iplot


class StockPlotter:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def get_data(self):
    # Retrieve stock data from Yahoo Finance
        data = yf.download(tickers=self.ticker, start=self.start_date, end=self.end_date)
        data = data.reset_index()
        for i in ["Open", "High", "Close", "Low"]:
            data[i] = data[i].astype("float64")
        self.data = data
        return data

    def calculate_technical_indicators(self):
        # Ensure we're working with the filtered dataset
        if self.data is None:
            self.get_data()

        # Calculate EMA
        self.data['EMA_8'] = self.data['Close'].ewm(span=8, adjust=False).mean()
        self.data['EMA_21'] = self.data['Close'].ewm(span=21, adjust=False).mean()

        # Calculate SMA
        self.data['SMA_10'] = self.data['Close'].rolling(window=10).mean()

        # Calculate RSI
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI_14'] = 100 - (100 / (1 + rs))

        # Calculate MACD
        ema_12 = self.data['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = self.data['Close'].ewm(span=26, adjust=False).mean()
        self.data['MACD'] = ema_12 - ema_26
        self.data['MACD_Signal'] = self.data['MACD'].ewm(span=9, adjust=False).mean()

        # Calculate Parabolic SAR
        self.data['SAR'] = self.data['Close'].rolling(window=4).apply(
            lambda x: x.min() if x.idxmin() == x.index[-1] else x.max()
        )

        return self.data
        
    def plot_with_indicators_2(self):
    # Create figure with secondary y-axis
        fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, 
                            subplot_titles=('Price', 'Indicators'))

        # Add candlestick
        fig.add_trace(go.Candlestick(
            x=self.data["Date"],
            open=self.data['Open'],
            high=self.data['High'],
            low=self.data['Low'],
            close=self.data['Close'],
            name="OHLC"), row=1, col=1)

        # Add EMA traces
        fig.add_trace(go.Scatter(
            x=self.data["Date"],
            y=self.data['EMA_8'],
            name="EMA 8"), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=self.data["Date"],
            y=self.data['EMA_21'],
            name="EMA 21"), row=1, col=1)

        # Add RSI
        fig.add_trace(go.Scatter(
            x=self.data["Date"],
            y=self.data['RSI_14'],
            name="RSI"), row=2, col=1)

        # Update layout
        fig.update_layout(
            title=f'{self.ticker} Stock Price',
            yaxis_title="Stock Price (USD)",
            xaxis_title="Date",
            legend=dict(
                x=0.01,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='rgba(0, 0, 0, 0.2)',
                borderwidth=1
            ),
            uirevision=True
        )

        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Indicators", row=2, col=1)

        fig.show()

    def plot_with_indicators_3(self):
        # Create figure
        fig_2 = go.Figure(data=[go.Candlestick(
            x=self.data["Date"],
            open=self.data['Open'],
            high=self.data['High'],
            low=self.data['Low'],
            close=self.data['Close'])])

        fig_2.show()

# Use dates in the past
start_date = '2023-10-10'
end_date = '2024-02-10'        

example = StockPlotter(ticker='AAPL', start_date=start_date, end_date=end_date)
example.get_data()
example.calculate_technical_indicators()
example.plot_with_indicators_2()
example.plot_with_indicators_3()
    