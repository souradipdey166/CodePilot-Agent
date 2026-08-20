import json
from datetime import datetime
from pathlib import Path
from tools.repo_clone import clone_repo
from tools.code_search import search_text
from loop import run_agent

# --- Fill these in for the real issue you picked ---
REPO_URL = "https://github.com/souradipdey166/endtoend_ML_project"
REPO_NAME = "endtoend_ML_project"
ISSUE_DESCRIPTION = """
Users report that dev(10, 3) returns 7 instead of the expected value.
Something is wrong with how the division is being calculated.
"""
TARGET_FILE = "src/check.py"
# -----------------------------------------------------

repo_path = clone_repo(REPO_URL, REPO_NAME)
print(f"Cloned to: {repo_path}")

#result = run_agent(repo_path, TARGET_FILE, ISSUE_DESCRIPTION)
result = run_agent(repo_path, TARGET_FILE, ISSUE_DESCRIPTION, repo_name=REPO_NAME)

print("\n=== FINAL RESULT ===")
print("Success:", result["success"])
print("Attempts used:", result["attempts"])

print("\n=== DEBUG: What went wrong ===")
for h in result["history"]:
    print(f"\n--- Attempt {h['attempt']} ---")
    print("Passed:", h["passed"])
    print("Test output (last 1000 chars):")
    print(h["test_output"][-1000:])

# --- Save run log ---
log_entry = {
    "timestamp": datetime.now().isoformat(),
    "repo": REPO_URL,
    "target_file": TARGET_FILE,
    "issue": ISSUE_DESCRIPTION.strip(),
    "success": result["success"],
    "attempts_used": result["attempts"],
    "history": result["history"]
}

Path("data").mkdir(exist_ok=True)
log_path = Path("data") / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(log_path, "w") as f:
    json.dump(log_entry, f, indent=2)

latest_path = Path("data") / "latest_run.json"
with open(latest_path, "w") as f:
    json.dump(log_entry, f, indent=2)

print(f"\nRun log saved to: {log_path}")