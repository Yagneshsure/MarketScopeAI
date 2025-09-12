import streamlit as st
import pandas as pd
import plotly.express as px
from fetchers.news import fetch_news, analyze_sentiment

def render_news_sentiment(company_name: str):
    st.subheader("📰 News & Sentiment")

    try:
        # Fetch and analyze news
        articles = fetch_news(company_name, page_size=20)
        articles = analyze_sentiment(articles)
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return

    if not articles:
        st.warning("No news found for this company.")
        return

    # Convert to DataFrame
    df = pd.DataFrame([{
        "Title": a.get("title", ""),
        "Source": a.get("source", {}).get("name", ""),
        "Date": a.get("publishedAt", "")[:10],
        "Sentiment": a.get("sentiment", "Neutral"),
        "Score": a.get("sentiment_score", 0),
        "URL": a.get("url", "")
    } for a in articles])

    # --- Highlight Top Headlines ---
    st.markdown("### 🌟 Highlights")
    top_pos = df[df["Sentiment"] == "Positive"].sort_values(by="Score", ascending=False).head(1)
    top_neg = df[df["Sentiment"] == "Negative"].sort_values(by="Score").head(1)

    if not top_pos.empty:
        st.success(f"📈 Positive Highlight: [{top_pos.iloc[0]['Title']}]({top_pos.iloc[0]['URL']})")
    if not top_neg.empty:
        st.error(f"📉 Negative Highlight: [{top_neg.iloc[0]['Title']}]({top_neg.iloc[0]['URL']})")

    # --- 📊 Charts ---
    col1, col2 = st.columns(2)

    with col1:
        fig_pie = px.pie(
            df, 
            names="Sentiment", 
            title="Sentiment Distribution",
            color="Sentiment", 
            color_discrete_map={"Positive":"green","Negative":"red","Neutral":"gray"}
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_bar = px.bar(
            df, x="Date", y="Score", color="Sentiment",
            title="Sentiment Over Time",
            hover_data=["Title", "Source"],
            color_discrete_map={"Positive":"green","Negative":"red","Neutral":"gray"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- 📊 Insights ---
    st.markdown("### 📌 Quick Insight")
    pos, neg, neu = (
        df["Sentiment"].value_counts().get("Positive", 0),
        df["Sentiment"].value_counts().get("Negative", 0),
        df["Sentiment"].value_counts().get("Neutral", 0),
    )
    if pos > neg and pos > neu:
        st.success("Most recent articles are **Positive** ✅ – market sentiment is favorable.")
    elif neg > pos and neg > neu:
        st.error("Most recent articles are **Negative** ⚠️ – cautious outlook.")
    else:
        st.info("Most articles are **Neutral** – no strong sentiment trend.")

    st.markdown("---")
    st.markdown("### 📰 Latest Articles")

    # --- Filter Toggle ---
    sentiment_filter = st.multiselect(
        "Filter by Sentiment:",
        options=["Positive", "Negative", "Neutral"],
        default=["Positive", "Negative", "Neutral"]
    )
    filtered_df = df[df["Sentiment"].isin(sentiment_filter)]

    # --- 📰 Styled Article Cards ---
    for _, row in filtered_df.iterrows():
        sentiment_icon = {"Positive": "🟢", "Negative": "🔴", "Neutral": "⚪"}
        st.markdown(
            f"""
            <div style="background-color:#f8f9fa; padding:14px; border-radius:10px; 
                        margin-bottom:12px; box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                <div style="font-size:18px; font-weight:700; color:#000;">
                    {sentiment_icon.get(row['Sentiment'], '⚪')} {row['Title']}
                </div>
                <div style="font-size:13px; color:#555; margin-top:6px;">
                    Source: {row['Source']} • 📅 {row['Date']}
                </div>
                <div style="font-size:14px; margin-top:6px; font-weight:600; color:#333;">
                    Sentiment: {row['Sentiment']} (Score: {row['Score']:.2f})
                </div>
                <div style="margin-top:8px;">
                    <a href="{row['URL']}" target="_blank" style="color:#0a66c2; text-decoration:none;">
                        🔗 Read Full Article
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


