import subprocess
import shutil
from pathlib import Path

WORKSPACE = Path("./workspace").resolve()

def clone_repo(repo_url: str, repo_name: str) -> Path:
    """Clone a fresh copy of a repo into the workspace folder."""
    repo_path = WORKSPACE / repo_name
    if repo_path.exists():
        shutil.rmtree(repo_path)
    WORKSPACE.mkdir(exist_ok=True)
    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, str(repo_path)],
        check=True
    )
    return repo_path