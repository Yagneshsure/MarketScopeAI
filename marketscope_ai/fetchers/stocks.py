# import yfinance as yf
# import pandas as pd
# from datetime import datetime
# from helpers.currency import convert_price

# def get_stock_data(symbol: str, start_date: str, end_date: str, interval: str, currency: str):
#     """
#     Fetch stock data from yfinance, convert to selected currency, and return a DataFrame.

#     Args:
#         symbol (str): Stock ticker symbol (e.g., "AAPL", "TSLA").
#         start_date (str): Start date for data (YYYY-MM-DD).
#         end_date (str): End date for data (YYYY-MM-DD).
#         interval (str): Interval (e.g., "1d", "1h").
#         currency (str): Target currency (USD, INR, GBP, AED, RUB).

#     Returns:
#         pd.DataFrame: Stock OHLCV data with converted prices.
#     """
#     try:
#         ticker = yf.Ticker(symbol)
#         df = ticker.history(start=start_date, end=end_date, interval=interval)

#         if df.empty:
#             return pd.DataFrame()

#         # Convert currency
#         for col in ["Open", "High", "Low", "Close"]:
#             df[col] = df[col].apply(lambda x: convert_price(x, "USD", currency))

#         df.reset_index(inplace=True)
#         return df

#     except Exception as e:
#         print(f"Error fetching stock data: {e}")
#         return pd.DataFrame()


# def get_company_info(symbol: str):
#     """
#     Fetch basic company information.
#     """
#     try:
#         ticker = yf.Ticker(symbol)
#         info = ticker.info

#         company_data = {
#             "Name": info.get("longName", "N/A"),
#             "Sector": info.get("sector", "N/A"),
#             "Industry": info.get("industry", "N/A"),
#             "Market Cap": info.get("marketCap", "N/A"),
#             "Currency": info.get("currency", "USD")
#         }

#         return company_data
#     except Exception as e:
#         print(f"Error fetching company info: {e}")
#         return {}



# fetchers/stocks.py

import yfinance as yf
from yahooquery import search
from components.currency import convert_currency


def search_symbol(query: str) -> str:
    """
    Search for the stock symbol based on the query (company name or symbol).
    Returns the ticker symbol if found, else returns the original query.
    """
    try:
        results = search(query)
        if "quotes" in results and results["quotes"]:
            return results["quotes"][0]["symbol"]
    except Exception as e:
        print(f"Error searching for symbol: {e}")
    return query  # fallback to user input


def get_stock_info(query: str, target_currency: str = "USD") -> dict:
    """
    Fetch stock data from Yahoo Finance.
    Supports both stock symbols and company names.
    Converts price into the chosen target currency.
    """
    try:
        # Resolve company name -> ticker
        symbol = search_symbol(query)
        stock = yf.Ticker(symbol)
        info = stock.info

        # Extract basic info
        name = info.get("shortName") or info.get("longName") or "Unknown Company"
        exchange = info.get("exchange", "Unknown")
        native_currency = info.get("currency", "USD")

        # Get current price
        current_price = info.get("currentPrice")

        # Conversion
        converted_price = None
        if current_price is not None:
            converted_price = convert_currency(current_price, native_currency, target_currency)

        return {
            "ticker": symbol,
            "name": name,
            "exchange": exchange,
            "native_currency": native_currency,
            "current_price_native": round(current_price, 2) if current_price else None,
            f"current_price_{target_currency}": converted_price,
        }

    except Exception as e:
        return {"error": f"Error fetching stock data: {e}"}
