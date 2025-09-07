import os
import requests
from dotenv import load_dotenv
from textblob import TextBlob


# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_company_news(symbol: str, language: str = "en", page_size: int = 5):
    """
    Fetch latest company news from NewsAPI.
    """
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not found in environment variables.")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": symbol,
        "language": language,
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return data.get("articles", [])

def analyze_sentiment(text: str) -> str:
    """
    Perform simple sentiment analysis using TextBlob.
    Returns: Positive, Negative, Neutral
    """
    if not text.strip():
        return "N/A"

    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.05:
        return "Positive"
    elif polarity < -0.05:
        return "Negative"
    else:
        return "Neutral"
