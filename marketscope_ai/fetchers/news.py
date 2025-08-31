import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def fetch_news_and_sentiment(ticker):
    url = f"https://www.google.com/search?q={ticker}+stock+news&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_items = []

    for item in soup.select("div.dbsr")[:5]:  # Get top 5 news
        title = item.select_one("div.JheGif.nDgy9d").text if item.select_one("div.JheGif.nDgy9d") else "No Title"
        link = item.a["href"] if item.a else "#"
        snippet = item.select_one("div.Y3v8qd").text if item.select_one("div.Y3v8qd") else ""

        sentiment_score = analyzer.polarity_scores(title + " " + snippet)["compound"]
        sentiment = "Positive" if sentiment_score > 0.05 else "Negative" if sentiment_score < -0.05 else "Neutral"

        news_items.append({
            "title": title,
            "link": link,
            "snippet": snippet,
            "sentiment": sentiment,
            "score": sentiment_score
        })

    return news_items
