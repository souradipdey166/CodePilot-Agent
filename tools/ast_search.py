from pathlib import Path
from tree_sitter import Language, Parser
import tree_sitter_python as tspython

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

def parse_file(file_path: Path):
    """Parse a Python file and return its syntax tree."""
    source = file_path.read_bytes()
    tree = parser.parse(source)
    return tree, source

def list_definitions(file_path: Path) -> list[dict]:
    """List all function and class definitions in a file, with line numbers."""
    tree, source = parse_file(file_path)
    definitions = []

    def walk(node):
        if node.type in ("function_definition", "class_definition"):
            name_node = node.child_by_field_name("name")
            if name_node:
                name = source[name_node.start_byte:name_node.end_byte].decode("utf-8")
                definitions.append({
                    "type": node.type,
                    "name": name,
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1
                })
        for child in node.children:
            walk(child)

    walk(tree.root_node)
    return definitions

def find_function(repo_path: Path, function_name: str, extension: str = ".py") -> list[dict]:
    """Search the whole repo for a function/class definition with an exact name match."""
    matches = []
    for file in Path(repo_path).rglob(f"*{extension}"):
        try:
            defs = list_definitions(file)
        except Exception:
            continue
        for d in defs:
            if d["name"] == function_name:
                matches.append({
                    "file": str(file.relative_to(repo_path)),
                    **d
                })
    return matches