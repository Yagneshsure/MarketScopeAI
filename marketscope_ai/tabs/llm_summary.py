# marketscope_ai/tabs/llm_summary.py
import streamlit as st
import json
import textwrap
from typing import Any, Dict, List, Optional

# local fetcher that calls the HF inference API (you already have this)
from fetchers.llm_summary import call_huggingface

# fallbacks (only used if caller doesn't pass data)
from fetchers.financials import get_financial_statements
from fetchers.news import fetch_news


def _to_text(obj: Any, max_chars: int = 4000) -> str:
    """Convert common objects (DataFrame/dict/list) into a concise text representation."""
    try:
        # pandas DataFrame or Series
        import pandas as pd
        if isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series):
            s = obj.head(6).to_dict()
            txt = json.dumps(s, default=str, indent=2)
            return txt[:max_chars]
    except Exception:
        pass

    # list of news dicts: extract headlines + source + date (if possible)
    if isinstance(obj, list):
        lines = []
        for i, it in enumerate(obj[:10]):  # limit items
            if isinstance(it, dict):
                title = it.get("title") or it.get("headline") or it.get("summary") or it.get("text") or ""
                src = (it.get("source") or {}).get("name") if isinstance(it.get("source"), dict) else it.get("source", "")
                date = it.get("publishedAt") or it.get("date") or ""
                lines.append(f"- {title} ({src} {date})".strip())
            else:
                lines.append(f"- {str(it)[:200]}")
        return "\n".join(lines)[:max_chars]

    # dict -> pretty JSON
    if isinstance(obj, dict):
        try:
            return json.dumps(obj, default=str, indent=2)[:max_chars]
        except Exception:
            return str(obj)[:max_chars]

    # fallback to str
    return str(obj)[:max_chars]


def _safe_json_parse(text: str) -> Optional[Dict]:
    """
    Try to parse a model response into JSON. Robust to extra text around JSON by extracting
    the first {...} block. Returns dict on success, else None.
    """
    if not isinstance(text, str):
        # sometimes the helper returns a dict already
        if isinstance(text, dict):
            return text
        try:
            return json.loads(text)
        except Exception:
            return None

    # quick attempt
    try:
        return json.loads(text)
    except Exception:
        # try to find the first { ... } and parse substring
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = text[start:end + 1]
            try:
                return json.loads(candidate)
            except Exception:
                pass
    return None


