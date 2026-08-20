from tools.memory import record_failure, load_memory, get_relevant_failures

record_failure(
    repo_name="test_repo",
    file_path="calculator.py",
    issue="add() returns wrong result",
    code_tried="def add(a, b): return a - b",
    error="assert 5 == -1"
)

print("All memory for test_repo:")
print(load_memory("test_repo"))

print("\nRelevant failures for calculator.py:")
print(get_relevant_failures("test_repo", "calculator.py"))