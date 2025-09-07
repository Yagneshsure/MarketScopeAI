import streamlit as st
from fetchers.news import fetch_company_news, analyze_sentiment


def render_news(symbol: str):
    st.header("📰 News & Sentiment")

    if not symbol:
        st.info("Enter a stock symbol in the sidebar to fetch related news.")
        return

    try:
        news_list = fetch_company_news(symbol)

        if not news_list:
            st.warning("No recent news found for this symbol.")
            return

        for article in news_list:
            title = article.get("title", "No Title")
            source = article.get("source", {}).get("name", "Unknown")
            published = article.get("publishedAt", "Unknown")
            description = article.get("description", "")

            # Analyze sentiment for each article
            sentiment = analyze_sentiment(title + " " + description)

            st.markdown(f"**{title}**")
            st.caption(f"{source} — {published}")
            if description:
                st.write(description)
            st.write(f"**Sentiment:** {sentiment}")
            st.divider()

    except Exception as e:
        st.error(f"Error fetching news: {e}")
