# # fetchers/financials.py
# import yfinance as yf
# import pandas as pd
# from datetime import datetime, timedelta
# from .stocks import search_symbol  # Import the proven search function


# def validate_symbol(symbol: str):
#     """
#     Validate if a symbol exists and has data
#     Returns: dict with 'valid' boolean and 'error' message if invalid
#     """
#     try:
#         ticker = yf.Ticker(symbol)
#         test_data = ticker.history(period="5d")
#         if test_data.empty:
#             return {
#                 'valid': False, 
#                 'error': f"No data found for symbol '{symbol}'. Please check if the ticker symbol is correct."
#             }
#         return {'valid': True, 'error': None}
#     except Exception as e:
#         return {'valid': False, 'error': f"Invalid symbol '{symbol}': {str(e)}"}


# def resolve_symbol_for_financials(input_string: str):
#     """
#     Resolve input to a valid ticker symbol using improved logic
#     First checks if input is already a valid symbol, then falls back to search
#     Returns: dict with 'symbol', 'name', and status info
#     """
#     try:
#         input_string = input_string.strip().upper()
        
#         # Step 1: Check if input is already a valid ticker symbol
#         validation = validate_symbol(input_string)
#         if validation['valid']:
#             # Input is already a valid symbol, get company name
#             ticker = yf.Ticker(input_string)
#             info = ticker.info
#             company_name = info.get('longName', info.get('shortName', input_string))
            
#             return {
#                 'found': True,
#                 'original_input': input_string,
#                 'symbol': input_string,
#                 'name': company_name,
#                 'resolution_method': 'direct_symbol'
#             }
        
#         # Step 2: If not a valid symbol, try to search for it as a company name
#         try:
#             # Use the search function from stocks.py
#             resolved_symbol = search_symbol(input_string)
            
#             # If search returned something different, validate it
#             if resolved_symbol and resolved_symbol.upper() != input_string:
#                 validation = validate_symbol(resolved_symbol)
#                 if validation['valid']:
#                     # Get company name for the resolved symbol
#                     ticker = yf.Ticker(resolved_symbol)
#                     info = ticker.info
#                     company_name = info.get('longName', info.get('shortName', resolved_symbol))
                    
#                     return {
#                         'found': True,
#                         'original_input': input_string,
#                         'symbol': resolved_symbol,
#                         'name': company_name,
#                         'resolution_method': 'company_name_search'
#                     }
#         except Exception as search_error:
#             print(f"Search failed for '{input_string}': {search_error}")
        
#         # Step 3: If all else fails, return not found
#         return {
#             'found': False,
#             'original_input': input_string,
#             'symbol': None,
#             'name': None,
#             'error': f"Could not find valid financial data for '{input_string}'. Please check if the ticker symbol or company name is correct.",
#             'resolution_method': 'failed'
#         }
            
#     except Exception as e:
#         return {
#             'found': False,
#             'original_input': input_string,
#             'symbol': None,
#             'name': None,
#             'error': f"Error resolving symbol for '{input_string}': {str(e)}",
#             'resolution_method': 'error'
#         }


# def get_basic_info(symbol: str):
#     """
#     Get basic company information and key metrics
#     Returns: dict with company info or None if failed
#     """
#     try:
#         ticker = yf.Ticker(symbol)
        
#         # Try multiple methods to get info
#         info = None
#         try:
#             info = ticker.info
#         except:
#             try:
#                 info = ticker.get_info()
#             except:
#                 pass
        
#         if not info:
#             return None
            
#         # Extract key metrics
#         result = {
#             'company_name': info.get('longName', info.get('shortName', symbol)),
#             'sector': info.get('sector', 'N/A'),
#             'industry': info.get('industry', 'N/A'),
#             'country': info.get('country', 'N/A'),
#             'exchange': info.get('exchange', 'N/A'),
#             'currency': info.get('currency', 'USD'),
#             'market_cap': info.get('marketCap'),
#             'pe_ratio': info.get('trailingPE') or info.get('forwardPE'),
#             'eps': info.get('trailingEps'),
#             'dividend_yield': info.get('dividendYield'),
#             'revenue_ttm': info.get('totalRevenue'),
#             'net_income_ttm': info.get('netIncomeToCommon'),
#             'book_value': info.get('bookValue'),
#             'price_to_book': info.get('priceToBook'),
#             'debt_to_equity': info.get('debtToEquity'),
#             'current_ratio': info.get('currentRatio'),
#             'beta': info.get('beta'),
#             'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
#             'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
#             'average_volume': info.get('averageVolume'),
#             'website': info.get('website'),
#             'business_summary': info.get('longBusinessSummary'),
#             'employees': info.get('fullTimeEmployees'),
#             'profit_margin': info.get('profitMargins'),
#             'operating_margin': info.get('operatingMargins'),
#             'return_on_equity': info.get('returnOnEquity'),
#             'return_on_assets': info.get('returnOnAssets'),
#             'enterprise_value': info.get('enterpriseValue'),
#             'price_to_sales': info.get('priceToSalesTrailing12Months'),
#             'gross_margin': info.get('grossMargins'),
#             'asset_turnover': info.get('assetTurnover'),
#             'peg_ratio': info.get('pegRatio'),
#             'timezone': info.get('timeZoneFullName')
#         }
        
