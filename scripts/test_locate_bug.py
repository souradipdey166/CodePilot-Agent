from pathlib import Path
from tools.locate_bug import locate_function

repo_path = Path("./workspace/requests")
result = locate_function(repo_path, "get")
print(result)