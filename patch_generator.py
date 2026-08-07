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
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0
        }
    )
    return response.json()["choices"][0]["message"]["content"]

def generate_patch(repo_path: Path, file_path: str, issue_description: str) -> str:
    """Given a file and an issue, ask the LLM to propose a fixed version of the file."""
    original_code = read_file(repo_path, file_path)

    prompt = f"""You are a coding agent fixing a bug.

ISSUE:
{issue_description}

FILE: {file_path}
CURRENT CONTENT:
{original_code}

Return ONLY the complete fixed version of this file. No explanations, no markdown fences, just the raw code."""

    return call_llm(prompt)