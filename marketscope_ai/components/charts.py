# components/charts.py
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def create_candlestick_chart(price_data, symbol: str, height: int = 400):
    """
    Create a candlestick chart with price data
    
    Args:
        price_data: DataFrame with OHLC data
        symbol: Stock symbol for title
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if price_data is None or price_data.empty:
        return None
        
    fig = go.Figure(data=[go.Candlestick(
        x=price_data.index,
        open=price_data['Open'],
        high=price_data['High'],
        low=price_data['Low'],
        close=price_data['Close'],
        name="Price"
    )])
    
    fig.update_layout(
        title=f'{symbol.upper()} - Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        height=height,
        xaxis_rangeslider_visible=False,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_volume_chart(price_data, symbol: str, height: int = 250):
    """
    Create a volume bar chart
    
    Args:
        price_data: DataFrame with Volume column
        symbol: Stock symbol for title
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if price_data is None or price_data.empty or 'Volume' not in price_data.columns:
        return None
    
    # Color bars based on price direction
    colors = ['green' if close >= open_price else 'red' 
              for close, open_price in zip(price_data['Close'], price_data['Open'])]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=price_data.index,
        y=price_data['Volume'],
        name='Volume',
        marker_color=colors,
        opacity=0.7
    ))
    
    fig.update_layout(
        title=f'{symbol.upper()} - Trading Volume',
        xaxis_title='Date',
        yaxis_title='Volume',
        height=height,
        template='plotly_white',
        showlegend=False
    )
    
    return fig


