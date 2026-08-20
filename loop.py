from pathlib import Path
from patch_generator import call_llm
from planner import generate_plan
from tools.code_search import read_file
from tools.patch_applier import apply_patch
from tools.test_runner import run_tests
from tools.memory import record_failure, get_relevant_failures

MAX_ATTEMPTS = 3

def run_agent(repo_path: Path, file_path: str, issue_description: str, repo_name: str = "default") -> dict:
    original_code = read_file(repo_path, file_path)
    attempt_history = []

    past_failures = get_relevant_failures(repo_name, file_path)
    memory_context = ""
    if past_failures:
        memory_context = "\n\nPast failed attempts on this file (avoid repeating these mistakes):\n"
        for pf in past_failures[-3:]:
            memory_context += f"- Tried: {pf['code_tried'][:200]}... Error: {pf['error'][:200]}\n"

    # NEW: generate a plan before writing any code
    plan = generate_plan(file_path, original_code, issue_description, memory_context)
    print(f"\n[PLAN]\n{plan}\n")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n=== Attempt {attempt}/{MAX_ATTEMPTS} ===")

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

YOUR PLAN (follow this):
{plan}
{memory_context}
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
            return {"success": True, "attempts": attempt, "history": attempt_history, "plan": plan}

        record_failure(repo_name, file_path, issue_description, fixed_code, result["stdout"] + result["stderr"])
        print(f"❌ Attempt {attempt} failed, retrying..." if attempt < MAX_ATTEMPTS else f"❌ Failed after {MAX_ATTEMPTS} attempts")

    return {"success": False, "attempts": MAX_ATTEMPTS, "history": attempt_history, "plan": plan}