#         return result
        
#     except Exception as e:
#         print(f"Error getting basic info for {symbol}: {e}")
#         return None


# def get_price_data(symbol: str, start_date=None, end_date=None, period="1y"):
#     """
#     Get historical price data
#     Returns: DataFrame with OHLCV data or None if failed
#     """
#     try:
#         ticker = yf.Ticker(symbol)
        
#         if start_date and end_date:
#             hist = ticker.history(start=start_date, end=end_date)
#         else:
#             hist = ticker.history(period=period)
        
#         if hist.empty:
#             return None
            
#         return hist
        
#     except Exception as e:
#         print(f"Error getting price data for {symbol}: {e}")
#         return None


# def get_financial_statements(symbol: str):
#     """
#     Get financial statements (income statement, balance sheet, cash flow)
#     Returns: dict with financial data or None if failed
#     """
#     try:
#         ticker = yf.Ticker(symbol)
#         result = {}
        
#         # Annual financials
#         try:
#             financials = ticker.financials
#             if financials is not None and not financials.empty:
#                 result['annual_financials'] = financials
#         except:
#             pass
        
#         # Quarterly financials
#         try:
#             quarterly_financials = ticker.quarterly_financials
#             if quarterly_financials is not None and not quarterly_financials.empty:
#                 result['quarterly_financials'] = quarterly_financials
#         except:
#             pass
        
#         # Balance sheet
#         try:
#             balance_sheet = ticker.balance_sheet
#             if balance_sheet is not None and not balance_sheet.empty:
#                 result['balance_sheet'] = balance_sheet
            
#             # Quarterly balance sheet
#             quarterly_balance_sheet = ticker.quarterly_balance_sheet
#             if quarterly_balance_sheet is not None and not quarterly_balance_sheet.empty:
#                 result['quarterly_balance_sheet'] = quarterly_balance_sheet
#         except:
#             pass
        
#         # Cash flow
#         try:
#             cashflow = ticker.cashflow
#             if cashflow is not None and not cashflow.empty:
#                 result['cashflow'] = cashflow
            
#             # Quarterly cash flow
#             quarterly_cashflow = ticker.quarterly_cashflow
#             if quarterly_cashflow is not None and not quarterly_cashflow.empty:
#                 result['quarterly_cashflow'] = quarterly_cashflow
#         except:
#             pass
        
#         return result if result else None
        
#     except Exception as e:
#         print(f"Error getting financial statements for {symbol}: {e}")
#         return None


# def get_earnings_data(symbol: str):
#     """
#     Get earnings data (annual and quarterly)
#     Returns: dict with earnings data or None if failed
#     """
#     try:
#         ticker = yf.Ticker(symbol)
#         result = {}
        
#         # Annual earnings
#         try:
#             earnings = ticker.earnings
#             if earnings is not None and not earnings.empty:
#                 result['annual_earnings'] = earnings
#         except:
#             pass
        
#         # Quarterly earnings
#         try:
#             quarterly_earnings = ticker.quarterly_earnings
#             if quarterly_earnings is not None and not quarterly_earnings.empty:
#                 result['quarterly_earnings'] = quarterly_earnings
#         except:
#             pass
        
#         # Earnings calendar
#         try:
#             earnings_calendar = ticker.calendar
#             if earnings_calendar is not None and not earnings_calendar.empty:
#                 result['earnings_calendar'] = earnings_calendar
#         except:
#             pass
        
#         return result if result else None
        
#     except Exception as e:
#         print(f"Error getting earnings data for {symbol}: {e}")
#         return None


# def get_dividend_data(symbol: str):
#     """
#     Get dividend history
#     Returns: Series with dividend data or None if failed
#     """
#     try:
#         ticker = yf.Ticker(symbol)
#         dividends = ticker.dividends
        
