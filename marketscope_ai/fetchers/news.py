# # import os
# # import requests
# # from dotenv import load_dotenv
# # from textblob import TextBlob
# # import time
# # import tqdm

# # # Load environment variables
# # load_dotenv()
# # NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# # def fetch_company_news(symbol: str, language: str = "en", page_size: int = 5):
# #     """
# #     Fetch latest company news from NewsAPI.
# #     """
# #     if not NEWS_API_KEY:
# #         raise ValueError("NEWS_API_KEY not found in environment variables.")

# #     url = "https://newsapi.org/v2/everything"
# #     params = {
# #         "q": symbol,
# #         "language": language,
# #         "pageSize": page_size,
# #         "sortBy": "publishedAt",
# #         "apiKey": NEWS_API_KEY
# #     }

# #     response = requests.get(url, params=params)
# #     response.raise_for_status()
# #     data = response.json()

# #     return data.get("articles", [])

# # def analyze_sentiment(text: str) -> str:
# #     """
# #     Perform simple sentiment analysis using TextBlob.
# #     Returns: Positive, Negative, Neutral
# #     """
# #     if not text.strip():
# #         return "N/A"

# #     polarity = TextBlob(text).sentiment.polarity
# #     if polarity > 0.05:
# #         return "Positive"
# #     elif polarity < -0.05:
# #         return "Negative"
# #     else:
# #         return "Neutral"



# import os
# import requests
# from dotenv import load_dotenv
# from textblob import TextBlob

# # Load environment variables
# load_dotenv()
# NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# def fetch_company_news(symbol: str, language: str = "en", page_size: int = 5):
#     """
#     Fetch latest company news from NewsAPI.
#     """
#     if not NEWS_API_KEY:
#         raise ValueError("NEWS_API_KEY not found in environment variables.")

#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": symbol,
#         "language": language,
#         "pageSize": page_size,
#         "sortBy": "publishedAt",
#         "apiKey": NEWS_API_KEY
#     }

#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     data = response.json()

#     return data.get("articles", [])


# def analyze_sentiment(text: str):
#     """
#     Perform sentiment analysis using TextBlob.
#     Returns: (label, percentage)
#     """
#     if not text.strip():
#         return "N/A", 0

#     polarity = TextBlob(text).sentiment.polarity
#     percentage = round(abs(polarity) * 100, 1)  # convert polarity to percentage

#     if polarity > 0.05:
#         return "Positive", percentage
#     elif polarity < -0.05:
#         return "Negative", percentage
#     else:
#         return "Neutral", percentage


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
