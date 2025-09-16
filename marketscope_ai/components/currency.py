import os
import requests
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_RATE_API = os.getenv("EXCHANGE_RATE_API")

EXCHANGE_CURRENCY_MAP = {
    "NSE": "INR",   # India
    "BSE": "INR",   # India
    "NYSE": "USD",  # USA
    "NASDAQ": "USD",  # USA
    "LSE": "GBP",   # London
    "TSE": "JPY",   # Tokyo
    "SSE": "CNY",   # Shanghai
    "HKEX": "HKD",  # Hong Kong
    "ASX": "AUD",   # Australia
    "TSX": "CAD",   # Canada
}

def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """
    Fetch exchange rate using ExchangeRate API.
    """
    if from_currency.upper() == to_currency.upper():
        return 1.0  # no conversion needed
    
    try:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API}/pair/{from_currency}/{to_currency}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and "conversion_rate" in data:
            return data["conversion_rate"]

        print(f"⚠️ ExchangeRate API error: {data}")
        return 1.0

    except Exception as e:
        print(f"❌ Error fetching exchange rate: {e}")
        return 1.0

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Convert currency using exchange rate.
    """
    rate = get_exchange_rate(from_currency, to_currency)
    return round(amount * rate, 2)  # always round to 2 decimals

def detect_currency_from_exchange(exchange: str) -> str:
    """
    Detect currency based on stock exchange.
    Defaults to USD if exchange is not mapped.
    """
    return EXCHANGE_CURRENCY_MAP.get(exchange.upper(), "USD")
