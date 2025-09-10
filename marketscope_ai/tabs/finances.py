# tabs/finances.py
import streamlit as st
from fetchers.financials import (
    get_all_financial_data, 
    format_large_number, 
    format_percentage,
    validate_symbol
)
# from components.charts import (
#     create_candlestick_chart,
#     create_volume_chart, 
#     create_revenue_income_chart,
#     create_earnings_trend_chart
# )


def render_finances(symbol: str, start_date=None, end_date=None):
    """
    Main function to render the finances tab
    """
    st.header("💰 Finance Overview")
    
    if not symbol:
        st.warning("Please select a symbol from the sidebar.")
        return
    
    # Display current symbol
    st.info(f"Analyzing: **{symbol.upper()}**")
    
    # Validate symbol and show suggestions for common mistakes
    validation = validate_symbol(symbol)
    if not validation['valid']:
        st.error(f"❌ {validation['error']}")
        _show_symbol_suggestions(symbol)
        return
    
    # Get all financial data
    with st.spinner(f"Loading financial data for {symbol}..."):
        financial_data = get_all_financial_data(symbol, start_date, end_date)
    
    if 'error' in financial_data:
        st.error(f"❌ {financial_data['error']}")
        return
    
    # Display the financial data
    _display_key_metrics(financial_data)
    _display_charts(financial_data, symbol)
    _display_financial_statements(financial_data)
    _display_company_info(financial_data)


def _show_symbol_suggestions(symbol: str):
    """Show suggestions for common symbol mistakes"""
    symbol_suggestions = {
        'lenovo': ['0992.HK', 'LNVGY'],
        'apple': ['AAPL'],
        'microsoft': ['MSFT'],
        'google': ['GOOGL', 'GOOG'],
        'tesla': ['TSLA'],
        'amazon': ['AMZN'],
        'meta': ['META'],
        'netflix': ['NFLX'],
        'nvidia': ['NVDA'],
        'disney': ['DIS']
    }
    
    if symbol.lower() in symbol_suggestions:
        st.warning(f"⚠️ '{symbol}' is not a valid ticker symbol. Try these instead:")
        for suggested_symbol in symbol_suggestions[symbol.lower()]:
            st.code(suggested_symbol)
    else:
        st.info("💡 **Common ticker formats:**")
        st.info("• US stocks: AAPL, MSFT, GOOGL")  
        st.info("• Hong Kong stocks: 0992.HK, 0700.HK")
        st.info("• Crypto: BTC-USD, ETH-USD")


def _display_key_metrics(financial_data: dict):
    """Display key financial metrics"""
    st.subheader("📊 Key Metrics")
    
    basic_info = financial_data.get('basic_info', {})
    current_price = financial_data.get('current_price')
    price_change = financial_data.get('price_change', 0)
    
    # Create metrics columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if current_price:
            st.metric(
                "Current Price", 
                f"${current_price:.2f}", 
                f"${price_change:.2f}"
            )
        
        # Market Cap
        market_cap = basic_info.get('market_cap')
        st.metric("Market Cap", format_large_number(market_cap))
    
    with col2:
        # P/E Ratio
        pe_ratio = basic_info.get('pe_ratio')
        pe_display = f"{pe_ratio:.2f}" if pe_ratio else "N/A"
        st.metric("P/E Ratio", pe_display)
        
        # EPS
        eps = basic_info.get('eps')
        eps_display = f"${eps:.2f}" if eps else "N/A"
        st.metric("EPS (TTM)", eps_display)
    
    with col3:
        # Revenue TTM
        revenue_ttm = basic_info.get('revenue_ttm')
        st.metric("Revenue (TTM)", format_large_number(revenue_ttm))
        
        # Dividend Yield
        dividend_yield = basic_info.get('dividend_yield')
        div_display = f"{dividend_yield:.2%}" if dividend_yield else "N/A"
        st.metric("Dividend Yield", div_display)
    
    with col4:
        # Net Income TTM
        net_income = basic_info.get('net_income_ttm')
        st.metric("Net Income (TTM)", format_large_number(net_income))
        
        # Beta
        beta = basic_info.get('beta')
        beta_display = f"{beta:.2f}" if beta else "N/A"
        st.metric("Beta", beta_display)
    
    # Additional metrics in expandable section
    with st.expander("📈 Additional Metrics"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            book_value = basic_info.get('book_value')
            st.metric("Book Value", f"${book_value:.2f}" if book_value else "N/A")
            
            current_ratio = basic_info.get('current_ratio')
            st.metric("Current Ratio", f"{current_ratio:.2f}" if current_ratio else "N/A")
        
        with col2:
            price_to_book = basic_info.get('price_to_book')
            st.metric("Price to Book", f"{price_to_book:.2f}" if price_to_book else "N/A")
            
            debt_to_equity = basic_info.get('debt_to_equity')
            st.metric("Debt to Equity", f"{debt_to_equity:.2f}" if debt_to_equity else "N/A")
        
        with col3:
            high_52w = basic_info.get('fifty_two_week_high')
            st.metric("52W High", f"${high_52w:.2f}" if high_52w else "N/A")
            
            low_52w = basic_info.get('fifty_two_week_low')
            st.metric("52W Low", f"${low_52w:.2f}" if low_52w else "N/A")


def _display_charts(financial_data: dict, symbol: str):
    """Display various financial charts"""
    
    # Price Chart
    if 'price_data' in financial_data:
        st.subheader("📈 Price Chart")
        price_data = financial_data['price_data']
        
        # Using simple plotly chart until you provide charts.py
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[go.Candlestick(
            x=price_data.index,
            open=price_data['Open'],
            high=price_data['High'],
            low=price_data['Low'],
            close=price_data['Close']
        )])
        
        fig.update_layout(
            title=f'{symbol} - Price Chart',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            height=400,
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Volume Chart
        if 'Volume' in price_data.columns:
            fig_vol = go.Figure()
            fig_vol.add_trace(go.Bar(
                x=price_data.index,
                y=price_data['Volume'],
                name='Volume',
                marker_color='rgba(158,202,225,0.8)'
            ))
            
            fig_vol.update_layout(
                title=f'{symbol} - Volume',
                xaxis_title='Date',
                yaxis_title='Volume',
                height=250
            )
            st.plotly_chart(fig_vol, use_container_width=True)
    
    # Revenue and Income Trend
    if 'revenue_income_trend' in financial_data:
        st.subheader("📈 Revenue & Net Income Trend")
        trend_data = financial_data['revenue_income_trend']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=trend_data['Year'], 
            y=trend_data['Revenue'], 
            name='Revenue',
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            x=trend_data['Year'], 
            y=trend_data['Net Income'], 
            name='Net Income',
            marker_color='lightgreen'
        ))
        
        fig.update_layout(
            barmode='group',
            title=f'{symbol} - Revenue vs Net Income',
            xaxis_title='Year',
            yaxis_title='Amount ($)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Earnings Trend
    earnings_data = financial_data.get('earnings_data', {})
    
    # Annual Earnings
    if 'annual_earnings' in earnings_data:
        st.subheader("📊 Annual Earnings Trend")
        annual_earnings = earnings_data['annual_earnings']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=annual_earnings.index,
            y=annual_earnings['Earnings'],
            name='Annual EPS',
            marker_color='lightgreen'
        ))
        fig.update_layout(
            title=f'{symbol} - Annual EPS',
            xaxis_title='Year',
            yaxis_title='EPS ($)',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Quarterly Earnings
    if 'quarterly_earnings' in earnings_data:
        st.subheader("📊 Quarterly Earnings Trend")
        quarterly_earnings = earnings_data['quarterly_earnings']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=quarterly_earnings.index,
            y=quarterly_earnings['Earnings'],
            mode='lines+markers',
            name='Quarterly EPS',
            line=dict(color='orange', width=2),
            marker=dict(size=6)
        ))
        fig.update_layout(
            title=f'{symbol} - Quarterly EPS Trend',
            xaxis_title='Quarter',
            yaxis_title='EPS ($)',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)


