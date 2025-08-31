# fetchers/stocks.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


class StockFetcher:
    """
    StockFetcher retrieves and processes stock market data using yfinance.
    """

    def __init__(self, ticker: str, period: str = "6mo", interval: str = "1d"):
        """
        Initialize the StockFetcher class.

        Args:
            ticker (str): Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'MSFT').
            period (str): Time range for fetching data (e.g., '1mo', '6mo', '1y', '5y', 'max').
            interval (str): Data frequency (e.g., '1d', '1h', '5m').
        """
        self.ticker = ticker.upper()
        self.period = period
        self.interval = interval
        self.stock = yf.Ticker(self.ticker)

    def get_historical_data(self) -> pd.DataFrame:
        """
        Fetch historical stock price data.

        Returns:
            pd.DataFrame: Historical OHLCV (Open, High, Low, Close, Volume) data.
        """
        try:
            df = self.stock.history(period=self.period, interval=self.interval)
            df.reset_index(inplace=True)
            df["Date"] = pd.to_datetime(df["Date"])
            return df
        except Exception as e:
            print(f"[ERROR] Could not fetch historical data for {self.ticker}: {e}")
            return pd.DataFrame()

    def get_company_info(self) -> dict:
        """
        Fetch basic company information.

        Returns:
            dict: Dictionary containing company details.
        """
        try:
            info = self.stock.info
            return {
                "symbol": self.ticker,
                "shortName": info.get("shortName", "N/A"),
                "longName": info.get("longName", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "country": info.get("country", "N/A"),
                "website": info.get("website", "N/A"),
                "marketCap": info.get("marketCap", None),
                "currency": info.get("currency", "N/A"),
            }
        except Exception as e:
            print(f"[ERROR] Could not fetch company info for {self.ticker}: {e}")
            return {}

    def get_current_price(self) -> float:
        """
        Fetch the latest stock price.

        Returns:
            float: Current market price.
        """
        try:
            data = self.stock.history(period="1d", interval="1m")
            if not data.empty:
                return round(data["Close"].iloc[-1], 2)
            return None
        except Exception as e:
            print(f"[ERROR] Could not fetch current price for {self.ticker}: {e}")
            return None

    def get_financials(self) -> dict:
        """
        Fetch financial statements (income statement, balance sheet, cash flow).

        Returns:
            dict: Financial data as pandas DataFrames.
        """
        try:
            return {
                "income_statement": self.stock.financials,
                "balance_sheet": self.stock.balance_sheet,
                "cashflow": self.stock.cashflow,
            }
        except Exception as e:
            print(f"[ERROR] Could not fetch financials for {self.ticker}: {e}")
            return {}

    def get_recommendations(self) -> pd.DataFrame:
        """
        Fetch analyst recommendations.

        Returns:
            pd.DataFrame: Analyst recommendations data.
        """
        try:
            df = self.stock.recommendations
            return df.reset_index() if df is not None else pd.DataFrame()
        except Exception as e:
            print(f"[ERROR] Could not fetch recommendations for {self.ticker}: {e}")
            return pd.DataFrame()


# Example Usage (only runs when testing this file directly)
if __name__ == "__main__":
    stock = StockFetcher("AAPL", period="6mo", interval="1d")

    print("🔹 Company Info:")
    print(stock.get_company_info())

    print("\n🔹 Current Price:")
    print(stock.get_current_price())

    print("\n🔹 Historical Data (last 5 rows):")
    print(stock.get_historical_data().tail())

    print("\n🔹 Analyst Recommendations:")
    print(stock.get_recommendations().head())
