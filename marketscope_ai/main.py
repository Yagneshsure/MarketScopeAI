import streamlit as st
import datetime

# --- Main app ---
def main():
    st.set_page_config(page_title="MarketScopeAI", layout="wide")

    # First Page: Market Type Selection
    if "selected_market" not in st.session_state:
        st.session_state.selected_market = None

    if not st.session_state.selected_market:
        st.title("📌 MarketScopeAI Navigation")
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
        # Sidebar
        st.sidebar.title("⚙️ Filters")

        # 1. Enter Symbol with Watermark + Search Button
        placeholder_text = f"Enter {st.session_state.selected_market} symbol or name..."
        user_symbol = st.sidebar.text_input("", placeholder=placeholder_text)
        if st.sidebar.button("🔍 Search"):
            st.sidebar.success(f"Searching for: {user_symbol}")

        # 2. Currency Selection
        currency = st.sidebar.selectbox(
            "Choose Currency", ["USD", "INR", "POUND", "DIRHAM", "RUB"]
        )

        # 3. Interval Selection
        if st.session_state.selected_market == "Crypto":
            intervals = ["1y", "6mo", "3mo", "1mo", "1d", "1h", "30m", "15m", "5m", "1m"]
            default_interval = intervals.index("1h")  # default = hourly
        else:
            intervals = ["1y", "6mo", "3mo", "1mo", "1d"]
            default_interval = intervals.index("1d")  # default = daily
        interval = st.sidebar.selectbox("Choose Interval", intervals, index=default_interval)

        # 4. Date Selection
        st.sidebar.write("📅 Select Date Range")
        start_date = st.sidebar.date_input("From Date", datetime.date(2023, 1, 1))
        end_date = st.sidebar.date_input("To Date", datetime.date.today())

        # 5. Calendar Picker
        calendar_date = st.sidebar.date_input("Pick a Date")

        # Go Back Option
        if st.sidebar.button("⬅️ Go Back"):
            st.session_state.selected_market = None
            st.rerun()

        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Overview", "📈 Finances", "📰 News & Sentiment", "🧠 LLM Summary", "💬 Ask AI"]
        )

        with tab1:
            st.header("📊 Overview")
            st.write(f"Showing overview for {user_symbol} in {currency}, interval: {interval}")

        with tab2:
            st.header("📈 Finances")
            st.write("Financial data will appear here...")

        with tab3:
            st.header("📰 News & Sentiment")
            st.write("News and sentiment data will appear here...")

        with tab4:
            st.header("🧠 LLM Summary")
            st.write("AI-generated summary will appear here...")

        with tab5:
            st.header("💬 Ask AI")
            query = st.text_input("Ask a question about this asset")
            if st.button("Submit Question"):
                st.write(f"🤖 AI Response to: {query} (placeholder)")


if __name__ == "__main__":
    main()
