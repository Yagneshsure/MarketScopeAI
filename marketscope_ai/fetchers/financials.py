# # marketscope_ai/tabs/finances.py

# import yfinance as yf
# import plotly.express as px
# import streamlit as st

# from fetchers.financials import get_financials, get_eps
# from components.charts import (
#     plot_line_price, plot_candlestick, plot_volume_histogram,
#     plot_price_with_ma, plot_ma_crossover, plot_bollinger_bands,
#     plot_rsi, plot_macd, plot_volatility, plot_drawdown
# )
# from components.helpers import _apply_dark_layout, _fmt_num


# def render_finances(symbol, start_date, end_date, currency):
#     """Render the Finances tab for the given symbol."""

#     st.header("💰 Finance Overview")

#     if symbol:
#         try:
#             ticker = yf.Ticker(symbol)
#             info = ticker.info

#             # =====================
#             # Key Metrics
#             # =====================
#             st.subheader("📊 Key Metrics")
#             col1, col2, col3 = st.columns(3)

#             with col1:
#                 st.markdown(f"<div class='metric-card'><b>Market Cap</b><br>${_fmt_num(info.get('marketCap'))}</div>", unsafe_allow_html=True)
#                 st.markdown(f"<div class='metric-card'><b>P/E Ratio</b><br>{_fmt_num(info.get('forwardPE'))}</div>", unsafe_allow_html=True)

#             with col2:
#                 st.markdown(f"<div class='metric-card'><b>EPS (TTM)</b><br>{_fmt_num(info.get('trailingEps'))}</div>", unsafe_allow_html=True)
#                 div_yield = info.get("dividendYield")
#                 st.markdown(
#                     f"<div class='metric-card'><b>Dividend Yield</b><br>{div_yield*100:.2f}%</div>"
#                     if isinstance(div_yield, (float, int)) else
#                     "<div class='metric-card'><b>Dividend Yield</b><br>N/A</div>",
#                     unsafe_allow_html=True
#                 )

#             with col3:
#                 st.markdown(f"<div class='metric-card'><b>Revenue (TTM)</b><br>${_fmt_num(info.get('totalRevenue'))}</div>", unsafe_allow_html=True)
#                 st.markdown(f"<div class='metric-card'><b>Net Income (TTM)</b><br>${_fmt_num(info.get('netIncomeToCommon'))}</div>", unsafe_allow_html=True)

#             # =====================
#             # Revenue & Net Income Trend
#             # =====================
#             st.subheader("📈 Revenue & Net Income Trend")
#             fin_df = get_financials(symbol)
#             if fin_df is not None and not fin_df.empty:
#                 fig_fin = px.bar(fin_df, x="Year", y=["Revenue", "Net Income"], barmode="group")
#                 _apply_dark_layout(fig_fin, "Annual Revenue vs Net Income")
#                 st.plotly_chart(fig_fin, use_container_width=True)
#             else:
#                 st.warning("Financial statement data not available.")

#             # =====================
#             # EPS Trend
#             # =====================
#             st.subheader("📈 EPS Trend")
#             eps_df = get_eps(symbol)
#             if eps_df is not None and not eps_df.empty:
#                 fig_eps = px.line(eps_df, x="Quarter", y="EPS", markers=True)
#                 _apply_dark_layout(fig_eps, "Quarterly EPS")
#                 st.plotly_chart(fig_eps, use_container_width=True)
#             else:
#                 st.info("Earnings data not available.")

#             # =====================
#             # Technical Charts
#             # =====================
#             st.subheader("📉 Technical Charts")
#             hist_tc = ticker.history(start=start_date, end=end_date, interval="1d")

#             if hist_tc is None or hist_tc.empty:
#                 st.warning("No historical OHLCV available to render technical charts.")
#             else:
#                 data = hist_tc.reset_index()
#                 chart_options = [
#                     "Line Price", "Candlestick", "Volume Histogram", "Price with Moving Averages",
#                     "MA Crossover", "Bollinger Bands", "RSI", "MACD", "Volatility", "Drawdown"
#                 ]
#                 selected_charts = st.multiselect(
#                     "Select charts to display:",
#                     chart_options,
#                     default=["Line Price", "Candlestick", "RSI"]
#                 )

#                 chart_map = {
#                     "Line Price": plot_line_price,
#                     "Candlestick": plot_candlestick,
#                     "Volume Histogram": plot_volume_histogram,
#                     "Price with Moving Averages": plot_price_with_ma,
#                     "MA Crossover": plot_ma_crossover,
#                     "Bollinger Bands": plot_bollinger_bands,
#                     "RSI": plot_rsi,
#                     "MACD": plot_macd,
#                     "Volatility": plot_volatility,
#                     "Drawdown": plot_drawdown,
#                 }

#                 for chart_name in selected_charts:
#                     fig = chart_map[chart_name](data)
#                     _apply_dark_layout(fig, chart_name)
#                     st.plotly_chart(fig, use_container_width=True)

#         except Exception as e:
#             st.error(f"Error loading financials: {e}")

#     else:
#         st.info("Enter a stock symbol in the sidebar to see financial data.")


# marketscope_ai/fetchers/financials.py

import yfinance as yf
import pandas as pd


def get_financials(symbol: str):
    """
    Fetch annual financials (Revenue, Net Income) for a stock symbol.
    Returns a DataFrame with columns: ['Year', 'Revenue', 'Net Income']
    """
    try:
        ticker = yf.Ticker(symbol)
        financials = ticker.financials  # Annual financials
        if financials is None or financials.empty:
            return None

        df = pd.DataFrame({
            "Year": financials.columns.year,
            "Revenue": financials.loc["Total Revenue"],
            "Net Income": financials.loc["Net Income"]
        }).reset_index(drop=True)

        return df
    except Exception as e:
        print(f"Error fetching financials for {symbol}: {e}")
        return None


def get_eps(symbol: str):
    """
    Fetch quarterly EPS for a stock symbol.
    Returns a DataFrame with columns: ['Quarter', 'EPS']
    """
    try:
        ticker = yf.Ticker(symbol)
        earnings = ticker.quarterly_earnings  # Quarterly EPS
        if earnings is None or earnings.empty:
            return None

        df = earnings.reset_index().rename(columns={"Earnings": "EPS"})
        df["Quarter"] = df["Quarter"].astype(str)
        return df
    except Exception as e:
        print(f"Error fetching EPS for {symbol}: {e}")
        return None
