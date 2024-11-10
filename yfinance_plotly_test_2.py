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
        data = yf.download(tickers = self.ticker, start = self.start_date, end = self.end_date)
        data = data.reset_index() 
        for i in ["Open", "High", "Close", "Low"]: 
            data[i] = data[i].astype("float64")
        self.data = data
        return data
    
    def calculate_technical_indicators(self):
    # Calculate EMA
        self.data['EMA_8'] = self.data['Close'][f"{self.ticker}"].ewm(span=8, adjust=False).mean()
        self.data['EMA_21'] = self.data['Close'][f"{self.ticker}"].ewm(span=21, adjust=False).mean()

        # Calculate SMA
        self.data['SMA_10'] = self.data['Close'][f"{self.ticker}"].rolling(window=10).mean()

        # Calculate RSI
        delta = self.data['Close'][f"{self.ticker}"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI_14'] = 100 - (100 / (1 + rs))

        # Calculate MACD
        ema_12 = self.data['Close'][f"{self.ticker}"].ewm(span=12, adjust=False).mean()
        ema_26 = self.data['Close'][f"{self.ticker}"].ewm(span=26, adjust=False).mean()
        self.data['MACD'] = ema_12 - ema_26
        self.data['MACD_Signal'] = self.data['MACD'].ewm(span=9, adjust=False).mean()

        # Calculate Parabolic SAR
        self.data['SAR'] = self.data['Close'][f"{self.ticker}"].rolling(window=4).apply(lambda x: x.min() if x.idxmin() == x.index[-1] else x.max())

        return self.data
        
    def plot_with_indicators_2(self):
    # Create figure with secondary y-axis using subplots
        fig = sp.make_subplots(rows=2, cols=1, 
                            shared_xaxes=True,
                            vertical_spacing=0.03,
                            subplot_titles=('Price', 'Indicators'),
                            row_heights=[0.7, 0.3])

        # Add candlestick with enhanced visibility settings
        fig.add_trace(go.Candlestick(
            x=self.data["Date"],
            open=self.data['Open'][f"{self.ticker}"],
            high=self.data['High'][f"{self.ticker}"],
            low=self.data['Low'][f"{self.ticker}"],
            close=self.data['Close'][f"{self.ticker}"],
            name='Candlestick',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350',
            increasing_fillcolor='#26a69a',
            decreasing_fillcolor='#ef5350',
            line=dict(width=1),
            opacity=1,
            showlegend=True,
            visible=True,
        ), row=1, col=1)

        # Add EMA lines to first subplot
        fig.add_trace(go.Scatter(
            x=self.data.index, y=self.data['EMA_8'],
            mode='lines', name='EMA 8',
            line=dict(color='orange', width=1)
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=self.data.index, y=self.data['EMA_21'],
            mode='lines', name='EMA 21',
            line=dict(color='blue', width=1)
        ), row=1, col=1)

        # Add SMA to first subplot
        fig.add_trace(go.Scatter(
            x=self.data.index, y=self.data['SMA_10'],
            mode='lines', name='SMA 10',
            line=dict(color='purple', width=1)
        ), row=1, col=1)

        # Add indicators to second subplot
        fig.add_trace(go.Scatter(
            x=self.data.index, y=self.data['RSI_14'],
            mode='lines', name='RSI 14',
            line=dict(color='gray', width=1)
        ), row=2, col=1)

        fig.add_trace(go.Scatter(
            x=self.data.index, y=self.data['MACD'],
            mode='lines', name='MACD',
            line=dict(color='blue', width=1)
        ), row=2, col=1)

        fig.add_trace(go.Scatter(
            x=self.data.index, y=self.data['MACD_Signal'],
            mode='lines', name='MACD Signal',
            line=dict(color='orange', width=1)
        ), row=2, col=1)

        fig.update_layout(
            title='Stock Price Data with Technical Indicators',
            height=800,
            showlegend=True,
            xaxis_rangeslider_visible=False,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='rgba(0, 0, 0, 0.2)',
                borderwidth=1
            ),
            # Ensure candlestick visibility
            uirevision=True
        )

        # Update yaxis properties
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Indicators", row=2, col=1)

        fig.show()
        
    def plot_with_indicators_3(self):
        # Convert dataframes to series 
        # Create figure
        fig_2 = go.Figure(data=[go.Candlestick(
            x=self.data["Date"],
            open=self.data['Open']["AAPL"],
            high=self.data['High']["AAPL"],
            low=self.data['Low']["AAPL"],
            close=self.data['Close']["AAPL"])])

        print(type(self.data))
        print(type(self.data["Date"]))
        print(type(self.data["Open"][f"{self.ticker}"]))
        
        fig_2.show()
        
start_date = '2022-01-01'
end_date = '2022-12-30'        

example = StockPlotter(ticker = 'AAPL', start_date = start_date, end_date = end_date) 

example.get_data() 
example.calculate_technical_indicators() 
example.plot_with_indicators_2()
example.plot_with_indicators_3()