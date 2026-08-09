import os, requests
from dotenv import load_dotenv

load_dotenv()

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
    json={
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": "what is the capital of india?"}]
    }
)
print(response.json()["choices"][0]["message"]["content"])