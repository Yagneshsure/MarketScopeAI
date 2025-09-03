import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from fetchers.stocks import get_stock_info
from components.helpers import _apply_dark_layout

def render_overview(selected_symbol, currency, interval, start_date, end_date):
    """Render the Overview tab with stock/crypto/ETF info and charts."""

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