#         if dividends is not None and not dividends.empty:
#             return dividends
#         return None
        
#     except Exception as e:
#         print(f"Error getting dividend data for {symbol}: {e}")
#         return None


# def get_revenue_and_income_trend(symbol: str):
#     """
#     Extract revenue and net income trend from financials
#     Returns: DataFrame with Year, Revenue, Net Income columns or None if failed
#     """
#     try:
#         financial_data = get_financial_statements(symbol)
#         if not financial_data or 'annual_financials' not in financial_data:
#             return None
        
#         financials = financial_data['annual_financials']
        
#         # Look for revenue keys
#         revenue_keys = [key for key in financials.index 
#                        if any(term in key.lower() for term in ['total revenue', 'revenue', 'net sales'])]
        
#         # Look for net income keys
#         income_keys = [key for key in financials.index 
#                       if any(term in key.lower() for term in ['net income', 'net earnings'])]
        
#         if not revenue_keys or not income_keys:
#             return None
        
#         revenue_data = financials.loc[revenue_keys[0]]
#         income_data = financials.loc[income_keys[0]]
        
#         # Create DataFrame
#         df = pd.DataFrame({
#             'Year': revenue_data.index.year,
#             'Revenue': revenue_data.values,
#             'Net Income': income_data.values
#         }).sort_values('Year')
        
#         return df
        
#     except Exception as e:
#         print(f"Error getting revenue and income trend for {symbol}: {e}")
#         return None


# def get_key_ratios(symbol: str):
#     """
#     Calculate and return key financial ratios
#     Returns: dict with financial ratios or None if failed
#     """
#     try:
#         info = get_basic_info(symbol)
#         if not info:
#             return None
        
#         ratios = {}
        
#         # Valuation ratios
#         if info.get('pe_ratio'):
#             ratios['pe_ratio'] = info['pe_ratio']
#         if info.get('price_to_book'):
#             ratios['price_to_book'] = info['price_to_book']
        
#         # Profitability ratios
#         if info.get('revenue_ttm') and info.get('net_income_ttm'):
#             ratios['net_margin'] = (info['net_income_ttm'] / info['revenue_ttm']) * 100
        
#         # Liquidity ratios
#         if info.get('current_ratio'):
#             ratios['current_ratio'] = info['current_ratio']
        
#         # Leverage ratios
#         if info.get('debt_to_equity'):
#             ratios['debt_to_equity'] = info['debt_to_equity']
        
#         # Market ratios
#         if info.get('dividend_yield'):
#             ratios['dividend_yield'] = info['dividend_yield'] * 100
        
#         if info.get('beta'):
#             ratios['beta'] = info['beta']
        
#         return ratios if ratios else None
        
#     except Exception as e:
#         print(f"Error calculating key ratios for {symbol}: {e}")
#         return None


# def get_all_financial_data(input_string: str, start_date=None, end_date=None, period="1y"):
#     """
#     Get comprehensive financial data for a symbol or company name
#     Uses improved symbol resolution to handle both symbols and company names
#     Returns: dict with all available financial data
#     """
#     try:
#         # Use improved symbol resolution
#         resolution = resolve_symbol_for_financials(input_string)
        
#         if not resolution['found']:
#             return {'error': resolution['error']}
        
#         symbol = resolution['symbol']
#         company_name = resolution['name']
#         original_input = resolution['original_input']
#         resolution_method = resolution['resolution_method']
        
#         result = {
#             'search_info': {
#                 'original_input': original_input,
#                 'resolved_symbol': symbol,
#                 'company_name': company_name,
#                 'search_successful': True,
#                 'resolution_method': resolution_method
#             }
#         }
        
#         # Basic info and metrics
#         basic_info = get_basic_info(symbol)
#         if basic_info:
#             result['basic_info'] = basic_info
        
#         # Price data
#         price_data = get_price_data(symbol, start_date, end_date, period)
#         if price_data is not None:
#             result['price_data'] = price_data
#             result['current_price'] = price_data['Close'].iloc[-1]
#             result['price_change'] = price_data['Close'].iloc[-1] - price_data['Close'].iloc[-2] if len(price_data) > 1 else 0
#             result['price_change_percent'] = ((result['price_change'] / price_data['Close'].iloc[-2]) * 100) if len(price_data) > 1 and price_data['Close'].iloc[-2] != 0 else 0
        
