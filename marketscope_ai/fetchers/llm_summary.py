# fetchers/llm_summary.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_llm_summary(company_name, description, financials, news, summary_style, model="openai/gpt-4o-mini"):
    """
    Generate an AI-powered summary for a company using OpenRouter API.
    """

    if not OPENROUTER_API_KEY:
        raise ValueError("⚠️ Missing OpenRouter API key. Please check your .env file.")

    # Build prompt
    prompt = f"""
    You are a financial analyst AI.
    
    Company: {company_name}

    --- Company Overview ---
    {description}

    --- Financial Highlights ---
    {financials}

    --- Recent News ---
    {news}

    Task: Provide a {summary_style} of this company. 
    Keep it clear, concise, and structured.
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]