def create_price_with_moving_averages(price_data, symbol: str, windows=[20, 50], height: int = 400):
    """
    Create a price chart with moving averages
    
    Args:
        price_data: DataFrame with Close column
        symbol: Stock symbol for title
        windows: List of moving average windows
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if price_data is None or price_data.empty or 'Close' not in price_data.columns:
        return None
        
    fig = go.Figure()
    
    # Add close price
    fig.add_trace(go.Scatter(
        x=price_data.index,
        y=price_data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='blue', width=2)
    ))
    
    # Add moving averages
    colors = ['orange', 'red', 'purple', 'brown']
    for i, window in enumerate(windows):
        ma = price_data['Close'].rolling(window=window).mean()
        fig.add_trace(go.Scatter(
            x=price_data.index,
            y=ma,
            mode='lines',
            name=f'{window}-Day MA',
            line=dict(color=colors[i % len(colors)], width=1.5)
        ))
    
    fig.update_layout(
        title=f'{symbol.upper()} - Price with Moving Averages',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        height=height,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_revenue_income_chart(trend_data, symbol: str, height: int = 400):
    """
    Create a bar chart showing revenue vs net income trend
    
    Args:
        trend_data: DataFrame with 'Year', 'Revenue', 'Net Income' columns
        symbol: Stock symbol for title
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    # FIXED: Proper DataFrame validation - this was the line causing the error
    if trend_data is None or trend_data.empty or 'Year' not in trend_data.columns:
        return None
    
    # Ensure we have the required columns
    required_columns = ['Year', 'Revenue', 'Net Income']
    if not all(col in trend_data.columns for col in required_columns):
        return None
    
    fig = go.Figure()
    
    # Add Revenue bars
    fig.add_trace(go.Bar(
        x=trend_data['Year'],
        y=trend_data['Revenue'],
        name='Revenue',
        marker_color='lightblue',
        opacity=0.8
    ))
    
    # Add Net Income bars
    fig.add_trace(go.Bar(
        x=trend_data['Year'],
        y=trend_data['Net Income'],
        name='Net Income',
        marker_color='lightgreen',
        opacity=0.8
    ))
    
    fig.update_layout(
        title=f'{symbol.upper()} - Revenue vs Net Income Trend',
        xaxis_title='Year',
        yaxis_title='Amount ($)',
        height=height,
        barmode='group',
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_earnings_trend_chart(earnings_data, symbol: str, chart_type='annual', height: int = 300):
    """
    Create earnings trend chart (annual or quarterly)
    
    Args:
        earnings_data: DataFrame with earnings data
        symbol: Stock symbol for title
        chart_type: 'annual' or 'quarterly'
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if earnings_data is None or earnings_data.empty:
        return None
    
    # Check if 'Earnings' column exists
    if 'Earnings' not in earnings_data.columns:
        return None
    
    fig = go.Figure()
    
    if chart_type == 'annual':
        fig.add_trace(go.Bar(
            x=earnings_data.index,
            y=earnings_data['Earnings'],
            name='Annual EPS',
            marker_color='lightgreen',
            opacity=0.8
        ))
        title = f'{symbol.upper()} - Annual EPS Trend'
        yaxis_title = 'EPS ($)'
    else:  # quarterly
        fig.add_trace(go.Scatter(
            x=earnings_data.index,
            y=earnings_data['Earnings'],
            mode='lines+markers',
            name='Quarterly EPS',
            line=dict(color='orange', width=2),
            marker=dict(size=6)
        ))
        title = f'{symbol.upper()} - Quarterly EPS Trend'
        yaxis_title = 'EPS ($)'
    
    fig.update_layout(
        title=title,
        xaxis_title='Period',
        yaxis_title=yaxis_title,
        height=height,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_bollinger_bands_chart(price_data, symbol: str, window=20, height: int = 400):
    """
    Create a Bollinger Bands chart
    
    Args:
        price_data: DataFrame with Close column
        symbol: Stock symbol for title
        window: Rolling window for calculations
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if price_data is None or price_data.empty or 'Close' not in price_data.columns:
        return None
        
    # Calculate Bollinger Bands
    sma = price_data['Close'].rolling(window=window).mean()
    std = price_data['Close'].rolling(window=window).std()
    upper_band = sma + (2 * std)
    lower_band = sma - (2 * std)
    
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(go.Scatter(
        x=price_data.index,
        y=price_data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='blue', width=2)
    ))
    
    # Add upper band
    fig.add_trace(go.Scatter(
        x=price_data.index,
        y=upper_band,
        mode='lines',
        name='Upper Band',
        line=dict(color='red', dash='dash', width=1)
    ))
    
    # Add lower band
    fig.add_trace(go.Scatter(
        x=price_data.index,
        y=lower_band,
        mode='lines',
        name='Lower Band',
        line=dict(color='red', dash='dash', width=1),
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.1)'
    ))
    
    # Add middle line (SMA)
    fig.add_trace(go.Scatter(
        x=price_data.index,
        y=sma,
        mode='lines',
        name=f'{window}-Day SMA',
        line=dict(color='orange', width=1)
    ))
    
    fig.update_layout(
        title=f'{symbol.upper()} - Bollinger Bands ({window} days)',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        height=height,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_rsi_chart(price_data, symbol: str, period=14, height: int = 250):
    """
    Create an RSI (Relative Strength Index) chart
    
    Args:
        price_data: DataFrame with Close column
        symbol: Stock symbol for title
        period: RSI calculation period
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if price_data is None or price_data.empty or 'Close' not in price_data.columns:
        return None
        
    # Calculate RSI
    delta = price_data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    fig = go.Figure()
    
    # Add RSI line
    fig.add_trace(go.Scatter(
        x=price_data.index,
        y=rsi,
        mode='lines',
        name=f'RSI ({period})',
        line=dict(color='purple', width=2)
    ))
    
    # Add overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", 
                  annotation_text="Overbought (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", 
                  annotation_text="Oversold (30)")
    
    fig.update_layout(
        title=f'{symbol.upper()} - RSI ({period} days)',
        xaxis_title='Date',
        yaxis_title='RSI',
        height=height,
        yaxis=dict(range=[0, 100]),
        template='plotly_white'
    )
    
    return fig


def create_macd_chart(price_data, symbol: str, fast=12, slow=26, signal=9, height: int = 300):
    """
    Create a MACD chart
    
    Args:
        price_data: DataFrame with Close column
        symbol: Stock symbol for title
        fast: Fast EMA period
        slow: Slow EMA period
        signal: Signal line period
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if price_data is None or price_data.empty or 'Close' not in price_data.columns:
        return None
        
    # Calculate MACD
    exp1 = price_data['Close'].ewm(span=fast).mean()
    exp2 = price_data['Close'].ewm(span=slow).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal).mean()
    histogram = macd - signal_line
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('MACD Line', 'MACD Histogram'),
        row_heights=[0.7, 0.3]
    )
    
    # Add MACD line
    fig.add_trace(go.Scatter(
        x=price_data.index,
        y=macd,
        mode='lines',
        name='MACD',
        line=dict(color='blue', width=2)
    ), row=1, col=1)
    
    # Add Signal line
    fig.add_trace(go.Scatter(
        x=price_data.index,
        y=signal_line,
        mode='lines',
        name='Signal',
        line=dict(color='red', width=2)
    ), row=1, col=1)
    
    # Add histogram
    colors = ['green' if val >= 0 else 'red' for val in histogram]
    fig.add_trace(go.Bar(
        x=price_data.index,
        y=histogram,
        name='Histogram',
        marker_color=colors,
        opacity=0.7
    ), row=2, col=1)
    
    fig.update_layout(
        title=f'{symbol.upper()} - MACD ({fast}, {slow}, {signal})',
        height=height,
        template='plotly_white',
        showlegend=True
    )
    
    return fig


