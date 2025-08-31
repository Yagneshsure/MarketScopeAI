import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import os

analyzer = SentimentIntensityAnalyzer()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Store this in your .env

def fetch_news_and_sentiment(symbol, days=7):
    query = f"{symbol} stock"
    url = (
        f"https://newsapi.org/v2/everything?q={query}&language=en&"
        f"sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)

    if response.status_code != 200:
        return pd.DataFrame()

    articles = response.json().get("articles", [])
    results = []

    for article in articles:
        title = article["title"]
        source = article["source"]["name"]
        published = article["publishedAt"]
        url = article["url"]
        score = analyzer.polarity_scores(title)["compound"]
        if score > 0.2:
            sentiment = "Positive"
        elif score < -0.2:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        results.append({
            "Title": title,
            "Source": source,
            "Published": published,
            "Sentiment": sentiment,
            "Score": round(score, 2),
            "URL": url
        })

    return pd.DataFrame(results)
