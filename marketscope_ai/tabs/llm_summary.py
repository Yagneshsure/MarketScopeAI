# tabs/llm.py

import streamlit as st
from fetchers.llm_summary import generate_summary

# -------------------------
# Streamlit LLM Tab
# -------------------------

def render_llm_summary(company_info=None, finance_info=None, technical_info=None):
    st.header("🧠 AI-Powered Stock Summary")

    # Select Provider
    provider = st.selectbox("Choose LLM Provider", ["Groq", "HuggingFace", "OpenRouter", "OpenAI"], index=0)

    # Summarize Company Description
    st.subheader("📜 Company & Market Overview")
    if company_info:
        summary = generate_summary(f"Summarize the following company profile:\n\n{company_info}", provider)
        st.info(summary)
    else:
        st.warning("⚠️ No company description found to summarize.")

    # Summarize Financials
    ## 
    st.subheader("💰 Financial Insights")
    if finance_info:
        summary = generate_summary(f"Summarize these financial metrics:\n\n{finance_info}", provider)
        st.success(summary)
    else:
        st.warning("⚠️ No financial data available.")

    # Summarize Technicals
    st.subheader("📊 Technical Analysis Insights")
    if technical_info:
        summary = generate_summary(f"Summarize the following technical indicators:\n\n{technical_info}", provider)
        st.info(summary)
    else:
        st.warning("⚠️ No technical data available.")

    # Ask AI Section
    st.subheader("💬 Ask AI Anything")
    user_q = st.text_area("Type your question about this stock:")
    if st.button("Generate Answer"):
        if user_q.strip():
            answer = generate_summary(user_q, provider)
            st.markdown(f"**AI Answer:**\n\n{answer}")
        else:
            st.warning("Please enter a question to ask the AI.")
####

