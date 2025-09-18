# marketscope_ai/fetchers/llm_summary.py
from transformers import pipeline

# Initialize Hugging Face pipelines
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
sentiment_analyzer = pipeline("sentiment-analysis")

def generate_summary(text: str, max_length: int = 130, min_length: int = 30) -> str:
    """Generate a concise summary of text."""
    if not text.strip():
        return "⚠️ No text provided for summarization."
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        return f"❌ Error generating summary: {e}"

def analyze_sentiment(text: str) -> str:
    """Classify sentiment as Bullish, Bearish, or Neutral."""
    if not text.strip():
        return "Neutral"
    try:
        result = sentiment_analyzer(text[:512])[0]  # limit tokens for safety
        label = result["label"]
        if label == "POSITIVE":
            return "Bullish 📈"
        elif label == "NEGATIVE":
            return "Bearish 📉"
        else:
            return "Neutral ⚖️"
    except Exception as e:
        return f"❌ Error in sentiment: {e}"

def generate_custom_summary(company: str, financials: str, news: str, style: str) -> dict:
    """
    Generate a multi-section AI summary for a company.
    Returns dict with overview, financials, news, sentiment, perspective.
    """
    # Combine inputs
    combined_text = f"""
    Company: {company}
    Financials: {financials}
    News: {news}
    """

    # Generate different parts
    overview = generate_summary(f"{company} overview: {financials} {news}")
    financial_summary = generate_summary(financials)
    news_summary = generate_summary(news)
    sentiment = analyze_sentiment(news + " " + financials)

    # Adjust tone/style
    if style == "Analyst":
        perspective = f"As an analyst, the outlook for {company} is {sentiment}."
    elif style == "Investor":
        perspective = f"From an investor’s perspective, {company} shows {sentiment} trends."
    else:  # News style
        perspective = f"Recent coverage suggests a {sentiment} stance for {company}."

    return {
        "overview": overview,
        "financials": financial_summary,
        "news": news_summary,
        "sentiment": sentiment,
        "perspective": perspective,
        "raw_text": combined_text,
    }