#         # Financial statements
#         financial_statements = get_financial_statements(symbol)
#         if financial_statements:
#             result['financial_statements'] = financial_statements
        
#         # Earnings data
#         earnings_data = get_earnings_data(symbol)
#         if earnings_data:
#             result['earnings_data'] = earnings_data
        
#         # Revenue and income trend
#         revenue_income_trend = get_revenue_and_income_trend(symbol)
#         if revenue_income_trend is not None:
#             result['revenue_income_trend'] = revenue_income_trend
        
#         # Key ratios
#         key_ratios = get_key_ratios(symbol)
#         if key_ratios:
#             result['key_ratios'] = key_ratios
        
#         # Dividend data
#         dividend_data = get_dividend_data(symbol)
#         if dividend_data is not None:
#             result['dividend_data'] = dividend_data
        
#         result['data_source'] = 'Yahoo Finance'
        
#         return result
        
#     except Exception as e:
#         return {'error': f"Error fetching financial data for '{input_string}': {str(e)}"}


# def get_quick_financial_summary(input_string: str):
#     """
#     Get a quick financial summary using improved symbol resolution
#     Returns: dict with key financial metrics
#     """
#     try:
#         resolution = resolve_symbol_for_financials(input_string)
#         if not resolution['found']:
#             return {'error': resolution['error']}
        
#         symbol = resolution['symbol']
        
#         # Get basic info and price data
#         ticker = yf.Ticker(symbol)
#         info = ticker.info
#         hist = ticker.history(period="5d")
        
#         if hist.empty:
#             return {'error': f"No price data available for {symbol}"}
        
#         current_price = hist['Close'].iloc[-1]
#         prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
#         price_change = current_price - prev_price
#         price_change_percent = (price_change / prev_price * 100) if prev_price != 0 else 0
        
#         return {
#             'search_info': {
#                 'original_input': input_string,
#                 'resolved_symbol': symbol,
#                 'company_name': resolution['name'],
#                 'resolution_method': resolution['resolution_method']
#             },
#             'price_info': {
#                 'current_price': round(current_price, 2),
#                 'price_change': round(price_change, 2),
#                 'price_change_percent': round(price_change_percent, 2),
#                 'currency': info.get('currency', 'USD')
#             },
#             'key_metrics': {
#                 'market_cap': format_large_number(info.get('marketCap')),
#                 'pe_ratio': info.get('trailingPE'),
#                 'dividend_yield': format_percentage(info.get('dividendYield', 0) * 100) if info.get('dividendYield') else "N/A",
#                 'beta': info.get('beta'),
#                 '52_week_high': info.get('fiftyTwoWeekHigh'),
#                 '52_week_low': info.get('fiftyTwoWeekLow')
#             }
#         }
        
#     except Exception as e:
#         return {'error': f"Error getting financial summary for '{input_string}': {str(e)}"}


# def format_large_number(value):
#     """
#     Format large numbers for display (e.g., 1.5B, 234.5M)
#     """
#     if value is None:
#         return "N/A"
    
#     try:
#         value = float(value)
#         if value >= 1e12:
#             return f"${value/1e12:.2f}T"
#         elif value >= 1e9:
#             return f"${value/1e9:.2f}B"
#         elif value >= 1e6:
#             return f"${value/1e6:.2f}M"
#         elif value >= 1e3:
#             return f"${value/1e3:.1f}K"
#         else:
#             return f"${value:.0f}"
#     except:
#         return "N/A"


# def format_percentage(value):
#     """
#     Format percentage values for display
#     """
#     if value is None:
#         return "N/A"
    
#     try:
#         return f"{float(value):.2f}%"
#     except:
#         return "N/A"


# # Test function
# def test_with_stocks_search():
#     """
#     Test the integration with improved symbol resolution
#     """
#     test_cases = [
#         "Tesla",      # Company name
#         "TSLA",       # Direct symbol
#         "Apple",      # Company name
#         "AAPL",       # Direct symbol
#         "Microsoft",  # Company name
#         "MSFT",       # Direct symbol
#         "GOOGL",      # Direct symbol
#         "Amazon",     # Company name
#         "AMZN"        # Direct symbol
#     ]
    
#     print("Testing Financial Data with improved symbol resolution:")
#     print("=" * 60)
    
#     for test in test_cases:
#         print(f"\nTesting: '{test}'")
#         print("-" * 40)
        
#         summary = get_quick_financial_summary(test)
#         if 'error' not in summary:
#             search_info = summary['search_info']
#             price_info = summary['price_info']
#             metrics = summary['key_metrics']
            