def create_volatility_chart(price_data, symbol: str, window=20, height: int = 300):
    """
    Create a volatility chart
    
    Args:
        price_data: DataFrame with Close column
        symbol: Stock symbol for title
        window: Rolling window for volatility calculation
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if price_data is None or price_data.empty or 'Close' not in price_data.columns:
        return None
        
    # Calculate returns and rolling volatility
    returns = price_data['Close'].pct_change()
    rolling_vol = returns.rolling(window=window).std() * np.sqrt(252)  # Annualized
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=price_data.index,
        y=rolling_vol,
        mode='lines',
        name=f'{window}-Day Volatility',
        line=dict(color='red', width=2),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title=f'{symbol.upper()} - Rolling Volatility ({window} days)',
        xaxis_title='Date',
        yaxis_title='Annualized Volatility',
        height=height,
        template='plotly_white',
        yaxis_tickformat='.1%'
    )
    
    return fig


def create_combined_price_volume_chart(price_data, symbol: str, height: int = 600):
    """
    Create a combined price and volume chart with subplots
    
    Args:
        price_data: DataFrame with OHLCV data
        symbol: Stock symbol for title
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if price_data is None or price_data.empty:
        return None
        
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f'{symbol.upper()} Price', 'Volume'),
        row_heights=[0.7, 0.3]
    )
    
    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=price_data.index,
        open=price_data['Open'],
        high=price_data['High'],
        low=price_data['Low'],
        close=price_data['Close'],
        name="Price"
    ), row=1, col=1)
    
    # Add volume bars (if available)
    if 'Volume' in price_data.columns:
        colors = ['green' if close >= open_price else 'red' 
                  for close, open_price in zip(price_data['Close'], price_data['Open'])]
        
        fig.add_trace(go.Bar(
            x=price_data.index,
            y=price_data['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.7
        ), row=2, col=1)
    
    fig.update_layout(
        title=f'{symbol.upper()} - Price & Volume',
        height=height,
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        showlegend=False
    )
    
    return fig


def prepare_chart_data(price_data):
    """
    Prepare and validate data for charting
    
    Args:
        price_data: Raw price data
    
    Returns:
        Processed DataFrame ready for charting
    """
    if price_data is None or price_data.empty:
        return None
    
    # Ensure we have the required columns
    required_columns = ['Open', 'High', 'Low', 'Close']
    if not all(col in price_data.columns for col in required_columns):
        return None
    
    # Remove any rows with NaN values in OHLC data
    price_data = price_data.dropna(subset=required_columns)
    
    if price_data.empty:
        return None
    
    # Ensure index is datetime
    if not isinstance(price_data.index, pd.DatetimeIndex):
        try:
            price_data.index = pd.to_datetime(price_data.index)
        except:
            return None
    
    return price_data