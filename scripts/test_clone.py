import subprocess
from pathlib import Path

WORKSPACE = Path("./workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)
repo_path = WORKSPACE / "requests"

subprocess.run(["git", "clone", "--depth", "1", "https://github.com/psf/requests", str(repo_path)], check=True)
print("Cloned to:", repo_path)
print("Files:", list(repo_path.glob("*"))[:5])