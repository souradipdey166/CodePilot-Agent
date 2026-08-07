import subprocess
from pathlib import Path

def run_tests(repo_path: Path, timeout: int = 60) -> dict:
    """Run pytest inside the repo, return pass/fail + output."""
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "-v"],
            cwd=repo_path,
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