#             print(f"✓ Input: '{search_info['original_input']}' → Symbol: {search_info['resolved_symbol']}")
#             print(f"  Company: {search_info['company_name']}")
#             print(f"  Resolution Method: {search_info['resolution_method']}")
#             print(f"  Price: {price_info['currency']} {price_info['current_price']}")
#             print(f"  Change: {price_info['price_change']} ({price_info['price_change_percent']:.2f}%)")
#             print(f"  Market Cap: {metrics['market_cap']}")
#             print(f"  P/E Ratio: {metrics['pe_ratio']}")
#         else:
#             print(f"✗ Error: {summary['error']}")


# if __name__ == "__main__":
#     test_with_stocks_search()




# fetchers/financials.py
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def validate_symbol(symbol: str):
    """
    Validate if a symbol exists and has data
    Returns: dict with 'valid' boolean and 'error' message if invalid
    """
    try:
        ticker = yf.Ticker(symbol.upper())
        test_data = ticker.history(period="2d")  # Reduced period for faster response
        if test_data.empty:
            return {
                'valid': False, 
                'error': f"No data found for symbol '{symbol}'. Please check if the ticker symbol is correct."
            }
        return {'valid': True, 'error': None}
    except Exception as e:
        return {'valid': False, 'error': f"Invalid symbol '{symbol}': {str(e)}"}


def resolve_symbol_for_financials(input_string: str):
    """
    Resolve input to a valid ticker symbol
    Uses a simple approach: direct validation, then yahooquery search
    """
    try:
        original_input = input_string.strip()
        
        # Step 1: Try direct validation (handles existing symbols like AAPL, MSFT)
        validation = validate_symbol(original_input)
        if validation['valid']:
            ticker = yf.Ticker(original_input.upper())
            info = ticker.info
            company_name = info.get('longName', info.get('shortName', original_input.upper()))
            
            return {
                'found': True,
                'original_input': original_input,
                'symbol': original_input.upper(),
                'name': company_name,
                'resolution_method': 'direct_symbol'
            }
        
        # Step 2: Try yahooquery search (handles company names like "apple", "microsoft")
        try:
            from yahooquery import search
            print(f"Searching for: '{original_input}'")  # Debug
            
            search_results = search(original_input)
            print(f"Search results: {search_results}")  # Debug
            
            if isinstance(search_results, dict) and "quotes" in search_results and search_results["quotes"]:
                # Try the first result
                first_result = search_results["quotes"][0]
                found_symbol = first_result.get("symbol")
                
                if found_symbol:
                    validation = validate_symbol(found_symbol)
                    if validation['valid']:
                        ticker = yf.Ticker(found_symbol)
                        info = ticker.info
                        company_name = info.get('longName', info.get('shortName', found_symbol))
                        
                        return {
                            'found': True,
                            'original_input': original_input,
                            'symbol': found_symbol,
                            'name': company_name,
                            'resolution_method': 'company_name_search'
                        }
        
        except ImportError:
            print("yahooquery not installed, skipping company name search")
        except Exception as search_error:
            print(f"Search error for '{original_input}': {search_error}")
        
        # Step 3: If yahooquery fails, try a simple yfinance-based search
        # This is a fallback for common company names
        possible_symbols = [
            original_input.upper(),
            original_input.upper() + ".US",
            original_input.replace(" ", "").upper(),
        ]
        
        for test_symbol in possible_symbols:
            try:
                ticker = yf.Ticker(test_symbol)
                hist = ticker.history(period="1d")
                if not hist.empty:
                    info = ticker.info
                    # Check if this looks like the right company
                    long_name = info.get('longName', '').lower()
                    short_name = info.get('shortName', '').lower()
                    
                    if (original_input.lower() in long_name or 
                        original_input.lower() in short_name or
                        test_symbol == original_input.upper()):
                        
                        company_name = info.get('longName', info.get('shortName', test_symbol))
                        return {
                            'found': True,
                            'original_input': original_input,
                            'symbol': test_symbol,
                            'name': company_name,
                            'resolution_method': 'fallback_search'
                        }
            except:
                continue
        
        # All methods failed
        return {
            'found': False,
            'original_input': original_input,
            'symbol': None,
            'name': None,
            'error': f"Could not find valid financial data for '{original_input}'. Please try using the exact ticker symbol (e.g., 'AAPL' for Apple).",
            'resolution_method': 'failed'
        }
            
    except Exception as e:
        return {
            'found': False,
            'original_input': input_string,
            'symbol': None,
            'name': None,
            'error': f"Error resolving symbol for '{input_string}': {str(e)}",
            'resolution_method': 'error'
        }


