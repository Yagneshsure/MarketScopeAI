# import streamlit as st
# import pandas as pd
# import datetime
# import sys
# import os

# # Add custom folders to sys.path
# sys.path.append(os.path.join(os.path.dirname(__file__), "fetchers"))
# sys.path.append(os.path.join(os.path.dirname(__file__), "components"))

# # Import fetchers and chart components
# from fetchers.stocks import fetch_stock_history, fetch_company_info
# from components.charts import (
#     plot_line_price, plot_candlestick, plot_volume_histogram, plot_price_with_ma,
#     plot_ma_crossover, plot_bollinger_bands, plot_rsi, plot_macd,
#     plot_volatility, plot_drawdown
# )

# # Streamlit page setup
# st.set_page_config(page_title="MarketScopeAI", layout="wide")
# st.title("📊 MarketScopeAI Dashboard")

# # --------------------------------
# # Sidebar Controls
# # --------------------------------
# st.sidebar.header("📌 Select Symbol")
# symbol = st.sidebar.text_input("Stock Symbol (e.g. AAPL, TSLA)", value="AAPL")

# st.sidebar.header("⏱️ Time Settings")
# interval = st.sidebar.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
# period = st.sidebar.selectbox("Period (fallback)", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=2)

# st.sidebar.header("📅 Custom Dates")
# today = datetime.date.today()
# default_start = today - datetime.timedelta(days=180)
# start_date = st.sidebar.date_input("Start Date", value=default_start, max_value=today)
# end_date = st.sidebar.date_input("End Date", value=today, min_value=start_date, max_value=today)

# # --------------------------------
# # Fetch data once
# # --------------------------------
# comp_info = fetch_company_info(symbol.upper())
# data = fetch_stock_history(symbol.upper(), interval=interval, period=period, start=start_date, end=end_date)

# # --------------------------------
# # Clickable Tabs: Overview | Finances
# # --------------------------------
# tab1, tab2 = st.tabs(["🔍 Overview", "💰 Finances"])

# # ----------------------------
# # Tab 1: Overview
# # ----------------------------
# with tab1:
#     st.header("🔍 Company Overview")

#     if comp_info:
#         st.subheader(f"{symbol.upper()} — {comp_info.get('longName', '')}")
#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown(f"**Sector:** {comp_info.get('sector', '-')}")
#             st.markdown(f"**Industry:** {comp_info.get('industry', '-')}")
#             st.markdown(f"**Exchange:** {comp_info.get('exchange', '-')}")
#             website = comp_info.get('website', '-')
#             if website and website != "-":
#                 st.markdown(f"**Website:** [{website}]({website})")
#             else:
#                 st.markdown("**Website:** -")

#         with col2:
#             market_cap = comp_info.get('marketCap', 0)
#             current_price = comp_info.get('currentPrice', '-')
#             st.markdown(f"**Market Cap:** ${market_cap:,}" if market_cap else "**Market Cap:** -")
#             st.markdown(f"**Current Price:** ${current_price}")
#             st.markdown(f"**Beta:** {comp_info.get('beta', '-')}")
#             st.markdown(f"**PE Ratio:** {comp_info.get('trailingPE', '-')}")

#         st.markdown("---")
#         st.write(f"**Description:**\n{comp_info.get('longBusinessSummary', '-')}")
#     else:
#         st.warning("⚠️ Company information not available.")

#     st.markdown("---")
#     st.subheader("📈 Historical Price Chart")

#     if not data.empty:
#         st.plotly_chart(plot_line_price(data), use_container_width=True)
#     else:
#         st.warning("⚠️ No price history available for this date range or symbol.")

# # ----------------------------
# # Tab 2: Finances
# # ----------------------------
# with tab2:
#     st.header("💰 Technical Analysis & Financial Charts")
#     st.markdown(f"### Stock: {symbol.upper()}")

#     if not data.empty:
#         st.dataframe(data.tail(10), use_container_width=True)

