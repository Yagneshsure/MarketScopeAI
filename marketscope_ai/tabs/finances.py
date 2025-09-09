import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import requests
import json
from datetime import datetime, timedelta

def render_finances(symbol: str, start_date=None, end_date=None):
    st.header("💰 Finance Overview")
    
    if not symbol:
        st.warning("Please select a symbol from the sidebar.")
        return
    
    st.info(f"Analyzing: **{symbol.upper()}**")
    
    # Try multiple methods
    methods = [
        ("Method 1: Enhanced yfinance", fetch_with_enhanced_yfinance),
        ("Method 2: Multiple yfinance calls", fetch_with_multiple_calls),
        ("Method 3: Raw yfinance data", fetch_with_raw_data),
        ("Method 4: Alternative data sources", fetch_with_alternatives)
    ]
    
    for method_name, method_func in methods:
        try:
            st.subheader(f"🔄 Trying {method_name}")
            result = method_func(symbol, start_date, end_date)
            if result and result.get('success'):
                st.success(f"✅ {method_name} worked!")
                display_financial_data(result['data'], symbol)
                return
            else:
                st.warning(f"⚠️ {method_name} failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ {method_name} error: {str(e)}")
    
    st.error("All methods failed. The symbol might not exist or have limited data.")


def fetch_with_enhanced_yfinance(symbol: str, start_date=None, end_date=None):
    """Method 1: Enhanced yfinance with multiple fallbacks"""
    try:
        ticker = yf.Ticker(symbol)
        
        # Test basic connectivity
        hist = ticker.history(period="1d")
        if hist.empty:
            return {'success': False, 'error': 'No price data available'}
        
        data = {'price_data': hist}
        
        # Try different info methods
        info_methods = [
            ('info', lambda: ticker.info),
            ('fast_info', lambda: ticker.fast_info),
            ('get_info', lambda: ticker.get_info()),
        ]
        
        for method_name, method in info_methods:
            try:
                info_data = method()
                if info_data:
                    data[f'{method_name}_data'] = info_data
                    break
            except:
                continue
        
        # Try financial statements
        financial_methods = [
            ('financials', lambda: ticker.financials),
            ('quarterly_financials', lambda: ticker.quarterly_financials),
            ('income_stmt', lambda: ticker.income_stmt),
            ('quarterly_income_stmt', lambda: ticker.quarterly_income_stmt)
        ]
        
        for method_name, method in financial_methods:
            try:
                fin_data = method()
                if fin_data is not None and not fin_data.empty:
                    data[f'{method_name}_data'] = fin_data
            except:
                continue
        
        # Try earnings data
        try:
            earnings = ticker.earnings
            if earnings is not None and not earnings.empty:
                data['earnings_data'] = earnings
        except:
            pass
            
        try:
            quarterly_earnings = ticker.quarterly_earnings
            if quarterly_earnings is not None and not quarterly_earnings.empty:
                data['quarterly_earnings_data'] = quarterly_earnings
        except:
            pass
        
        return {'success': True, 'data': data}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


def fetch_with_multiple_calls(symbol: str, start_date=None, end_date=None):
    """Method 2: Multiple separate yfinance calls"""
    try:
        data = {}
        
        # Basic price data
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1y")
        if hist.empty:
            return {'success': False, 'error': 'No historical data'}
        data['price_data'] = hist
        
        # Manual calculation of key metrics
        current_price = hist['Close'].iloc[-1]
        
        # Try to get shares outstanding
        try:
            shares = ticker.get_shares_full(start="2020-01-01", end=None)
            if shares is not None and not shares.empty:
                shares_outstanding = shares.iloc[-1]
                data['market_cap'] = current_price * shares_outstanding
        except:
            pass
        
        # Calculate simple metrics
        data['current_price'] = current_price
        data['price_change'] = hist['Close'].iloc[-1] - hist['Close'].iloc[-2] if len(hist) > 1 else 0
        data['volume'] = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else None
        
        # Try dividends
        try:
            dividends = ticker.dividends
            if dividends is not None and not dividends.empty:
                annual_dividend = dividends.groupby(dividends.index.year).sum().iloc[-1] if len(dividends) > 0 else 0
                data['dividend_yield'] = (annual_dividend / current_price) * 100 if current_price > 0 else 0
        except:
            pass
        
        return {'success': True, 'data': data}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


def fetch_with_raw_data(symbol: str, start_date=None, end_date=None):
    """Method 3: Raw yfinance data extraction"""
    try:
        ticker = yf.Ticker(symbol)
        data = {}
        
        # Get all available data
        attributes = ['info', 'history', 'financials', 'balance_sheet', 'cashflow', 
                     'earnings', 'quarterly_earnings', 'dividends', 'splits']
        
        for attr in attributes:
            try:
                if attr == 'history':
                    value = ticker.history(period="1y")
                else:
                    value = getattr(ticker, attr, None)
                
                if value is not None:
                    if hasattr(value, 'empty') and not value.empty:
                        data[attr] = value
                    elif isinstance(value, dict) and value:
                        data[attr] = value
                    elif not hasattr(value, 'empty'):
                        data[attr] = value
            except:
                continue
        
        if not data:
            return {'success': False, 'error': 'No data attributes found'}
        
        return {'success': True, 'data': data}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


