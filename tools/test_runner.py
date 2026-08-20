import subprocess
from pathlib import Path

DOCKER_IMAGE = "code-agent-sandbox"

def run_tests(repo_path: Path, timeout: int = 60) -> dict:
    """Run pytest inside a Docker container, isolated from the host machine."""
    repo_path = Path(repo_path).resolve()

    # Find the working directory inside the repo (src/ if it exists, else repo root)
    test_dir = "src" if (repo_path / "src").exists() else "."

    try:
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{repo_path}:/workspace",
                "-w", f"/workspace/{test_dir}",
                DOCKER_IMAGE,
                "python", "-m", "pytest", "-v"
            ],
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