#         with st.expander("📊 Candlestick + Volume", expanded=True):
#             st.plotly_chart(plot_candlestick(data), use_container_width=True, key="candlestick_main")
#             st.plotly_chart(plot_volume_histogram(data), use_container_width=True, key="volume_main")

#         with st.expander("📈 Price + Moving Averages + RSI", expanded=False):
#             st.plotly_chart(plot_price_with_ma(data), use_container_width=True, key="price_ma_main")
#             st.plotly_chart(plot_rsi(data), use_container_width=True, key="rsi_main")

#         with st.expander("📉 Bollinger Bands + MACD", expanded=False):
#             st.plotly_chart(plot_bollinger_bands(data), use_container_width=True, key="bollinger_main")
#             st.plotly_chart(plot_macd(data), use_container_width=True, key="macd_main")

#         with st.expander("📉 Drawdown", expanded=False):
#             st.plotly_chart(plot_drawdown(data), use_container_width=True, key="drawdown_main")

#         with st.expander("⚡ Volatility", expanded=False):
#             st.plotly_chart(plot_volatility(data), use_container_width=True, key="volatility_main")
#     else:
#         st.warning("⚠️ No stock data available for selected input.")


import streamlit as st
import pandas as pd
import datetime
import sys
import os

from dotenv import load_dotenv
import os
import openai

# Add custom folders to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "fetchers"))
sys.path.append(os.path.join(os.path.dirname(__file__), "components"))

# Import fetchers and chart components
from fetchers.stocks import fetch_stock_history, fetch_company_info, search_symbol
from components.charts import (
    plot_line_price, plot_candlestick, plot_volume_histogram, plot_price_with_ma,
    plot_ma_crossover, plot_bollinger_bands, plot_rsi, plot_macd,
    plot_volatility, plot_drawdown
)
from components.ask_ai import ask_ai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit page setup
st.set_page_config(page_title="MarketScopeAI", layout="wide")
st.title("📊 MarketScopeAI Dashboard")

# --------------------------------
# Sidebar Controls
# --------------------------------
st.sidebar.header("📌 Select Stock")
input_query = st.sidebar.text_input("Enter Company Name or Symbol", value="Apple")

st.sidebar.header("⏱️ Time Settings")
interval = st.sidebar.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
period = st.sidebar.selectbox("Period (fallback)", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=2)

st.sidebar.header("📅 Custom Dates")
today = datetime.date.today()
default_start = today - datetime.timedelta(days=180)
start_date = st.sidebar.date_input("Start Date", value=default_start, max_value=today)
end_date = st.sidebar.date_input("End Date", value=today, min_value=start_date, max_value=today)

# --------------------------------
# Resolve symbol
# --------------------------------
symbol = search_symbol(input_query)

# --------------------------------
# Fetch data once
# --------------------------------
comp_info = fetch_company_info(symbol)
data = fetch_stock_history(symbol, interval=interval, period=period, start=start_date, end=end_date)

# --------------------------------
# Clickable Tabs: Overview | Finances
# --------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "📈 Finances", 
    "📰 News & Sentiment", 
    "🧠 LLM Summary", 
    "💬 Ask AI"
])

# --------------------------------
###### === Tab 1: Overview === #####
# --------------------------------

