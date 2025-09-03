# fetchers/financials.py

import yfinance as yf
import pandas as pd

def get_financials(symbol: str):
    """
    Fetch annual financials (Revenue & Net Income) for a stock symbol.
    Returns DataFrame with columns: Year, Revenue, Net Income
    """
    try:
        ticker = yf.Ticker(symbol)
        fin = ticker.financials  # annual financials
        if fin is None or fin.empty:
            return None

        fin = fin.T.reset_index()
        fin.rename(columns={"index": "Year"}, inplace=True)

        df = pd.DataFrame({
            "Year": fin["Year"].dt.year,
            "Revenue": fin.get("Total Revenue", pd.Series([None] * len(fin))),
            "Net Income": fin.get("Net Income", pd.Series([None] * len(fin))),
        })
        return df
    except Exception:
        return None


def get_eps(symbol: str):
    """
    Fetch quarterly EPS trend for a stock symbol.
    Returns DataFrame with columns: Quarter, EPS
    """
    try:
        ticker = yf.Ticker(symbol)
        earnings = ticker.quarterly_earnings
        if earnings is None or earnings.empty:
            return None

        earnings = earnings.reset_index()
        df = pd.DataFrame({
            "Quarter": earnings["Quarter"].astype(str),
            "EPS": earnings["Earnings"],
        })
        return df
    except Exception:
        return None
