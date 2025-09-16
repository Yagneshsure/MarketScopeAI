import requests
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load API key (set this in your .env or Streamlit secrets)
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

def fetch_news(company: str, language="en", page_size=10):
    """
    Fetch latest news articles about the company using NewsAPI.
    """
    if not NEWS_API_KEY:
        raise ValueError("❌ NEWS_API_KEY is missing. Set it in environment or Streamlit secrets.")

    url = f"https://newsapi.org/v2/everything?q={company}&language={language}&sortBy=publishedAt&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        return []

    return data.get("articles", [])


def analyze_sentiment(articles):
    """
    Run sentiment analysis on article headlines using VADER.
    Adds sentiment score & label.
    """
    sia = SentimentIntensityAnalyzer()
    for article in articles:
        title = article.get("title", "")
        score = sia.polarity_scores(title)
        article["sentiment_score"] = score["compound"]
        if score["compound"] >= 0.05:
            article["sentiment"] = "Positive"
        elif score["compound"] <= -0.05:
            article["sentiment"] = "Negative"
        else:
            article["sentiment"] = "Neutral"
    return articles
