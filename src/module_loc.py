import ast
import sys
import importlib.util

def list_imports_with_locations(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            if module:
                imports.append(module)
    
    for module_name in imports:
        location = get_module_location(module_name)
        print(f"{module_name}: {location}")

def get_module_location(module_name):
    try:
        spec = importlib.util.find_spec(module_name)
        if spec and spec.origin:
            return spec.origin
        else:
            return f"Module {module_name} not found"
    except ModuleNotFoundError:
        return f"Module {module_name} not found"


def main(file):
    list_imports_with_locations(file)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python module_loc.py <file>")
        sys.exit(1)
    repo = args[0]
    main(repo)
