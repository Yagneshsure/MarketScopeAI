# tabs/finances.py
import streamlit as st
import pandas as pd
from fetchers.financials import (
    get_all_financial_data, 
    format_large_number, 
    format_percentage,
    validate_symbol
)
from components.charts import (
    create_candlestick_chart,
    create_volume_chart, 
    create_revenue_income_chart,
    create_earnings_trend_chart,
    create_combined_price_volume_chart,
    create_price_with_moving_averages,
    create_bollinger_bands_chart,
    create_rsi_chart,
    create_macd_chart,
    create_volatility_chart,
    prepare_chart_data
)


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
    
    # Get all financial data (this will now handle both symbols and company names)
    with st.spinner(f"Loading financial data for {symbol}..."):
        financial_data = get_all_financial_data(symbol, start_date, end_date)
    
    if 'error' in financial_data:
        st.error(f"❌ {financial_data['error']}")
        _show_symbol_suggestions(symbol)
        return
    
    # Show search resolution info if available
    if 'search_info' in financial_data:
        search_info = financial_data['search_info']
        if search_info.get('resolution_method') == 'company_name_search':
            st.success(f"✅ Found '{search_info['original_input']}' → {search_info['resolved_symbol']} ({search_info['company_name']})")
        elif search_info.get('resolution_method') == 'direct_symbol':
            st.info(f"✅ Using symbol: {search_info['resolved_symbol']} ({search_info['company_name']})")
    
    # Store symbol in financial_data for reference
    resolved_symbol = financial_data.get('search_info', {}).get('resolved_symbol', symbol)
    financial_data['symbol'] = resolved_symbol
    
    # Display the financial data
    _display_key_metrics(financial_data)
    _display_charts(financial_data, resolved_symbol)
    _display_technical_analysis(financial_data, resolved_symbol)
    _display_performance_metrics(financial_data)
    _display_price_alerts(financial_data, resolved_symbol)
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
        st.info("• Try using company names: 'Apple', 'Microsoft', 'Tesla'")


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
    """Display price and volume charts"""
    st.subheader("📈 Price Charts")
    
    if 'price_data' not in financial_data:
        st.info("No price data available for charting.")
        return
    
    price_data = prepare_chart_data(financial_data['price_data'])
    if price_data is None:
        st.info("Price data is not suitable for charting.")
        return
    
    # Chart type selector
    chart_type = st.selectbox(
        "Select Chart Type:",
        ["Combined Price & Volume", "Candlestick", "Price with Moving Averages", "Volume Only"],
        index=0
    )
    
    # Display selected chart
    if chart_type == "Combined Price & Volume":
        fig = create_combined_price_volume_chart(price_data, symbol)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Candlestick":
        fig = create_candlestick_chart(price_data, symbol)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Price with Moving Averages":
        # MA period selector
        col1, col2 = st.columns(2)
        with col1:
            ma_periods = st.multiselect(
                "Select Moving Average Periods:",
                [5, 10, 20, 50, 100, 200],
                default=[20, 50]
            )
        
        if ma_periods:
            fig = create_price_with_moving_averages(price_data, symbol, windows=ma_periods)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Volume Only":
        fig = create_volume_chart(price_data, symbol)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Revenue and Income Trend
    if 'revenue_income_trend' in financial_data:
        st.subheader("📈 Revenue & Net Income Trend")
        fig = create_revenue_income_chart(financial_data['revenue_income_trend'], symbol)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Earnings Charts
    earnings_data = financial_data.get('earnings_data', {})
    
    # Annual Earnings
    if 'annual_earnings' in earnings_data:
        st.subheader("📊 Annual Earnings Trend")
        fig = create_earnings_trend_chart(
            earnings_data['annual_earnings'], 
            symbol, 
            chart_type='annual'
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Quarterly Earnings
    if 'quarterly_earnings' in earnings_data:
        st.subheader("📊 Quarterly Earnings Trend")
        fig = create_earnings_trend_chart(
            earnings_data['quarterly_earnings'], 
            symbol, 
            chart_type='quarterly'
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)


def _display_technical_analysis(financial_data: dict, symbol: str):
    """Display technical analysis charts"""
    if 'price_data' not in financial_data:
        return
    
    price_data = prepare_chart_data(financial_data['price_data'])
    if price_data is None:
        return
    
    with st.expander("🔍 Technical Analysis"):
        # Technical indicator selector
        tech_tabs = st.tabs([
            "Bollinger Bands", 
            "RSI", 
            "MACD", 
            "Volatility"
        ])
        
        with tech_tabs[0]:  # Bollinger Bands
            col1, col2 = st.columns([1, 3])
            with col1:
                bb_period = st.slider("Bollinger Bands Period:", 10, 50, 20, key="bb_period")
            
            fig = create_bollinger_bands_chart(price_data, symbol, window=bb_period)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with tech_tabs[1]:  # RSI
            col1, col2 = st.columns([1, 3])
            with col1:
                rsi_period = st.slider("RSI Period:", 5, 30, 14, key="rsi_period")
            
            fig = create_rsi_chart(price_data, symbol, period=rsi_period)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with tech_tabs[2]:  # MACD
            col1, col2, col3 = st.columns(3)
            with col1:
                macd_fast = st.slider("Fast EMA:", 5, 20, 12, key="macd_fast")
            with col2:
                macd_slow = st.slider("Slow EMA:", 15, 40, 26, key="macd_slow")
            with col3:
                macd_signal = st.slider("Signal:", 3, 15, 9, key="macd_signal")
            
            fig = create_macd_chart(price_data, symbol, fast=macd_fast, slow=macd_slow, signal=macd_signal)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with tech_tabs[3]:  # Volatility
            col1, col2 = st.columns([1, 3])
            with col1:
                vol_period = st.slider("Volatility Window:", 10, 50, 20, key="vol_period")
            
            fig = create_volatility_chart(price_data, symbol, window=vol_period)
            if fig:
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
                    
                    # Format large numbers for better readability
                    formatted_data = recent_data.copy()
                    for col in formatted_data.columns:
                        if formatted_data[col].dtype in ['int64', 'float64']:
                            formatted_data[col] = formatted_data[col].apply(
                                lambda x: format_large_number(x) if pd.notna(x) else 'N/A'
                            )
                    
                    st.dataframe(formatted_data, use_container_width=True)
                    
                    # Add download button for the data
                    csv = recent_data.to_csv()
                    st.download_button(
                        label=f"Download {data_key.replace('_', ' ').title()} CSV",
                        data=csv,
                        file_name=f"{data_key}_{financial_data.get('symbol', 'unknown')}.csv",
                        mime="text/csv"
                    )
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
            if basic_info.get('employees'):
                employees = basic_info['employees']
                if employees >= 1000:
                    emp_str = f"{employees/1000:.1f}K"
                else:
                    emp_str = f"{employees:,}"
                st.write(f"**Employees:** {emp_str}")
        
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
            
            if basic_info.get('exchange'):
                st.write(f"**Exchange:** {basic_info['exchange']}")
            
            if basic_info.get('currency'):
                st.write(f"**Currency:** {basic_info['currency']}")
            
            if basic_info.get('timezone'):
                st.write(f"**Timezone:** {basic_info['timezone']}")
        
        # Business Summary
        if basic_info.get('business_summary'):
            st.write("**Business Summary:**")
            summary = basic_info['business_summary']
            # Truncate if too long
            if len(summary) > 500:
                summary = summary[:500] + "..."
            st.write(summary)
        
        # Key Statistics Summary
        if any(key in basic_info for key in ['market_cap', 'pe_ratio', 'revenue_ttm']):
            st.write("**Key Statistics:**")
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            
            with stats_col1:
                if basic_info.get('profit_margin'):
                    margin = basic_info['profit_margin']
                    st.write(f"• Profit Margin: {margin:.2%}")
                if basic_info.get('operating_margin'):
                    op_margin = basic_info['operating_margin']
                    st.write(f"• Operating Margin: {op_margin:.2%}")
            
            with stats_col2:
                if basic_info.get('return_on_equity'):
                    roe = basic_info['return_on_equity']
                    st.write(f"• ROE: {roe:.2%}")
                if basic_info.get('return_on_assets'):
                    roa = basic_info['return_on_assets']
                    st.write(f"• ROA: {roa:.2%}")
            
            with stats_col3:
                if basic_info.get('enterprise_value'):
                    ev = basic_info['enterprise_value']
                    st.write(f"• Enterprise Value: {format_large_number(ev)}")
                if basic_info.get('price_to_sales'):
                    ps = basic_info['price_to_sales']
                    st.write(f"• P/S Ratio: {ps:.2f}")


def _display_price_alerts(financial_data: dict, symbol: str):
    """Display price alert functionality"""
    current_price = financial_data.get('current_price')
    if not current_price:
        return
    
    with st.expander("🔔 Price Alerts"):
        st.write("Set price alerts for this stock:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            alert_price = st.number_input(
                "Alert Price ($):",
                min_value=0.01,
                value=float(current_price),
                step=0.01,
                format="%.2f"
            )
        
        with col2:
            alert_type = st.selectbox(
                "Alert Type:",
                ["Above", "Below"]
            )
        
        if st.button("Set Alert"):
            # This would integrate with your notification system
            st.success(f"Alert set: Notify when {symbol} goes {alert_type.lower()} ${alert_price:.2f}")
            st.info("Note: This is a demo. In a real application, this would integrate with a notification service.")


def _display_performance_metrics(financial_data: dict):
    """Display additional performance metrics"""
    basic_info = financial_data.get('basic_info', {})
    
    if not basic_info:
        return
    
    with st.expander("📊 Performance Metrics"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Profitability:**")
            if basic_info.get('gross_margin'):
                st.write(f"• Gross Margin: {basic_info['gross_margin']:.2%}")
            if basic_info.get('operating_margin'):
                st.write(f"• Operating Margin: {basic_info['operating_margin']:.2%}")
            if basic_info.get('profit_margin'):
                st.write(f"• Profit Margin: {basic_info['profit_margin']:.2%}")
        
        with col2:
            st.write("**Efficiency:**")
            if basic_info.get('return_on_equity'):
                st.write(f"• ROE: {basic_info['return_on_equity']:.2%}")
            if basic_info.get('return_on_assets'):
                st.write(f"• ROA: {basic_info['return_on_assets']:.2%}")
            if basic_info.get('asset_turnover'):
                st.write(f"• Asset Turnover: {basic_info['asset_turnover']:.2f}")
        
        with col3:
            st.write("**Valuation:**")
            if basic_info.get('price_to_sales'):
                st.write(f"• P/S Ratio: {basic_info['price_to_sales']:.2f}")
            if basic_info.get('price_to_book'):
                st.write(f"• P/B Ratio: {basic_info['price_to_book']:.2f}")
            if basic_info.get('peg_ratio'):
                st.write(f"• PEG Ratio: {basic_info['peg_ratio']:.2f}")


# Enhanced render function with additional features
def render_finances_enhanced(symbol: str, start_date=None, end_date=None):
    """
    Enhanced version of render_finances with additional features
    """
    st.header("💰 Enhanced Finance Overview")
    
    if not symbol:
        st.warning("Please select a symbol from the sidebar.")
        return
    
    # Display current symbol with last update time
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"Analyzing: **{symbol.upper()}**")
    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Get all financial data
    with st.spinner(f"Loading financial data for {symbol}..."):
        financial_data = get_all_financial_data(symbol, start_date, end_date)
    
    if 'error' in financial_data:
        st.error(f"❌ {financial_data['error']}")
        _show_symbol_suggestions(symbol)
        return
    
    # Show search resolution info if available
    if 'search_info' in financial_data:
        search_info = financial_data['search_info']
        if search_info.get('resolution_method') == 'company_name_search':
            st.success(f"✅ Found '{search_info['original_input']}' → {search_info['resolved_symbol']} ({search_info['company_name']})")
        elif search_info.get('resolution_method') == 'direct_symbol':
            st.info(f"✅ Using symbol: {search_info['resolved_symbol']} ({search_info['company_name']})")
    
    # Store symbol in financial_data for reference
    resolved_symbol = financial_data.get('search_info', {}).get('resolved_symbol', symbol)
    financial_data['symbol'] = resolved_symbol
    
    # Display all sections
    _display_key_metrics(financial_data)
    _display_charts(financial_data, resolved_symbol)
    _display_technical_analysis(financial_data, resolved_symbol)
    _display_performance_metrics(financial_data)
    _display_price_alerts(financial_data, resolved_symbol)
    _display_financial_statements(financial_data)
    _display_company_info(financial_data)
    
    # Footer with data source info
    st.markdown("---")
    st.caption("💡 Data is for educational purposes only. Not financial advice.")
    if financial_data.get('data_source'):
        st.caption(f"Data source: {financial_data['data_source']}")


# Export the main functions
__all__ = ['render_finances', 'render_finances_enhanced']