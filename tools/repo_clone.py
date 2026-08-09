import subprocess
import shutil
import stat
from pathlib import Path
import os

WORKSPACE = Path("./workspace").resolve()

def _remove_readonly(func, path, excinfo):
    """Clear the read-only bit and retry deletion (needed for git's .git folder on Windows)."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repo(repo_url: str, repo_name: str) -> Path:
    """Clone a fresh copy of a repo into the workspace folder."""
    repo_path = WORKSPACE / repo_name
    if repo_path.exists():
        shutil.rmtree(repo_path, onerror=_remove_readonly)
    WORKSPACE.mkdir(exist_ok=True)
    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, str(repo_path)],
        check=True
    )
    return repo_path