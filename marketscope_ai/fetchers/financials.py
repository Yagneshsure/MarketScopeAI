# fetchers/financials.py
import yfinance as yf
import pandas as pd

def get_financials(symbol: str):
    """
    Fetch revenue and net income from Yahoo Finance.
    Returns a DataFrame with yearly financials.
    """
    try:
        ticker = yf.Ticker(symbol)
        fin = ticker.financials  # yearly financials (income statement)
        if fin.empty:
            return None

        df = fin.T.reset_index()
        df.rename(columns={"Total Revenue": "Revenue", "Net Income": "Net Income"}, inplace=True)
        df = df[["index", "Revenue", "Net Income"]]
        df.rename(columns={"index": "Year"}, inplace=True)
        df["Year"] = df["Year"].dt.year
        return df
    except Exception as e:
        print(f"Error fetching financials: {e}")
        return None


def get_eps(symbol: str):
    """
    Fetch earnings per share (EPS) history from Yahoo Finance.
    Returns a DataFrame with quarterly EPS.
    """
    try:
        ticker = yf.Ticker(symbol)
        earnings = ticker.quarterly_earnings
        if earnings is None or earnings.empty:
            return None

        df = earnings.reset_index()
        df.rename(columns={"Earnings": "EPS", "Revenue": "Revenue"}, inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching EPS: {e}")
        return None
