import requests
import json

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}
payload = {
    "model": "llama3-70b-8192",
    "messages": [{"role": "user", "content": "Tell me a joke about finance."}],
    "temperature": 0.7
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json()["choices"][0]["message"]["content"])

print("Using model:", model_name)

