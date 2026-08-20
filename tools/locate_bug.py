from pathlib import Path
from typing import Optional
from tools.ast_search import find_function

def locate_function(repo_path: Path, function_name: str) -> Optional[dict]:
    """Find the most likely definition of a function, given its name.
    Returns the first match for now — later we can add smarter disambiguation."""
    matches = find_function(repo_path, function_name)
    if not matches:
        return None
    return matches[0]  # naive for now — good enough to start