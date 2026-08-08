from pathlib import Path
from tools.repo_clone import clone_repo
from tools.code_search import search_text
from loop import run_agent

# --- Fill these in for the real issue you picked ---
REPO_URL = "https://github.com/<owner>/<repo>"
REPO_NAME = "<repo-name>"
ISSUE_DESCRIPTION = """
<paste the real GitHub issue title + description here>
"""
# -----------------------------------------------------

repo_path = clone_repo(REPO_URL, REPO_NAME)
print(f"Cloned to: {repo_path}")

# Use search to find which file is likely relevant before running the agent
# Example: search for a function/keyword mentioned in the issue
results = search_text(repo_path, "some_keyword_from_the_issue")
print("Candidate files:")
for r in results[:10]:
    print(f"  {r['file']}:{r['line']} -> {r['text']}")

# Once you've picked the right file from the search results above, set it here:
TARGET_FILE = "<path/to/file.py>"

result = run_agent(repo_path, TARGET_FILE, ISSUE_DESCRIPTION)

print("\n=== FINAL RESULT ===")
print("Success:", result["success"])
print("Attempts used:", result["attempts"])