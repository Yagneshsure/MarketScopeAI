# =============================================
# IMPORTS
# =============================================
import streamlit as st

# Custom fetchers + components
from components.sidebar import render_sidebar
from tabs.overview import render_overview
from tabs.finances import render_finances
from tabs.news import render_news_sentiment
# from tabs.llm_summary import render_llm_summary
# from tabs.ask_ai import render_ask_ai


# =============================================
# MAIN APP
# =============================================
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
                st.rerun()
        with col2:
            if st.button("💰 Crypto", use_container_width=True):
                st.session_state.selected_market = "Crypto"
                st.rerun()
        with col3:
            if st.button("📊 ETFs", use_container_width=True):
                st.session_state.selected_market = "ETFs"
                st.rerun()

        col4, col5 = st.columns(2)
        with col4:
            if st.button("⚒️ Commodities", use_container_width=True):
                st.session_state.selected_market = "Commodities"
                st.rerun()
        with col5:
            if st.button("🏦 Mutual Funds", use_container_width=True):
                st.session_state.selected_market = "Mutual Funds"
                st.rerun()

    else:
        # Add back button
        if st.sidebar.button("← Back to Market Selection"):
            st.session_state.selected_market = None
            st.rerun()
            
        # Sidebar (modularized)
        sidebar_config = render_sidebar(st.session_state.selected_market)

        selected_symbol = sidebar_config["symbol"]
        currency = sidebar_config["currency"]
        interval = sidebar_config["interval"]
        start_date = sidebar_config["start_date"]
        end_date = sidebar_config["end_date"]

        # Only show tabs if a symbol is selected
        if selected_symbol:
            # Tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["📊 Overview", "💰 Finances", "📰 News & Sentiment", "🧠 LLM Summary", "💬 Ask AI"]
            )

            with tab1:
                render_overview(selected_symbol, currency, interval, start_date, end_date)

            with tab2:
                render_finances(selected_symbol, start_date, end_date)

            with tab3:
                render_news_sentiment(selected_symbol)

            # with tab4:
            #     render_llm_summary(selected_symbol)

            # with tab5:
            #     render_ask_ai(selected_symbol)
        else:
            st.info("Please select a symbol from the sidebar to view data.")


# =============================================
# ENTRY POINT
# =============================================
if __name__ == "__main__":
    main()