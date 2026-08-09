import subprocess
from pathlib import Path

def run_tests(repo_path: Path, timeout: int = 60) -> dict:
    """Run pytest inside the repo, return pass/fail + output."""
    # Run from src/ if it exists, since that's where the code + tests live
    test_dir = Path(repo_path) / "src"
    if not test_dir.exists():
        test_dir = Path(repo_path)

    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "-v"],
            cwd=test_dir,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "passed": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {"passed": False, "stdout": "", "stderr": "Timed out"}