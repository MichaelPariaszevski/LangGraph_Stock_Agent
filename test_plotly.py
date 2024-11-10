import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# Force renderer
pio.renderers.default = 'browser'

try:
    symbol = 'AAPL'
    df = yf.download(symbol, start='2020-01-01')
    
    # Debug print data
    print("\nShape of dataframe:", df.shape)
    print("\nColumns:", df.columns.tolist())
    print("\nFirst 3 rows:")
    print(df.head(3).to_string())
    
    if df.empty:
        raise ValueError("No data downloaded")

    df = df.reset_index()
    
    # Create figure with explicit parameters
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing=dict(line=dict(color='green'), fillcolor='green'),
        decreasing=dict(line=dict(color='red'), fillcolor='red')
    )])

    # More explicit layout
    fig.update_layout(
        title=dict(
            text=f'{symbol} Stock Price',
            x=0.5
        ),
        yaxis_title='Stock Price (USD)',
        xaxis_title='Date',
        template='plotly_white',
        showlegend=False,
        xaxis_rangeslider_visible=False
    )

    # Save with full HTML
    fig.write_html("candlestick.html", include_plotlyjs=True, full_html=True)
    
    # Show with specific renderer
    fig.show(renderer='browser')

except Exception as e:
    print(f"Error occurred: {e}")
    raise  # Re-raise to see full traceback