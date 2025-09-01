import yfinance as yf
import pandas as pd
from yahooquery import search
from components.currency import get_stock_price

# Map exchanges to their default currencies
EXCHANGE_CURRENCY_MAP = {
    "NSE": "INR", "BSE": "INR",
    "NYSE": "USD", "NASDAQ": "USD",
    "TSX": "CAD", "LSE": "GBP",
    "HKEX": "HKD", "TSE": "JPY",
    "SSE": "CNY", "SZSE": "CNY",
    "FWB": "EUR", "ETR": "EUR",
    "SWX": "CHF", "ASX": "AUD"
}


def search_symbol(company_name: str):
    """Search for the stock symbol based on the company name using yahooquery."""
    try:
        results = search(company_name)
        if 'quotes' in results:
            for quote in results['quotes']:
                if quote.get('exchange') in EXCHANGE_CURRENCY_MAP:
                    return quote['symbol']
        return None
    except Exception as e:
        return f"Error while searching symbol: {str(e)}"


def fetch_stock_data(symbol: str, period="6mo", interval="1d"):
    """Fetch historical stock data."""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, interval=interval)
        hist.reset_index(inplace=True)
        return hist
    except Exception as e:
        return f"Error fetching stock data: {str(e)}"


def fetch_company_info(symbol: str):
    """Fetch company information including name, sector, industry, description."""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "longName": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "longBusinessSummary": info.get("longBusinessSummary", "No description available")
        }
    except Exception as e:
        return {"error": f"Error fetching company info: {str(e)}"}


def fetch_current_price(symbol: str, target_currency="INR"):
    """
    Fetch current stock price and convert to target currency.
    Uses universal get_stock_price from components.currency.
    """
    try:
        converted_price, currency = get_stock_price(symbol, base_currency=target_currency)
        return round(converted_price, 2), currency
    except Exception as e:
        return f"Error fetching price: {str(e)}", None
