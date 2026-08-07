from pathlib import Path

def apply_patch(repo_path: Path, file_path: str, new_content: str):
    """Overwrite the file with the LLM's proposed fixed version."""
    full_path = Path(repo_path) / file_path
    full_path.write_text(new_content, encoding="utf-8")