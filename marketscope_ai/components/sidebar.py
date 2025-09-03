# components/sidebar.py

import streamlit as st
import datetime

def render_sidebar(selected_market):
    """Render sidebar filters and return user selections."""

    st.sidebar.title("⚙️ Filters")

    placeholder_text = f"Enter {selected_market} symbol or name..."
    user_symbol = st.sidebar.text_input("", placeholder=placeholder_text)

    if st.sidebar.button("🔍 Search"):
        if user_symbol:
            st.session_state.search_symbol = user_symbol
        else:
            st.sidebar.warning("Please enter a symbol")

    currency = st.sidebar.selectbox(
        "Choose Currency", ["USD", "INR", "EUR", "GBP", "AED", "RUB"]
    )

    if selected_market == "Crypto":
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

    return {
        "symbol": st.session_state.get("search_symbol", None),
        "currency": currency,
        "interval": interval,
        "start_date": start_date,
        "end_date": end_date,
    }
