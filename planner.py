from patch_generator import call_llm

def generate_plan(file_path: str, original_code: str, issue_description: str, memory_context: str = "") -> str:
    """Ask the LLM to reason about the bug and propose an approach, without writing code yet."""
    prompt = f"""You are a coding agent analyzing a bug before fixing it.

ISSUE:
{issue_description}

FILE: {file_path}
CURRENT CONTENT:
{original_code}
{memory_context}

Do NOT write code yet. Instead, briefly explain:
1. What is actually wrong (root cause, not just symptom)
2. What the correct fix should be (describe the approach in plain English)
3. What you must NOT change (parts of the file that are unrelated and should stay untouched)

Keep this to a few sentences per point."""

    return call_llm(prompt)