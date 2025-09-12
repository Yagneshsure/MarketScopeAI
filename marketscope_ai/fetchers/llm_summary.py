# fetchers/llm_fetchers.py

import os
import requests

# Load API keys from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# -------------------------
# LLM API Call Functions
# -------------------------

def call_groq(prompt: str):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"].strip()


def call_huggingface(prompt: str):
    url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt, "parameters": {"max_length": 300}}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()[0]["summary_text"]


def call_openrouter(prompt: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"].strip()


def call_openai(prompt: str):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def generate_summary(prompt: str, provider: str):
    try:
        if provider == "Groq":
            return call_groq(prompt)
        elif provider == "HuggingFace":
            return call_huggingface(prompt)
        elif provider == "OpenRouter":
            return call_openrouter(prompt)
        elif provider == "OpenAI":
            return call_openai(prompt)
        else:
            return "⚠️ Unsupported LLM provider selected."
    except Exception as e:
        return f"⚠️ Error generating summary: {e}"