def fetch_with_alternatives(symbol: str, start_date=None, end_date=None):
    """Method 4: Alternative approaches"""
    try:
        data = {}
        
        # Try different period formats
        periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y']
        ticker = yf.Ticker(symbol)
        
        for period in periods:
            try:
                hist = ticker.history(period=period)
                if not hist.empty:
                    data['price_data'] = hist
                    data['period_used'] = period
                    break
            except:
                continue
        
        if 'price_data' not in data:
            return {'success': False, 'error': 'No price data available for any period'}
        
        # Try to download with different parameters
        try:
            # Alternative download method
            alt_data = yf.download(symbol, period="6mo", group_by='ticker', 
                                 auto_adjust=True, prepost=True, threads=True)
            if not alt_data.empty:
                data['alternative_price_data'] = alt_data
        except:
            pass
        
        return {'success': True, 'data': data}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


def display_financial_data(data, symbol):
    """Display the financial data that was successfully fetched"""
    
    # Display Key Metrics
    st.subheader("📊 Available Data")
    
    col1, col2, col3 = st.columns(3)
    
    # Price data
    if 'price_data' in data:
        hist = data['price_data']
        current_price = hist['Close'].iloc[-1]
        price_change = hist['Close'].iloc[-1] - hist['Close'].iloc[-2] if len(hist) > 1 else 0
        
        with col1:
            st.metric("Current Price", f"${current_price:.2f}", f"${price_change:.2f}")
            if 'Volume' in hist.columns:
                st.metric("Volume", f"{hist['Volume'].iloc[-1]:,.0f}")
    
    # Market cap from different sources
    market_cap = None
    if 'market_cap' in data:
        market_cap = data['market_cap']
    elif 'info_data' in data and isinstance(data['info_data'], dict):
        market_cap = data['info_data'].get('marketCap')
    elif 'fast_info_data' in data:
        market_cap = getattr(data['fast_info_data'], 'market_cap', None)
    
    if market_cap:
        with col2:
            if market_cap >= 1e12:
                cap_str = f"${market_cap/1e12:.2f}T"
            elif market_cap >= 1e9:
                cap_str = f"${market_cap/1e9:.2f}B"
            else:
                cap_str = f"${market_cap/1e6:.2f}M"
            st.metric("Market Cap", cap_str)
    
    # Dividend yield
    dividend_yield = data.get('dividend_yield')
    if dividend_yield:
        with col3:
            st.metric("Dividend Yield", f"{dividend_yield:.2f}%")
    
    # Price Chart
    if 'price_data' in data:
        st.subheader("📈 Price Chart")
        hist = data['price_data']
        
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name=symbol
        ))
        
        fig.update_layout(
            title=f'{symbol} - Price Chart ({data.get("period_used", "Recent")})',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            height=500,
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Financial statements if available
    financial_keys = ['financials_data', 'quarterly_financials_data', 'income_stmt_data']
    for key in financial_keys:
        if key in data:
            st.subheader(f"📋 {key.replace('_', ' ').title()}")
            fin_data = data[key]
            
            if not fin_data.empty:
                # Look for revenue and net income
                revenue_rows = [idx for idx in fin_data.index if 'revenue' in str(idx).lower()]
                income_rows = [idx for idx in fin_data.index if 'net income' in str(idx).lower()]
                
                if revenue_rows:
                    st.write("**Revenue:**")
                    st.dataframe(fin_data.loc[revenue_rows].head())
                    
                if income_rows:
                    st.write("**Net Income:**")
                    st.dataframe(fin_data.loc[income_rows].head())
            break
    
    # Earnings data
    if 'earnings_data' in data:
        st.subheader("📊 Annual Earnings")
        earnings = data['earnings_data']
        if not earnings.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=earnings.index,
                y=earnings['Earnings'],
                name='EPS'
            ))
            fig.update_layout(title=f'{symbol} - Annual EPS')
            st.plotly_chart(fig, use_container_width=True)
    
    if 'quarterly_earnings_data' in data:
        st.subheader("📊 Quarterly Earnings")
        q_earnings = data['quarterly_earnings_data']
        if not q_earnings.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=q_earnings.index,
                y=q_earnings['Earnings'],
                mode='lines+markers',
                name='Quarterly EPS'
            ))
            fig.update_layout(title=f'{symbol} - Quarterly EPS Trend')
            st.plotly_chart(fig, use_container_width=True)
    
    # Debug info
    with st.expander("🔍 Debug: Available Data Keys"):
        st.write("Data sources found:")
        for key, value in data.items():
            if hasattr(value, 'shape'):
                st.write(f"- {key}: DataFrame with shape {value.shape}")
            elif isinstance(value, dict):
                st.write(f"- {key}: Dictionary with {len(value)} keys")
            else:
                st.write(f"- {key}: {type(value).__name__}")