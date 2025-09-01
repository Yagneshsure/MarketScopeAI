import yfinance as yf

# Map exchange suffix to default currency
EXCHANGE_CURRENCY_MAP = {
    ".NS": "INR",   # NSE India
    ".BO": "INR",   # BSE India
    ".T": "JPY",    # Tokyo
    ".L": "GBP",    # London
    ".HK": "HKD",   # Hong Kong
    ".SS": "CNY",   # Shanghai
    ".SZ": "CNY",   # Shenzhen
    ".TO": "CAD",   # Toronto
    ".AX": "AUD",   # Australia
    ".SA": "BRL",   # Brazil
    ".TW": "TWD",   # Taiwan
    ".KS": "KRW",   # Korea
    # Add more as needed
}

def detect_currency_from_symbol(symbol: str) -> str:
    """Detect default trading currency based on symbol suffix."""
    for suffix, currency in EXCHANGE_CURRENCY_MAP.items():
        if symbol.endswith(suffix):
            return currency
    return "USD"  # Default if no suffix found (e.g., US tickers)

def get_stock_price(symbol: str, base_currency: str = "USD"):
    """
    Get stock price and convert into base currency (default USD).
    """
    ticker = yf.Ticker(symbol)
    info = ticker.info
    price = info.get("currentPrice")
    
    if not price:
        return None, None

    stock_currency = info.get("currency") or detect_currency_from_symbol(symbol)

    # If already in base currency, return
    if stock_currency == base_currency:
        return price, stock_currency

    # Else convert
    fx_symbol = f"{stock_currency}{base_currency}=X"
    fx_data = yf.Ticker(fx_symbol).history(period="1d")

    if not fx_data.empty:
        fx_rate = fx_data["Close"].iloc[-1]
        converted_price = price * fx_rate
        return converted_price, base_currency

    return price, stock_currency
