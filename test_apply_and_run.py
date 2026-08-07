from pathlib import Path
from patch_generator import generate_patch
from tools.patch_applier import apply_patch
from tools.test_runner import run_tests

repo_path = Path("./workspace/sample_project")
issue = "The add() function returns the wrong result. add(2, 3) should return 5, but it doesn't."

# Generate the fix
fixed_code = generate_patch(repo_path, "calculator.py", issue)
print("--- Proposed fix ---")
print(fixed_code)

# Apply it
apply_patch(repo_path, "calculator.py", fixed_code)
print("\n--- Patch applied ---")

# Run tests to verify
result = run_tests(repo_path)
print("\n--- Test results ---")
print("PASSED" if result["passed"] else "FAILED")
print(result["stdout"][-500:])