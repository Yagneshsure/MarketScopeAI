# import os
# from dotenv import load_dotenv
# import openai

# # Load environment variables
# load_dotenv()

# # Set your OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def ask_company_ai(user_query):
#     if not openai.api_key:
#         return "❌ OpenAI API key not found in environment."

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # You can use "gpt-4" if available
#             messages=[
#                 {"role": "system", "content": "You are a helpful AI assistant that provides financial and business-related insights."},
#                 {"role": "user", "content": user_query}
#             ],
#             max_tokens=300,
#             temperature=0.7,
#         )
#         return response['choices'][0]['message']['content'].strip()

#     except openai.error.AuthenticationError as e:
#         return f"❌ Authentication error: {e}"
#     except openai.error.OpenAIError as e:
#         return f"⚠️ OpenAI API Error: {e}"
#     except Exception as e:
#         return f"⚠️ Unexpected Error: {str(e)}"


# ask_ai.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def ask_ai(prompt, model="llama3-70b-8192"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful financial analyst and assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {e}"