def get_basic_info(symbol: str):
    """
    Get basic company information and key metrics
    Returns: dict with company info or None if failed
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # Try multiple methods to get info
        info = None
        try:
            info = ticker.info
        except:
            try:
                info = ticker.get_info()
            except:
                pass
        
        if not info:
            return None
            
        # Extract key metrics
        result = {
            'company_name': info.get('longName', info.get('shortName', symbol)),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'country': info.get('country', 'N/A'),
            'exchange': info.get('exchange', 'N/A'),
            'currency': info.get('currency', 'USD'),
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE') or info.get('forwardPE'),
            'eps': info.get('trailingEps'),
            'dividend_yield': info.get('dividendYield'),
            'revenue_ttm': info.get('totalRevenue'),
            'net_income_ttm': info.get('netIncomeToCommon'),
            'book_value': info.get('bookValue'),
            'price_to_book': info.get('priceToBook'),
            'debt_to_equity': info.get('debtToEquity'),
            'current_ratio': info.get('currentRatio'),
            'beta': info.get('beta'),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
            'average_volume': info.get('averageVolume'),
            'website': info.get('website'),
            'business_summary': info.get('longBusinessSummary'),
            'employees': info.get('fullTimeEmployees'),
            'profit_margin': info.get('profitMargins'),
            'operating_margin': info.get('operatingMargins'),
            'return_on_equity': info.get('returnOnEquity'),
            'return_on_assets': info.get('returnOnAssets'),
            'enterprise_value': info.get('enterpriseValue'),
            'price_to_sales': info.get('priceToSalesTrailing12Months'),
            'gross_margin': info.get('grossMargins'),
            'asset_turnover': info.get('assetTurnover'),
            'peg_ratio': info.get('pegRatio'),
            'timezone': info.get('timeZoneFullName')
        }
        
        return result
        
    except Exception as e:
        print(f"Error getting basic info for {symbol}: {e}")
        return None


def get_price_data(symbol: str, start_date=None, end_date=None, period="1y"):
    """
    Get historical price data
    Returns: DataFrame with OHLCV data or None if failed
    """
    try:
        ticker = yf.Ticker(symbol)
        
        if start_date and end_date:
            hist = ticker.history(start=start_date, end=end_date)
        else:
            hist = ticker.history(period=period)
        
        if hist.empty:
            return None
            
        return hist
        
    except Exception as e:
        print(f"Error getting price data for {symbol}: {e}")
        return None


def get_financial_statements(symbol: str):
    """
    Get financial statements (income statement, balance sheet, cash flow)
    Returns: dict with financial data or None if failed
    """
    try:
        ticker = yf.Ticker(symbol)
        result = {}
        
        # Annual financials
        try:
            financials = ticker.financials
            if financials is not None and not financials.empty:
                result['annual_financials'] = financials
        except:
            pass
        
        # Quarterly financials
        try:
            quarterly_financials = ticker.quarterly_financials
            if quarterly_financials is not None and not quarterly_financials.empty:
                result['quarterly_financials'] = quarterly_financials
        except:
            pass
        
        # Balance sheet
        try:
            balance_sheet = ticker.balance_sheet
            if balance_sheet is not None and not balance_sheet.empty:
                result['balance_sheet'] = balance_sheet
            
            # Quarterly balance sheet
            quarterly_balance_sheet = ticker.quarterly_balance_sheet
            if quarterly_balance_sheet is not None and not quarterly_balance_sheet.empty:
                result['quarterly_balance_sheet'] = quarterly_balance_sheet
        except:
            pass
        
        # Cash flow
        try:
            cashflow = ticker.cashflow
            if cashflow is not None and not cashflow.empty:
                result['cashflow'] = cashflow
            
            # Quarterly cash flow
            quarterly_cashflow = ticker.quarterly_cashflow
            if quarterly_cashflow is not None and not quarterly_cashflow.empty:
                result['quarterly_cashflow'] = quarterly_cashflow
        except:
            pass
        
        return result if result else None
        
    except Exception as e:
        print(f"Error getting financial statements for {symbol}: {e}")
        return None


def get_earnings_data(symbol: str):
    """
    Get earnings data (annual and quarterly)
    Returns: dict with earnings data or None if failed
    """
    try:
        ticker = yf.Ticker(symbol)
        result = {}
        
        # Annual earnings
        try:
            earnings = ticker.earnings
            if earnings is not None and not earnings.empty:
                result['annual_earnings'] = earnings
        except:
            pass
        
        # Quarterly earnings
        try:
            quarterly_earnings = ticker.quarterly_earnings
            if quarterly_earnings is not None and not quarterly_earnings.empty:
                result['quarterly_earnings'] = quarterly_earnings
        except:
            pass
        
        # Earnings calendar
        try:
            earnings_calendar = ticker.calendar
            if earnings_calendar is not None and not earnings_calendar.empty:
                result['earnings_calendar'] = earnings_calendar
        except:
            pass
        
        return result if result else None
        
    except Exception as e:
        print(f"Error getting earnings data for {symbol}: {e}")
        return None


def get_dividend_data(symbol: str):
    """
    Get dividend history
    Returns: Series with dividend data or None if failed
    """
    try:
        ticker = yf.Ticker(symbol)
        dividends = ticker.dividends
        
        if dividends is not None and not dividends.empty:
            return dividends
        return None
        
    except Exception as e:
        print(f"Error getting dividend data for {symbol}: {e}")
        return None


def get_revenue_and_income_trend(symbol: str):
    """
    Extract revenue and net income trend from financials
    Returns: DataFrame with Year, Revenue, Net Income columns or None if failed
    """
    try:
        financial_data = get_financial_statements(symbol)
        if not financial_data or 'annual_financials' not in financial_data:
            return None
        
        financials = financial_data['annual_financials']
        
        # Look for revenue keys
        revenue_keys = [key for key in financials.index 
                       if any(term in key.lower() for term in ['total revenue', 'revenue', 'net sales'])]
        
        # Look for net income keys
        income_keys = [key for key in financials.index 
                      if any(term in key.lower() for term in ['net income', 'net earnings'])]
        
        if not revenue_keys or not income_keys:
            return None
        
        revenue_data = financials.loc[revenue_keys[0]]
        income_data = financials.loc[income_keys[0]]
        
        # Create DataFrame
        df = pd.DataFrame({
            'Year': revenue_data.index.year,
            'Revenue': revenue_data.values,
            'Net Income': income_data.values
        }).sort_values('Year')
        
        return df
        
    except Exception as e:
        print(f"Error getting revenue and income trend for {symbol}: {e}")
        return None


def get_key_ratios(symbol: str):
    """
    Calculate and return key financial ratios
    Returns: dict with financial ratios or None if failed
    """
    try:
        info = get_basic_info(symbol)
        if not info:
            return None
        
        ratios = {}
        
        # Valuation ratios
        if info.get('pe_ratio'):
            ratios['pe_ratio'] = info['pe_ratio']
        if info.get('price_to_book'):
            ratios['price_to_book'] = info['price_to_book']
        
        # Profitability ratios
        if info.get('revenue_ttm') and info.get('net_income_ttm'):
            ratios['net_margin'] = (info['net_income_ttm'] / info['revenue_ttm']) * 100
        
        # Liquidity ratios
        if info.get('current_ratio'):
            ratios['current_ratio'] = info['current_ratio']
        
        # Leverage ratios
        if info.get('debt_to_equity'):
            ratios['debt_to_equity'] = info['debt_to_equity']
        
        # Market ratios
        if info.get('dividend_yield'):
            ratios['dividend_yield'] = info['dividend_yield'] * 100
        
        if info.get('beta'):
            ratios['beta'] = info['beta']
        
        return ratios if ratios else None
        
    except Exception as e:
        print(f"Error calculating key ratios for {symbol}: {e}")
        return None


def get_all_financial_data(input_string: str, start_date=None, end_date=None, period="1y"):
    """
    Get comprehensive financial data for a symbol or company name
    Uses improved symbol resolution to handle both symbols and company names
    Returns: dict with all available financial data
    """
    try:
        # Use improved symbol resolution
        resolution = resolve_symbol_for_financials(input_string)
        
        if not resolution['found']:
            return {'error': resolution['error']}
        
        symbol = resolution['symbol']
        company_name = resolution['name']
        original_input = resolution['original_input']
        resolution_method = resolution['resolution_method']
        
        result = {
            'search_info': {
                'original_input': original_input,
                'resolved_symbol': symbol,
                'company_name': company_name,
                'search_successful': True,
                'resolution_method': resolution_method
            }
        }
        
        # Basic info and metrics
        basic_info = get_basic_info(symbol)
        if basic_info:
            result['basic_info'] = basic_info
        
        # Price data
        price_data = get_price_data(symbol, start_date, end_date, period)
        if price_data is not None:
            result['price_data'] = price_data
            result['current_price'] = price_data['Close'].iloc[-1]
            result['price_change'] = price_data['Close'].iloc[-1] - price_data['Close'].iloc[-2] if len(price_data) > 1 else 0
            result['price_change_percent'] = ((result['price_change'] / price_data['Close'].iloc[-2]) * 100) if len(price_data) > 1 and price_data['Close'].iloc[-2] != 0 else 0
        
        # Financial statements
        financial_statements = get_financial_statements(symbol)
        if financial_statements:
            result['financial_statements'] = financial_statements
        
        # Earnings data
        earnings_data = get_earnings_data(symbol)
        if earnings_data:
            result['earnings_data'] = earnings_data
        
        # Revenue and income trend
        revenue_income_trend = get_revenue_and_income_trend(symbol)
        if revenue_income_trend is not None:
            result['revenue_income_trend'] = revenue_income_trend
        
        # Key ratios
        key_ratios = get_key_ratios(symbol)
        if key_ratios:
            result['key_ratios'] = key_ratios
        
        # Dividend data
        dividend_data = get_dividend_data(symbol)
        if dividend_data is not None:
            result['dividend_data'] = dividend_data
        
        result['data_source'] = 'Yahoo Finance'
        
        return result
        
    except Exception as e:
        return {'error': f"Error fetching financial data for '{input_string}': {str(e)}"}


def get_quick_financial_summary(input_string: str):
    """
    Get a quick financial summary using improved symbol resolution
    Returns: dict with key financial metrics
    """
    try:
        resolution = resolve_symbol_for_financials(input_string)
        if not resolution['found']:
            return {'error': resolution['error']}
        
        symbol = resolution['symbol']
        
        # Get basic info and price data
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="5d")
        
        if hist.empty:
            return {'error': f"No price data available for {symbol}"}
        
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        price_change = current_price - prev_price
        price_change_percent = (price_change / prev_price * 100) if prev_price != 0 else 0
        
        return {
            'search_info': {
                'original_input': input_string,
                'resolved_symbol': symbol,
                'company_name': resolution['name'],
                'resolution_method': resolution['resolution_method']
            },
            'price_info': {
                'current_price': round(current_price, 2),
                'price_change': round(price_change, 2),
                'price_change_percent': round(price_change_percent, 2),
                'currency': info.get('currency', 'USD')
            },
            'key_metrics': {
                'market_cap': format_large_number(info.get('marketCap')),
                'pe_ratio': info.get('trailingPE'),
                'dividend_yield': format_percentage(info.get('dividendYield', 0) * 100) if info.get('dividendYield') else "N/A",
                'beta': info.get('beta'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow')
            }
        }
        
    except Exception as e:
        return {'error': f"Error getting financial summary for '{input_string}': {str(e)}"}


def format_large_number(value):
    """
    Format large numbers for display (e.g., 1.5B, 234.5M)
    """
    if value is None:
        return "N/A"
    
    try:
        value = float(value)
        if value >= 1e12:
            return f"${value/1e12:.2f}T"
        elif value >= 1e9:
            return f"${value/1e9:.2f}B"
        elif value >= 1e6:
            return f"${value/1e6:.2f}M"
        elif value >= 1e3:
            return f"${value/1e3:.1f}K"
        else:
            return f"${value:.0f}"
    except:
        return "N/A"


def format_percentage(value):
    """
    Format percentage values for display
    """
    if value is None:
        return "N/A"
    
    try:
        return f"{float(value):.2f}%"
    except:
        return "N/A"


# Test function
def test_symbol_resolution():
    """
    Test the improved symbol resolution
    """
    test_cases = [
        "apple",      # Company name lowercase
        "APPLE",      # Company name uppercase
        "Apple",      # Company name title case
        "AAPL",       # Direct symbol
        "tesla",      # Another company name
        "TSLA",       # Another direct symbol
    ]
    
    print("Testing Symbol Resolution:")
    print("=" * 50)
    
    for test in test_cases:
        print(f"\nTesting: '{test}'")
        print("-" * 30)
        
        resolution = resolve_symbol_for_financials(test)
        if resolution['found']:
            print(f"✅ Success: '{resolution['original_input']}' → {resolution['symbol']} ({resolution['name']})")
            print(f"   Method: {resolution['resolution_method']}")
        else:
            print(f"❌ Failed: {resolution['error']}")


if __name__ == "__main__":
    test_symbol_resolution()