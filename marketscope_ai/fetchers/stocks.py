# # fetchers/stocks.py

# import yfinance as yf
# from yahooquery import search, Ticker as YQTicker
# from components.currency import convert_currency


# def search_symbol(query: str) -> str:
#     """
#     Search for the stock symbol based on the query (company name or symbol).
#     Returns the ticker symbol if found, else returns the original query.
#     """
#     try:
#         results = search(query)
#         if "quotes" in results and results["quotes"]:
#             return results["quotes"][0]["symbol"]
#     except Exception as e:
#         print(f"Error searching symbol: {e}")
#     return query


# def get_stock_info(query: str, target_currency: str = "USD") -> dict:
#     """
#     Fetch stock data + company details.
#     Combines YahooQuery (profile) + YFinance (market data).
#     Converts price into target currency.
#     """
#     try:
#         # Resolve symbol
#         symbol = search_symbol(query)

#         # YahooQuery for detailed company profile
#         yq_stock = YQTicker(symbol)
#         profile = yq_stock.asset_profile.get(symbol, {}) or {}

#         # YFinance for price & financial data
#         stock = yf.Ticker(symbol)
#         fast_info = getattr(stock, "fast_info", {})

#         # Basic identifiers
#         name = profile.get("longName") or stock.info.get("shortName") or stock.info.get("longName") or symbol
#         exchange = fast_info.get("exchange", stock.info.get("exchange", "N/A"))
#         native_currency = fast_info.get("currency", stock.info.get("currency", "USD"))

#         # Price & conversion
#         current_price = fast_info.get("last_price") or stock.info.get("currentPrice")
#         converted_price = convert_currency(current_price, native_currency, target_currency) if current_price else None

#         # Company details
#         sector = profile.get("sector", stock.info.get("sector", "N/A"))
#         industry = profile.get("industry", stock.info.get("industry", "N/A"))
#         country = profile.get("country", stock.info.get("country", "N/A"))
#         website = profile.get("website", stock.info.get("website", "N/A"))
#         description = profile.get("longBusinessSummary", stock.info.get("longBusinessSummary", "Description not available."))

#         # Financials
#         market_cap = fast_info.get("market_cap", stock.info.get("marketCap", "N/A"))
#         pe_ratio = stock.info.get("trailingPE", "N/A")
#         dividend_yield = stock.info.get("dividendYield", "N/A")
#         beta = stock.info.get("beta", "N/A")

#         return {
#             "ticker": symbol,
#             "name": name,
#             "exchange": exchange,
#             "native_currency": native_currency,
#             "current_price_native": round(current_price, 2) if current_price else None,
#             f"current_price_{target_currency}": converted_price,

#             # Company info
#             "sector": sector,
#             "industry": industry,
#             "country": country,
#             "website": website,
#             "description": description,

#             # Financials
#             "market_cap": market_cap,
#             "pe_ratio": pe_ratio,
#             "dividend_yield": dividend_yield,
#             "beta": beta,
#         }

#     except Exception as e:
#         return {"error": f"Error fetching stock data: {e}"}


# fetchers/stocks.py

import yfinance as yf
from yahooquery import search, Ticker as YQTicker
from components.currency import convert_currency


def search_symbol(query: str) -> str:
    """
    Search for the stock symbol based on the query (company name or symbol).
    First checks if query is already a valid symbol, then searches if needed.
    Returns the ticker symbol if found, else returns the original query.
    """
    try:
        query = query.strip()
        
        # First, check if the query is already a valid symbol by testing with yfinance
        try:
            test_ticker = yf.Ticker(query)
            test_data = test_ticker.history(period="5d")
            if not test_data.empty:
                # Query is already a valid symbol
                return query.upper()
        except:
            pass  # Not a valid symbol, continue with search
        
        # If not a valid symbol, search for it as a company name
        results = search(query)
        if "quotes" in results and results["quotes"]:
            found_symbol = results["quotes"][0]["symbol"]
            
            # Validate the found symbol before returning it
            try:
                test_ticker = yf.Ticker(found_symbol)
                test_data = test_ticker.history(period="5d")
                if not test_data.empty:
                    return found_symbol
            except:
                pass
        
        # If search fails or returns invalid symbol, return original query
        return query.upper()
        
    except Exception as e:
        print(f"Error searching symbol: {e}")
        return query.upper()


def get_stock_info(query: str, target_currency: str = "USD") -> dict:
    """
    Fetch stock data + company details.
    Combines YahooQuery (profile) + YFinance (market data).
    Converts price into target currency.
    """
    try:
        # Resolve symbol
        symbol = search_symbol(query)

        # YahooQuery for detailed company profile
        yq_stock = YQTicker(symbol)
        profile = yq_stock.asset_profile.get(symbol, {}) or {}

        # YFinance for price & financial data
        stock = yf.Ticker(symbol)
        fast_info = getattr(stock, "fast_info", {})

        # Basic identifiers
        name = profile.get("longName") or stock.info.get("shortName") or stock.info.get("longName") or symbol
        exchange = fast_info.get("exchange", stock.info.get("exchange", "N/A"))
        native_currency = fast_info.get("currency", stock.info.get("currency", "USD"))

        # Price & conversion
        current_price = fast_info.get("last_price") or stock.info.get("currentPrice")
        converted_price = convert_currency(current_price, native_currency, target_currency) if current_price else None

        # Company details
        sector = profile.get("sector", stock.info.get("sector", "N/A"))
        industry = profile.get("industry", stock.info.get("industry", "N/A"))
        country = profile.get("country", stock.info.get("country", "N/A"))
        website = profile.get("website", stock.info.get("website", "N/A"))
        description = profile.get("longBusinessSummary", stock.info.get("longBusinessSummary", "Description not available."))

        # Financials
        market_cap = fast_info.get("market_cap", stock.info.get("marketCap", "N/A"))
        pe_ratio = stock.info.get("trailingPE", "N/A")
        dividend_yield = stock.info.get("dividendYield", "N/A")
        beta = stock.info.get("beta", "N/A")

        return {
            "ticker": symbol,
            "name": name,
            "exchange": exchange,
            "native_currency": native_currency,
            "current_price_native": round(current_price, 2) if current_price else None,
            f"current_price_{target_currency}": converted_price,

            # Company info
            "sector": sector,
            "industry": industry,
            "country": country,
            "website": website,
            "description": description,

            # Financials
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "dividend_yield": dividend_yield,
            "beta": beta,
        }

    except Exception as e:
        return {"error": f"Error fetching stock data: {e}"}