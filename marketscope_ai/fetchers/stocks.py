import yfinance as yf
import pandas as pd
from yahooquery import search  # Needed for search_symbol

def search_symbol(company_name):
    """
    Search for the stock symbol based on the company name using yahooquery.
    Returns the first matching symbol.
    """
    try:
        results = search(company_name)
        if 'quotes' in results:
            for quote in results['quotes']:
                if quote.get('quoteType') in ['EQUITY', 'ETF']:
                    return quote['symbol']
        return None
    except Exception as e:
        print(f"Error searching for symbol: {e}")
        return None

def fetch_stock_history(symbol, period='6mo', interval='1d', start=None, end=None):
    """
    Fetch historical stock data. If start and end dates are provided, use them instead of period.
    """
    try:
        ticker = yf.Ticker(symbol)
        if start and end:
            hist = ticker.history(start=start, end=end, interval=interval)
        else:
            hist = ticker.history(period=period, interval=interval)

        if hist.empty:
            return pd.DataFrame()

        hist.reset_index(inplace=True)
        if 'Datetime' in hist.columns:
            hist.rename(columns={'Datetime': 'Date'}, inplace=True)
        if 'date' in hist.columns:
            hist.rename(columns={'date': 'Date'}, inplace=True)

        return hist

    except Exception as e:
        print(f"[Error] Failed to fetch data for {symbol}: {e}")
        return pd.DataFrame()

def fetch_company_info(symbol):
    """
    Fetch company information for the given stock symbol using yfinance.
    Returns a dictionary of available company details.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return info
    except Exception as e:
        print(f"Error fetching company info for {symbol}: {e}")
        return None
