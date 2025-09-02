# import streamlit as st
# import datetime
# from fetchers.stocks import get_stock_info


# # --- Main app ---
# def main():
#     st.set_page_config(page_title="MarketScopeAI", layout="wide")

#     # First Page: Market Type Selection
#     if "selected_market" not in st.session_state:
#         st.session_state.selected_market = None

#     if not st.session_state.selected_market:
#         st.title("📌 MarketScopeAI Navigation")
#         st.subheader("Choose Market Type")

#         col1, col2, col3 = st.columns(3)
#         with col1:
#             if st.button("📈 Stocks", use_container_width=True):
#                 st.session_state.selected_market = "Stocks"
#         with col2:
#             if st.button("💰 Crypto", use_container_width=True):
#                 st.session_state.selected_market = "Crypto"
#         with col3:
#             if st.button("📊 ETFs", use_container_width=True):
#                 st.session_state.selected_market = "ETFs"

#         col4, col5 = st.columns(2)
#         with col4:
#             if st.button("⚒️ Commodities", use_container_width=True):
#                 st.session_state.selected_market = "Commodities"
#         with col5:
#             if st.button("🏦 Mutual Funds", use_container_width=True):
#                 st.session_state.selected_market = "Mutual Funds"

#     else:
#         # Sidebar
#         st.sidebar.title("⚙️ Filters")

#         # 1. Enter Symbol with Watermark + Search Button
#         placeholder_text = f"Enter {st.session_state.selected_market} symbol or name..."
#         user_symbol = st.sidebar.text_input("", placeholder=placeholder_text)

#         if st.sidebar.button("🔍 Search"):
#             if user_symbol:
#                 st.session_state.search_symbol = user_symbol
#             else:
#                 st.sidebar.warning("Please enter a symbol")

#         # 2. Currency Selection
#         currency = st.sidebar.selectbox(
#             "Choose Currency", ["USD", "INR", "EUR", "GBP", "AED", "RUB"]
#         )

#         # 3. Interval Selection
#         if st.session_state.selected_market == "Crypto":
#             intervals = ["1y", "6mo", "3mo", "1mo", "1d", "1h", "30m", "15m", "5m", "1m"]
#             default_interval = intervals.index("1h")  # default = hourly
#         else:
#             intervals = ["1y", "6mo", "3mo", "1mo", "1d"]
#             default_interval = intervals.index("1d")  # default = daily
#         interval = st.sidebar.selectbox("Choose Interval", intervals, index=default_interval)

#         # 4. Date Selection
#         st.sidebar.write("📅 Select Date Range")
#         start_date = st.sidebar.date_input("From Date", datetime.date(2023, 1, 1))
#         end_date = st.sidebar.date_input("To Date", datetime.date.today())

#         # 5. Calendar Picker
#         calendar_date = st.sidebar.date_input("Pick a Date")

#         # Go Back Option
#         if st.sidebar.button("⬅️ Go Back"):
#             st.session_state.selected_market = None
#             st.session_state.search_symbol = None
#             st.rerun()

#         # Tabs
#         tab1, tab2, tab3, tab4, tab5 = st.tabs(
#             ["📊 Overview", "📈 Finances", "📰 News & Sentiment", "🧠 LLM Summary", "💬 Ask AI"]
#         )

#         # Check if user has searched for a symbol
#         selected_symbol = st.session_state.get("search_symbol", None)

#         with tab1:
#             st.header("📊 Overview")

#             if selected_symbol:
#                 stock_info = get_stock_info(selected_symbol, target_currency=currency)

#                 if "error" in stock_info:
#                     st.error(stock_info["error"])
#                 else:
#                      # --- Company Name + Ticker ---
#                     st.subheader(f"{stock_info['ticker']} — {stock_info['name']}")

#                     # --- Price Box ---
#                     col_price = st.container()
#                     with col_price:
#                         st.markdown(
#                             f"""
#                             <div style="padding:15px; background-color:#2b8be6; border-radius:10px; 
#                                         text-align:center; color:white; font-size:20px;">
#                              <b>Current Price</b><br>
#                             {stock_info['native_currency']} {stock_info['current_price_native']} 
#                             / {currency} {stock_info[f'current_price_{currency}']}
#                         </div>
#                         """,
#                         unsafe_allow_html=True,
#                     )

#                 # --- Two-column layout for company details ---
#                 col1, col2 = st.columns(2)

#                 with col1:
#                     st.markdown(f"**Sector:** {stock_info['sector']}")
#                     st.markdown(f"**Industry:** {stock_info['industry']}")
#                     st.markdown(f"**Exchange:** {stock_info['exchange']}")