def render_llm_summary(
    symbol: str,
    financials: Any = None,
    news: Any = None,
    model_default: str = "google/flan-t5-large",
) -> Optional[Dict]:
    """
    Render the LLM Summary tab.

    Args:
        symbol: ticker or company name
        financials: (optional) pre-fetched financials object (dict / DataFrame)
        news: (optional) pre-fetched news list
        model_default: default HF model to call

    Returns:
        parsed_summary dict if generation succeeded (also displayed in UI), else None
    """
    st.header("🧠 LLM-Generated Summary")

    # If caller didn't pass financials/news, fetch them as fallback so function is flexible
    if financials is None:
        try:
            financials = get_financial_statements(symbol)
        except Exception as e:
            financials = {"error": f"Failed to fetch financials: {e}"}

    if news is None:
        try:
            news = fetch_news(symbol)
        except Exception as e:
            news = [{"error": f"Failed to fetch news: {e}"}]

    # --- UI controls ---
    style_map = {
        "Analyst-style": "Write a concise professional analyst-style summary focused on financial performance, valuation cues, and risks.",
        "Investor-style": "Write a practical investor-style summary: focus on what retail investors should know (growth, revenue, risks).",
        "Beginner-friendly": "Explain the company's situation in very simple words for a non-expert audience.",
        "News-driven": "Focus on the latest news and its likely impact on the stock (short-term sentiment).",
    }

    style = st.selectbox("Choose summary style", list(style_map.keys()), index=0)
    model = st.selectbox("Choose Hugging Face model", [model_default, "mistralai/Mixtral-8x7B-Instruct-v0.1"], index=0)

    max_tokens = st.slider("Max tokens for generation (model may ignore)", 100, 1500, 400)

    # Prepare compact textual payloads
    fin_text = _to_text(financials, max_chars=3000)
    news_text = _to_text(news, max_chars=3000)

    st.markdown("**Preview of data used (truncated):**")
    with st.expander("🔎 Financials preview"):
        st.code(fin_text[:2000], language="json")
    with st.expander("📰 News preview"):
        st.code(news_text[:2000])

    # Button to generate
    if st.button("✨ Generate AI Summary"):
        # Build a prompt that asks the model to output strict JSON
        prompt = textwrap.dedent(f"""
        You are a professional financial assistant. Produce a JSON object (no extra commentary)
        with the exact keys: "overview", "financial_highlights", "news_summary",
        "sentiment", "perspective", "recommendation", "key_bullets".

        - overview: 2-3 sentence executive summary.
        - financial_highlights: plain-English summary of key financials (revenue, profit, growth, risks).
        - news_summary: short bullets of the most important recent news and their impact.
        - sentiment: one of "Bullish", "Bearish", or "Neutral".
        - perspective: short (2-3 lines) reasoning supporting the sentiment.
        - recommendation: one of "Buy", "Hold", "Sell" (only one word).
        - key_bullets: list of 3-6 short bullet points with the most important takeaways.

        Style requirement: {style_map[style]}

        Company: {symbol}

        FINANCIALS (raw, truncated):
        {fin_text}

        NEWS (truncated):
        {news_text}

        Return ONLY a valid JSON object. Do not add extra text outside the JSON.
        """).strip()

        with st.spinner(f"🤖 Generating AI summary using {model}..."):
            # call_huggingface returns a string (or error string)
            result = call_huggingface(prompt, model=model)

        # Handle obvious error responses from call_huggingface
        if isinstance(result, str) and result.startswith("❌"):
            st.error(result)
            return {"error": result}

        # Try to parse JSON
        parsed = _safe_json_parse(result)
        if parsed is None:
            # Attempt a second-pass: ask the model to reformat into JSON if it returned plain text
            st.warning("Model output could not be parsed as JSON. Showing raw output and offering a reformat attempt.")
            with st.expander("Raw model output"):
                st.code(result)

            # Ask the model to return only JSON based on previous output
            re_prompt = textwrap.dedent(f"""
            The previous response could not be parsed as JSON. Convert the following text into a JSON object
            matching this schema: overview, financial_highlights, news_summary, sentiment, perspective, recommendation, key_bullets.

            Text to convert:
            {result}

            Return ONLY the JSON object (no commentary).
            """).strip()

            with st.spinner("🔁 Asking model to reformat into JSON..."):
                re_result = call_huggingface(re_prompt, model=model)

            parsed = _safe_json_parse(re_result)
            if parsed is None:
                st.error("Unable to parse model output into JSON. See raw output below.")
                with st.expander("Final raw model output (unparsed)"):
                    st.code(re_result)
                return {"error": "unparsed_response", "raw": re_result}

        # Normalized parsed output: ensure keys exist
        def _get(k, default=""):
            return parsed.get(k) if isinstance(parsed, dict) else default

        overview = _get("overview", "")
        financial_highlights = _get("financial_highlights", "")
        news_summary = _get("news_summary", "")
        sentiment = _get("sentiment", "")
        perspective = _get("perspective", "")
        recommendation = _get("recommendation", "")
        key_bullets = _get("key_bullets", []) or []

        # --- UI Display ---
        st.subheader("📌 AI Summary (structured)")

        # Sentiment badge + recommendation
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Overview:** {overview}")
        with col2:
            # sentiment box
            sentiment_display = sentiment or "N/A"
            st.metric(label="Sentiment", value=sentiment_display, delta=recommendation or "")

        # Expanders for each section
        with st.expander("📜 Company Overview"):
            st.write(overview)

        with st.expander("💰 Financial Highlights"):
            st.write(financial_highlights or "No financial highlights produced by model.")
            if isinstance(financials, dict) or (hasattr(financials, "to_dict")):
                with st.expander("🔢 Raw Financials (truncated)"):
                    try:
                        # show compact raw financials
                        st.json(json.loads(_to_text(financials, max_chars=2000)))
                    except Exception:
                        st.code(_to_text(financials, max_chars=2000))

        with st.expander("📰 News & Sentiment Recap"):
            st.write(news_summary or "No news summary produced.")
            if isinstance(news, list):
                st.write("Showing top news items provided to the model:")
                for i, item in enumerate(news[:6]):
                    if isinstance(item, dict):
                        title = item.get("title") or item.get("headline") or ""
                        src = (item.get("source") or {}).get("name") if isinstance(item.get("source"), dict) else item.get("source", "")
                        st.markdown(f"- **{title}** — {src}")
                    else:
                        st.markdown(f"- {str(item)[:200]}")

        with st.expander("🎯 AI Perspective & Recommendation"):
            st.write(perspective or "No perspective generated.")
            st.write(f"**Recommendation:** {recommendation or 'N/A'}")

        with st.expander("🔎 Key Bullets"):
            if isinstance(key_bullets, list):
                for b in key_bullets:
                    st.markdown(f"- {b}")
            else:
                st.write(key_bullets)

        # show raw model output for debugging
        with st.expander("🧾 Raw Model Output"):
            st.code(result)

        # Return parsed dict so caller can reuse programmatically
        parsed_result = {
            "overview": overview,
            "financial_highlights": financial_highlights,
            "news_summary": news_summary,
            "sentiment": sentiment,
            "perspective": perspective,
            "recommendation": recommendation,
            "key_bullets": key_bullets,
            "raw_model_output": result,
        }
        return parsed_result

    # If user hasn't clicked "Generate", still return None for programmatic calls
    return None
