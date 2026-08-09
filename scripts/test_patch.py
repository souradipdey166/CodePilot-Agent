from pathlib import Path
from patch_generator import generate_patch

repo_path = Path("./workspace/sample_project")
issue = "The add() function returns the wrong result. add(2, 3) should return 5, but it doesn't."

fixed_code = generate_patch(repo_path, "calculator.py", issue)
print("--- LLM's proposed fix ---")
print(fixed_code)