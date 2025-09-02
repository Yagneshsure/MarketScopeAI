# =============================================
### IMPORTING REQUIRED LIBRARIES ###
# ============================================

import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
import streamlit as st
import datetime

# Custom fetchers + components
from fetchers.stocks import get_stock_info
from components.charts import (
    plot_line_price, plot_candlestick, plot_volume_histogram,
    plot_price_with_ma, plot_ma_crossover, plot_bollinger_bands,
    plot_rsi, plot_macd, plot_volatility, plot_drawdown
)
from components.helpers import _apply_dark_layout, _fmt_num
from fetchers.financials import get_financials, get_eps


# ======================================
# MAIN APP
# ======================================
def main():
    st.set_page_config(page_title="MarketScopeAI", layout="wide")

    # Inject CSS for metric cards
    st.markdown(
        """
        <style>
        .metric-card {
            padding:15px;
            background-color:#1e1e1e;
            border-radius:12px;
            text-align:center;
            color:white;
            font-size:18px;
            margin-bottom:10px;
            border:1px solid #2b8be6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # First Page: Market Type Selection
    if "selected_market" not in st.session_state:
        st.session_state.selected_market = None

    if not st.session_state.selected_market:
        st.title("📊 MarketScopeAI Navigation")
        st.subheader("Choose Market Type")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📈 Stocks", use_container_width=True):
                st.session_state.selected_market = "Stocks"
        with col2:
            if st.button("💰 Crypto", use_container_width=True):
                st.session_state.selected_market = "Crypto"
        with col3:
            if st.button("📊 ETFs", use_container_width=True):
                st.session_state.selected_market = "ETFs"

        col4, col5 = st.columns(2)
        with col4:
            if st.button("⚒️ Commodities", use_container_width=True):
                st.session_state.selected_market = "Commodities"
        with col5:
            if st.button("🏦 Mutual Funds", use_container_width=True):
                st.session_state.selected_market = "Mutual Funds"

    else:
        # Sidebar filters
        st.sidebar.title("⚙️ Filters")

        placeholder_text = f"Enter {st.session_state.selected_market} symbol or name..."
        user_symbol = st.sidebar.text_input("", placeholder=placeholder_text)

        if st.sidebar.button("🔍 Search"):
            if user_symbol:
                st.session_state.search_symbol = user_symbol
            else:
                st.sidebar.warning("Please enter a symbol")

        currency = st.sidebar.selectbox(
            "Choose Currency", ["USD", "INR", "EUR", "GBP", "AED", "RUB"]
        )

        if st.session_state.selected_market == "Crypto":
            intervals = ["1y", "6mo", "3mo", "1mo", "1d", "1h", "30m", "15m", "5m", "1m"]
            default_interval = intervals.index("1h")
        else:
            intervals = ["1y", "6mo", "3mo", "1mo", "1d"]
            default_interval = intervals.index("1d")
        interval = st.sidebar.selectbox("Choose Interval", intervals, index=default_interval)

        st.sidebar.write("📅 Select Date Range")
        start_date = st.sidebar.date_input("From Date", datetime.date(2023, 1, 1))
        end_date = st.sidebar.date_input("To Date", datetime.date.today())

        if st.sidebar.button("⬅️ Go Back"):
            st.session_state.selected_market = None
            st.session_state.search_symbol = None
            st.rerun()

        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Overview", "💰 Finances", "📰 News & Sentiment", "🧠 LLM Summary", "💬 Ask AI"]
        )

        selected_symbol = st.session_state.get("search_symbol", None)

# =================================
# TAB 1: Overview
# =================================
        with tab1:
            st.header("📊 Overview")

            if selected_symbol:
                stock_info = get_stock_info(selected_symbol, target_currency=currency)

                if "error" in stock_info:
                    st.error(stock_info["error"])
                else:
                    st.subheader(f"{stock_info['ticker']} — {stock_info['name']}")

                    # Price box
                    st.markdown(
                        f"""
                        <div style="padding:15px; background-color:#2b8be6; border-radius:10px; 
                                    text-align:center; color:white; font-size:20px;">
                        <b>Current Price</b><br>
                        {stock_info['native_currency']} {stock_info['current_price_native']} 
                        / {currency} {stock_info[f'current_price_{currency}']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Company details
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Sector:** {stock_info['sector']}")
                        st.markdown(f"**Industry:** {stock_info['industry']}")
                        st.markdown(f"**Exchange:** {stock_info['exchange']}")
                    with col2:
                        st.markdown(f"**Market Cap:** {stock_info['market_cap']}")
                        st.markdown(f"**Beta:** {stock_info['beta']}")
                        st.markdown(f"**P/E Ratio:** {stock_info['pe_ratio']}")
                        st.markdown(f"**Website:** [{stock_info['website']}]({stock_info['website']})")

                    # Description
                    st.subheader("🏢 Company Description")
                    st.write(stock_info['description'])

                    # Historical chart
                    st.subheader("📈 Price Charts")
                    stock = yf.Ticker(stock_info["ticker"])
                    hist = stock.history(start=start_date, end=end_date, interval=interval)

                    if not hist.empty:
                        hist = hist.reset_index()
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=hist["Date"],
                            y=hist["Close"],
                            mode="lines+markers",
                            name="Closing Price",
                            line=dict(color="#00FFFF", width=2.5),
                            marker=dict(size=4, color="#2b8be6"),
                            hovertemplate="Date: %{x}<br>Price: %{y:.2f}<extra></extra>"
                        ))
                        _apply_dark_layout(fig, f"{stock_info['ticker']} Closing Price Over Time")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No historical data available for this stock.")

            else:
                st.info("Please enter a symbol and click Search.")

