import os
import requests

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "hf_xxx")  # replace hf_xxx with your real key
print("HF API Key loaded:", HF_API_KEY[:10] + "...")

# Use a lightweight model
API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

payload = {"inputs": "The stock market today is"}

try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    print("✅ Response received:")
    print(data)
except requests.exceptions.Timeout:
    print("❌ Error: Request timed out.")
except requests.exceptions.RequestException as e:
    print(f"❌ Error: {e}")
