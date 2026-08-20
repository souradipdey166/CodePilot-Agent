import json
from pathlib import Path
from datetime import datetime

MEMORY_DIR = Path("./data/memory")

def _memory_path(repo_name: str) -> Path:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    return MEMORY_DIR / f"{repo_name}.json"

def load_memory(repo_name: str) -> list[dict]:
    """Load all recorded failed attempts for a given repo."""
    path = _memory_path(repo_name)
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)

def record_failure(repo_name: str, file_path: str, issue: str, code_tried: str, error: str):
    """Append a new failed attempt to memory."""
    memory = load_memory(repo_name)
    memory.append({
        "timestamp": datetime.now().isoformat(),
        "file": file_path,
        "issue": issue,
        "code_tried": code_tried,
        "error": error
    })
    with open(_memory_path(repo_name), "w") as f:
        json.dump(memory, f, indent=2)

def get_relevant_failures(repo_name: str, file_path: str) -> list[dict]:
    """Get past failures for a specific file in this repo."""
    memory = load_memory(repo_name)
    return [m for m in memory if m["file"] == file_path]