# ==================================
# TAB 2: Finances
# ==================================
        with tab2:
            st.header("💰 Finance Overview")

            if selected_symbol:
                try:
                    ticker = yf.Ticker(selected_symbol)
                    info = ticker.info

                    # Metrics
                    st.subheader("📊 Key Metrics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"<div class='metric-card'><b>Market Cap</b><br>${_fmt_num(info.get('marketCap'))}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='metric-card'><b>P/E Ratio</b><br>{_fmt_num(info.get('forwardPE'))}</div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<div class='metric-card'><b>EPS (TTM)</b><br>{_fmt_num(info.get('trailingEps'))}</div>", unsafe_allow_html=True)
                        div_yield = info.get("dividendYield")
                        st.markdown(
                            f"<div class='metric-card'><b>Dividend Yield</b><br>{div_yield*100:.2f}%</div>"
                            if isinstance(div_yield, (float, int)) else
                            "<div class='metric-card'><b>Dividend Yield</b><br>N/A</div>",
                            unsafe_allow_html=True
                        )
                    with col3:
                        st.markdown(f"<div class='metric-card'><b>Revenue (TTM)</b><br>${_fmt_num(info.get('totalRevenue'))}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='metric-card'><b>Net Income (TTM)</b><br>${_fmt_num(info.get('netIncomeToCommon'))}</div>", unsafe_allow_html=True)

                    # Revenue & Net Income Trend
                    st.subheader("📈 Revenue & Net Income Trend")
                    fin_df = get_financials(selected_symbol)
                    if fin_df is not None and not fin_df.empty:
                        fig_fin = px.bar(fin_df, x="Year", y=["Revenue", "Net Income"], barmode="group")
                        _apply_dark_layout(fig_fin, "Annual Revenue vs Net Income")
                        st.plotly_chart(fig_fin, use_container_width=True)
                    else:
                        st.warning("Financial statement data not available.")

                    # # EPS Trend
                    # st.subheader("📈 EPS Trend")
                    # eps_df = get_eps(selected_symbol)
                    # if eps_df is not None and not eps_df.empty:
                    #     fig_eps = px.line(eps_df, x="Quarter", y="EPS", markers=True)
                    #     _apply_dark_layout(fig_eps, "Quarterly EPS")
                    #     st.plotly_chart(fig_eps, use_container_width=True)
                    # else:
                    #     st.info("Earnings data not available.")

                    # Technical Charts
                    st.subheader("📉 Technical Charts")
                    hist_tc = ticker.history(start=start_date, end=end_date, interval="1d")
                    if hist_tc is None or hist_tc.empty:
                        st.warning("No historical OHLCV available to render technical charts.")
                    else:
                        data = hist_tc.reset_index()
                        chart_options = [
                            "Line Price", "Candlestick", "Volume Histogram", "Price with Moving Averages",
                            "MA Crossover", "Bollinger Bands", "RSI", "MACD", "Volatility", "Drawdown"
                        ]
                        selected_charts = st.multiselect("Select charts to display:", chart_options, default=["Line Price", "Candlestick", "RSI"])

                        chart_map = {
                            "Line Price": plot_line_price,
                            "Candlestick": plot_candlestick,
                            "Volume Histogram": plot_volume_histogram,
                            "Price with Moving Averages": plot_price_with_ma,
                            "MA Crossover": plot_ma_crossover,
                            "Bollinger Bands": plot_bollinger_bands,
                            "RSI": plot_rsi,
                            "MACD": plot_macd,
                            "Volatility": plot_volatility,
                            "Drawdown": plot_drawdown,
                        }

                        for chart_name in selected_charts:
                            fig = chart_map[chart_name](data)
                            _apply_dark_layout(fig, chart_name)
                            st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    st.error(f"Error loading financials: {e}")
            else:
                st.info("Enter a stock symbol above to see financial data.")

        # ============================
        # TAB 3: News & Sentiment
        # ============================
        with tab3:
            st.header("📰 News & Sentiment")
            st.write("🔧 Coming soon: live financial news + sentiment analysis")

        # ============================
        # TAB 4: LLM Summary
        # ============================
        with tab4:
            st.header("🧠 LLM Summary")
            st.write("🤖 AI-generated company summaries will appear here.")

        # ============================
        # TAB 5: Ask AI
        # ============================
        with tab5:
            st.header("💬 Ask AI")
            query = st.text_input("Ask a question about this asset")
            if st.button("Submit Question"):
                st.write(f"🤖 AI Response to: {query} (placeholder)")


if __name__ == "__main__":
    main()
