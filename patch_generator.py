import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from tools.code_search import read_file


load_dotenv()

def call_llm(prompt: str) -> str:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
        
        json={
            "model": "openai/gpt-oss-120b",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0
        }
    )
    data = response.json()
    if "choices" not in data:
        print("=== GROQ API ERROR ===")
        print("Status code:", response.status_code)
        print("Response:", data)
        raise RuntimeError(f"Groq API call failed: {data}")
    return data["choices"][0]["message"]["content"]