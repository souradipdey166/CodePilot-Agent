from pathlib import Path
import os
from tools.ast_search import list_definitions, find_function

repo_path = Path("./workspace/requests")

# 1. List all definitions in one file
defs = list_definitions(repo_path / "src" / "requests" / "api.py")
print("Definitions in api.py:")
for d in defs:
    print(f"  {d['type']}: {d['name']} (lines {d['start_line']}-{d['end_line']})")

# 2. Find a specific function by exact name, across the whole repo
matches = find_function(repo_path, "get")
print("\nExact matches for function 'get':")
for m in matches:
    print(f"  {m['file']}:{m['start_line']} -> {m['type']} {m['name']}")