def _display_financial_statements(financial_data: dict):
    """Display financial statements data"""
    financial_statements = financial_data.get('financial_statements', {})
    
    if not financial_statements:
        return
    
    st.subheader("📋 Financial Statements")
    
    # Create tabs for different financial statements
    tabs = []
    tab_data = []
    
    if 'annual_financials' in financial_statements:
        tabs.append("📊 Income Statement")
        tab_data.append(('annual_financials', financial_statements['annual_financials']))
    
    if 'balance_sheet' in financial_statements:
        tabs.append("⚖️ Balance Sheet") 
        tab_data.append(('balance_sheet', financial_statements['balance_sheet']))
    
    if 'cashflow' in financial_statements:
        tabs.append("💰 Cash Flow")
        tab_data.append(('cashflow', financial_statements['cashflow']))
    
    if tabs:
        financial_tabs = st.tabs(tabs)
        
        for i, (tab_name, (data_key, data)) in enumerate(zip(financial_tabs, tab_data)):
            with tab_name:
                if not data.empty:
                    # Show recent years data (limit to 5 years)
                    recent_data = data.iloc[:, :5] if data.shape[1] > 5 else data
                    st.dataframe(recent_data, use_container_width=True)
                else:
                    st.info("No data available")


def _display_company_info(financial_data: dict):
    """Display company information"""
    basic_info = financial_data.get('basic_info', {})
    
    if not basic_info:
        return
    
    with st.expander("🏢 Company Information"):
        col1, col2 = st.columns(2)
        
        with col1:
            if basic_info.get('company_name'):
                st.write(f"**Company:** {basic_info['company_name']}")
            if basic_info.get('sector'):
                st.write(f"**Sector:** {basic_info['sector']}")
            if basic_info.get('industry'):
                st.write(f"**Industry:** {basic_info['industry']}")
            if basic_info.get('country'):
                st.write(f"**Country:** {basic_info['country']}")
            if basic_info.get('website'):
                st.write(f"**Website:** {basic_info['website']}")
        
        with col2:
            if basic_info.get('average_volume'):
                avg_vol = basic_info['average_volume']
                if avg_vol >= 1e6:
                    vol_str = f"{avg_vol/1e6:.1f}M"
                elif avg_vol >= 1e3:
                    vol_str = f"{avg_vol/1e3:.1f}K"
                else:
                    vol_str = f"{avg_vol:.0f}"
                st.write(f"**Average Volume:** {vol_str}")
        
        # Business Summary
        if basic_info.get('business_summary'):
            st.write("**Business Summary:**")
            st.write(basic_info['business_summary'][:500] + "..." if len(basic_info['business_summary']) > 500 else basic_info['business_summary'])


# TODO: Remove this section once you provide charts.py
# This is temporary - using basic plotly charts
# Replace with your chart components once you share charts.py
def _create_temp_chart_placeholder():
    """
    Temporary placeholder for charts until charts.py is provided
    This will be replaced with actual chart components
    """
    pass