with tab1:
    st.markdown("## 🔍 Company Overview")

    if comp_info:
        display_symbol = comp_info.get("symbol", symbol)
        company_name = comp_info.get("longName", "")
        current_price = comp_info.get("currentPrice", "-")

        st.subheader(f"{display_symbol} — {company_name}")

        # 🔵 Compact Current Price Box - Modified
        st.markdown(
            f"""
            <div style='
                background-color: #1f77b4;
                padding: 8px 12px;
                border-radius: 8px;
                margin: 10px 0 20px 0;
                text-align: center;
                max-width: 300px;
            '>
                <h4 style='color: white; margin: 5px 0;'>Current Price</h4>
                <h3 style='color: white; font-size: 1.8em; margin: 5px 0;'>${current_price}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        sector = comp_info.get("sector", "-")
        industry = comp_info.get("industry", "-")
        exchange = comp_info.get("exchange", "-")
        market_cap = comp_info.get("marketCap", None)
        beta = comp_info.get("beta", "-")
        pe_ratio = comp_info.get("trailingPE", "-")
        website = comp_info.get("website", "-")
        description = comp_info.get("longBusinessSummary", "-")

        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**Sector:** {sector}")
        col1.markdown(f"**Industry:** {industry}")
        col1.markdown(f"**Exchange:** {exchange}")

        col2.markdown(f"**Market Cap:** ${market_cap:,}" if market_cap else "**Market Cap:** -")
        col2.markdown(f"**Beta:** {beta}")
        col2.markdown(f"**P/E Ratio:** {pe_ratio}")

        col3.markdown(f"**Website:** [{website}]({website})" if website != "-" else "**Website:** -")

        st.markdown("### 📘 Company Description")
        st.write(description)

    else:
        st.warning("⚠️ No company data found.")

    st.markdown("---")
    st.subheader("📈 Historical Price Chart")

    if not data.empty:
        st.plotly_chart(plot_line_price(data), use_container_width=True)
    else:
        st.warning("⚠️ No price history available for this date range or symbol.")


# --------------------------------
##### ===Tab 2: Finances === #####
# --------------------------------

with tab2:
    st.header("💰 Technical Analysis & Financial Charts")
    st.markdown(f"### Stock: {symbol.upper()}")

    if not data.empty:
        st.dataframe(data.tail(10), use_container_width=True)

        with st.expander("📊 Candlestick + Volume", expanded=True):
            st.plotly_chart(plot_candlestick(data), use_container_width=True, key="candlestick_main")
            st.plotly_chart(plot_volume_histogram(data), use_container_width=True, key="volume_main")

        with st.expander("📈 Price + Moving Averages + RSI", expanded=False):
            st.plotly_chart(plot_price_with_ma(data), use_container_width=True, key="price_ma_main")
            st.plotly_chart(plot_rsi(data), use_container_width=True, key="rsi_main")

        with st.expander("📉 Bollinger Bands + MACD", expanded=False):
            st.plotly_chart(plot_bollinger_bands(data), use_container_width=True, key="bollinger_main")
            st.plotly_chart(plot_macd(data), use_container_width=True, key="macd_main")

        with st.expander("📉 Drawdown", expanded=False):
            st.plotly_chart(plot_drawdown(data), use_container_width=True, key="drawdown_main")

        with st.expander("⚡ Volatility", expanded=False):
            st.plotly_chart(plot_volatility(data), use_container_width=True, key="volatility_main")
    else:
        st.warning("⚠️ No stock data available for selected input.")


# --------------------------------
##### === NEWS & SENTIMENT TAB === ####
# --------------------------------

with tab3:
    st.markdown("## 📰 News & Sentiment")
    st.info("This section will include latest news headlines and sentiment analysis (Coming soon).")

##### === LLM SUMMARY TAB === #####
with tab4:
    st.markdown("## 🧠 LLM Generated Summary")
    st.info("This section will provide a concise summary of the company using LLM. (Coming soon).")


# --------------------------------
##### === ASK AI TAB === #####
# --------------------------------

with tab5:
    st.markdown("## 💬 Ask AI about this Company")

    user_query = st.text_input("What would you like to know about this company or its stock performance?", key="ask_ai_input")

    if user_query:
        with st.spinner("Analyzing..."):
            response = ask_ai(user_query)  # Uses the Groq-powered ask_ai function
            if response.startswith("❌"):
                st.error(response)
            else:
                st.markdown("**📊 AI Response:**")
                st.markdown(response)
    else:
        st.info("Enter a question to get insights from the AI assistant.")