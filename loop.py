from pathlib import Path
from patch_generator import call_llm
from tools.code_search import read_file
from tools.patch_applier import apply_patch
from tools.test_runner import run_tests

MAX_ATTEMPTS = 3

def run_agent(repo_path: Path, file_path: str, issue_description: str) -> dict:
    """Main agent loop: try to fix the issue, retrying with test feedback on failure."""
    original_code = read_file(repo_path, file_path)
    attempt_history = []

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n=== Attempt {attempt}/{MAX_ATTEMPTS} ===")

        # Build the prompt, including any previous failure info
        feedback = ""
        if attempt_history:
            last = attempt_history[-1]
            feedback = f"""
Your previous attempt failed. Here's what happened:
PREVIOUS CODE YOU WROTE:
{last['code']}
TEST OUTPUT:
{last['test_output'][-800:]}

Fix the issue, taking this failure into account."""

        prompt = f"""You are a coding agent fixing a bug.

ISSUE:
{issue_description}

FILE: {file_path}
ORIGINAL CONTENT:
{original_code}
{feedback}

Return ONLY the complete fixed version of this file. No explanations, no markdown fences, just the raw code."""

        fixed_code = call_llm(prompt)
        apply_patch(repo_path, file_path, fixed_code)

        result = run_tests(repo_path)
        attempt_history.append({
            "attempt": attempt,
            "code": fixed_code,
            "passed": result["passed"],
            "test_output": result["stdout"] + result["stderr"]
        })

        if result["passed"]:
            print(f"✅ Fixed on attempt {attempt}")
            return {"success": True, "attempts": attempt, "history": attempt_history}

        print(f"❌ Attempt {attempt} failed, retrying..." if attempt < MAX_ATTEMPTS else f"❌ Failed after {MAX_ATTEMPTS} attempts")

    return {"success": False, "attempts": MAX_ATTEMPTS, "history": attempt_history}