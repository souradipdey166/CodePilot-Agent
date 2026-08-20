from pathlib import Path
from tools.code_search import list_files, search_text, read_file

repo_path = Path("./workspace/requests")

files = list_files(repo_path)
print("Sample files:", files[:5])

results = search_text(repo_path, "def get(")
print("\nSearch results for 'def get(':")
for r in results[:5]:
    print(f"  {r['file']}:{r['line']} -> {r['text']}")

print('\n-'*2)

if results:
    content = read_file(repo_path, results[0]["file"])
    print(f"\nFirst 200 chars of {results[0]['file']}:")
    print(content[:200])