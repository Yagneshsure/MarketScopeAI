# tabs/llm_summary.py

import streamlit as st
from fetchers.stocks import get_stock_info
from fetchers.financials import get_all_financial_data
from fetchers.news import fetch_news, analyze_sentiment
from fetchers.llm_summary import generate_llm_summary


def render_llm_summary(symbol: str):
    """Render the LLM-based summary tab for a given stock/asset symbol."""
    st.subheader("🧠 LLM-Generated Summary")

    # --- User controls ---
    col1, col2 = st.columns(2)

    with col1:
        summary_style = st.selectbox(
            "Choose summary style",
            ["Executive Summary", "Analyst-style Summary", "Investor Brief"],
            index=0
        )

    with col2:
        model_choice = st.selectbox(
            "Choose AI model (via OpenRouter)",
            [
                "openai/gpt-4o-mini",
                "anthropic/claude-3.5-sonnet",
                "meta-llama/llama-3.1-8b-instruct",
                "mistralai/mistral-7b-instruct"
            ],
            index=0
        )

    # --- Fetch company data ---
    try:
        company_info = get_stock_info(symbol)
    except Exception:
        company_info = {"longName": symbol, "longBusinessSummary": "⚠️ Company info not available."}

    try:
        financials = get_all_financial_data(symbol)
    except Exception:
        financials = {}

    try:
        news_articles = fetch_news(symbol, page_size=5)
        news_articles = analyze_sentiment(news_articles)
    except Exception:
        news_articles = []

    # Prepare context
    description = company_info.get("longBusinessSummary", "No description available.")
    fin_data = str(financials)[:2000]  # truncate to avoid token overload
    news_data = " | ".join([a.get("title", "") for a in news_articles[:5]])

    # --- Generate summary ---
    if st.button("✨ Generate AI Summary", use_container_width=True):
        with st.spinner("Generating AI summary..."):
            try:
                summary = generate_llm_summary(
                    company_name=company_info.get("longName", symbol),
                    description=description,
                    financials=fin_data,
                    news=news_data,
                    summary_style=summary_style,
                    model=model_choice
                )
                st.success("✅ Summary generated successfully!")
                st.markdown("### 📜 AI Summary")
                st.write(summary)

            except Exception as e:
                st.error(f"Error generating summary: {e}")

    # --- Optional raw data expander ---
    with st.expander("📂 Raw Data Used for Summary"):
        st.write("**Company Description:**")
        st.write(description)

        st.write("**Financials (truncated):**")
        st.json(financials)

        st.write("**Recent News Headlines:**")
        for a in news_articles[:5]:
            st.write(f"- {a.get('title', '')}")
