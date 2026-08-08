from pathlib import Path
from loop import run_agent

repo_path = Path("./workspace/sample_project")
issue = "The add() function returns the wrong result. add(2, 3) should return 5, but it doesn't."

result = run_agent(repo_path, "calculator.py", issue)

print("\n=== FINAL RESULT ===")
print("Success:", result["success"])
print("Attempts used:", result["attempts"])