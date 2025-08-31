import plotly.graph_objs as go
import pandas as pd

def plot_line_price(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Date"], y=data["Close"], mode="lines", name="Close Price"
    ))
    fig.update_layout(title="Closing Price Over Time")
    return fig

def plot_candlestick(data):
    fig = go.Figure(data=[go.Candlestick(
        x=data["Date"],
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"]
    )])
    fig.update_layout(title="Candlestick Chart")
    return fig

def plot_volume_histogram(data):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data["Date"], y=data["Volume"], name="Volume"
    ))
    fig.update_layout(title="Traded Volume")
    return fig

def plot_price_with_ma(data, windows=[20, 50]):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Date"], y=data["Close"], mode="lines", name="Close Price"
    ))
    for window in windows:
        ma = data["Close"].rolling(window).mean()
        fig.add_trace(go.Scatter(
            x=data["Date"], y=ma, mode="lines", name=f"{window}-Day MA"
        ))
    fig.update_layout(title="Price with Moving Averages")
    return fig

def plot_ma_crossover(data, fast=20, slow=50):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Date"], y=data["Close"], mode="lines", name="Close Price"
    ))
    fast_ma = data["Close"].rolling(fast).mean()
    slow_ma = data["Close"].rolling(slow).mean()
    fig.add_trace(go.Scatter(x=data["Date"], y=fast_ma, mode="lines", name=f"{fast}-Day MA"))
    fig.add_trace(go.Scatter(x=data["Date"], y=slow_ma, mode="lines", name=f"{slow}-Day MA"))
    fig.update_layout(title="Moving Average Crossover")
    return fig

def plot_bollinger_bands(data, window=20):
    sma = data["Close"].rolling(window).mean()
    std = data["Close"].rolling(window).std()
    upper = sma + 2 * std
    lower = sma - 2 * std
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Date"], y=data["Close"], mode="lines", name="Close Price"
    ))
    fig.add_trace(go.Scatter(
        x=data["Date"], y=upper, mode="lines", name="Upper Band", line=dict(dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=data["Date"], y=lower, mode="lines", name="Lower Band", line=dict(dash="dash")
    ))
    fig.update_layout(title="Bollinger Bands")
    return fig

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def plot_rsi(data, period=14):
    rsi = compute_rsi(data["Close"], period=period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Date"], y=rsi, mode="lines", name="RSI"
    ))
    fig.update_layout(title=f"Relative Strength Index (RSI-{period})", yaxis=dict(range=[0, 100]))
    return fig

def plot_macd(data, fast=12, slow=26, signal=9):
    fast_ema = data["Close"].ewm(span=fast, adjust=False).mean()
    slow_ema = data["Close"].ewm(span=slow, adjust=False).mean()
    macd = fast_ema - slow_ema
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"], y=macd, name="MACD"))
    fig.add_trace(go.Scatter(x=data["Date"], y=signal_line, name="Signal Line"))
    fig.update_layout(title="MACD")
    return fig

def plot_volatility(data, window=20):
    returns = data["Close"].pct_change()
    rolling_vol = returns.rolling(window).std() * (252 ** 0.5)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Date"], y=rolling_vol, mode="lines", name="Volatility"
    ))
    fig.update_layout(title="Volatility (Rolling Annualized)")
    return fig

def plot_drawdown(data):
    running_max = data["Close"].cummax()
    drawdown = (data["Close"] - running_max) / running_max
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Date"], y=drawdown, mode="lines", name="Drawdown"
    ))
    fig.update_layout(title="Drawdown (Peak-to-Trough)", yaxis_tickformat="%")
    return fig