#                 with col2:
#                     st.markdown(f"**Market Cap:** {stock_info['market_cap']}")
#                     st.markdown(f"**Beta:** {stock_info['beta']}")
#                     st.markdown(f"**P/E Ratio:** {stock_info['pe_ratio']}")
#                     st.markdown(f"**Website:** [{stock_info['website']}]({stock_info['website']})")

#                 # --- Description ---
#                 st.subheader("🏢 Company Description")
#                 st.write(stock_info['description'])

#                 # --- Historical Charts ---
#                 st.subheader("📈 Price Charts")

#                 import yfinance as yf
#                 import components.charts as charts

#                 stock = yf.Ticker(stock_info["ticker"])
#                 hist = stock.history(start=start_date, end=end_date, interval=interval)

#                 if not hist.empty:
#                     hist = hist.reset_index()
#                     hist.rename(columns={"index": "Date"}, inplace=True)

#                     st.plotly_chart(charts.plot_line_price(hist), use_container_width=True)


#                 else:
#                     st.warning("No historical data available for this stock.")

#             else:
#                 st.info("Please enter a symbol and click Search.")



#         with tab2:
#             st.header("📈 Finances")
#             st.write("Financial data will appear here...")

#         with tab3:
#             st.header("📰 News & Sentiment")
#             st.write("News and sentiment data will appear here...")

#         with tab4:
#             st.header("🧠 LLM Summary")
#             st.write("AI-generated summary will appear here...")

#         with tab5:
#             st.header("💬 Ask AI")
#             query = st.text_input("Ask a question about this asset")
#             if st.button("Submit Question"):
#                 st.write(f"🤖 AI Response to: {query} (placeholder)")


# if __name__ == "__main__":
#     main()



import streamlit as st
import datetime
from fetchers.stocks import get_stock_info


# --- Main app ---
def main():
    st.set_page_config(page_title="MarketScopeAI", layout="wide")

    # First Page: Market Type Selection
    if "selected_market" not in st.session_state:
        st.session_state.selected_market = None

    if not st.session_state.selected_market:
        st.title(" MarketScopeAI Navigation")
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
            if user_symbol:
                st.session_state.search_symbol = user_symbol
            else:
                st.sidebar.warning("Please enter a symbol")

        # 2. Currency Selection
        currency = st.sidebar.selectbox(
            "Choose Currency", ["USD", "INR", "EUR", "GBP", "AED", "RUB"]
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
            st.session_state.search_symbol = None
            st.rerun()

        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Overview", "📈 Finances", "📰 News & Sentiment", "🧠 LLM Summary", "💬 Ask AI"]
        )

        # Check if user has searched for a symbol
        selected_symbol = st.session_state.get("search_symbol", None)

        with tab1:
            st.header("📊 Overview")

            if selected_symbol:
                stock_info = get_stock_info(selected_symbol, target_currency=currency)

                if "error" in stock_info:
                    st.error(stock_info["error"])
                else:
                    # --- Company Name + Ticker ---
                    st.subheader(f"{stock_info['ticker']} — {stock_info['name']}")

                    # --- Price Box ---
                    col_price = st.container()
                    with col_price:
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

                    # --- Two-column layout for company details ---
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

                    # --- Description ---
                    st.subheader("🏢 Company Description")
                    st.write(stock_info['description'])

                    # --- Historical Charts ---
                    st.subheader("📈 Price Charts")

                    import yfinance as yf
                    import plotly.graph_objs as go

                    stock = yf.Ticker(stock_info["ticker"])
                    hist = stock.history(start=start_date, end=end_date, interval=interval)

                    if not hist.empty:
                        hist = hist.reset_index()

                        # Enhanced dark chart
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=hist["Date"],
                            y=hist["Close"],
                            mode="lines+markers",
                            name="Closing Price",
                            line=dict(color="#00FFFF", width=2.5),  # Cyan line
                            marker=dict(size=4, color="#2b8be6"),
                            hovertemplate="Date: %{x}<br>Price: %{y:.2f}<extra></extra>"
                        ))

                        fig.update_layout(
                            title=f"{stock_info['ticker']} Closing Price Over Time",
                            title_x=0.5,
                            xaxis_title="Date",
                            yaxis_title=f"Price ({currency})",
                            template="plotly_dark",  # Dark theme
                            hovermode="x unified",
                            font=dict(size=14, color="white"),
                            margin=dict(l=20, r=20, t=40, b=20),
                            plot_bgcolor="black",
                            paper_bgcolor="black"
                        )

                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No historical data available for this stock.")

            else:
                st.info("Please enter a symbol and click Search.")


########################################################################                
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
