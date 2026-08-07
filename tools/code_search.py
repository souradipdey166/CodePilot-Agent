from pathlib import Path

def list_files(repo_path: Path, extension: str = ".py") -> list[str]:
    """List all files of a given type in the repo."""
    files = list(Path(repo_path).rglob(f"*{extension}"))
    return [str(f.relative_to(repo_path)) for f in files]

def search_text(repo_path: Path, query: str, extension: str = ".py") -> list[dict]:
    """Search for a text string across files, return matches with file + line number."""
    matches = []
    for file in Path(repo_path).rglob(f"*{extension}"):
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if query.lower() in line.lower():
                matches.append({
                    "file": str(file.relative_to(repo_path)),
                    "line": i,
                    "text": line.strip()
                })
    return matches

def read_file(repo_path: Path, relative_path: str) -> str:
    """Read the full contents of a specific file."""
    full_path = Path(repo_path) / relative_path
    return full_path.read_text(encoding="utf-8", errors="ignore")