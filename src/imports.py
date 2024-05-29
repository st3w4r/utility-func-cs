import os
import sys
import ast
import importlib
import inspect

def list_imports_with_paths(directory):
    imports = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        node = ast.parse(f.read(), filename=file_path)
                        for item in node.body:
                            if isinstance(item, ast.Import):
                                for alias in item.names:
                                    imports[alias.name] = None
                            elif isinstance(item, ast.ImportFrom):
                                module = item.module if item.module else ''
                                for alias in item.names:
                                    full_import = f"{module}.{alias.name}" if module else alias.name
                                    imports[full_import] = None
                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")
    return imports


def get_module_filepath(imports):
    for imp in imports.keys():
        try:
            print(imp)
            module = importlib.import_module(imp.split('.')[0])
            file_path = inspect.getfile(module)
            imports[imp] = file_path
        except Exception as e:
            imports[imp] = f"Could not locate: {e}"
    return imports


def main(repo):
    imports = list_imports_with_paths(repo)
    imports = get_module_filepath(imports)
    for imp, path in imports.items():
        print(f"{imp}:\t{path}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python find_utils.py <repo_path>")
        sys.exit(1)
    repo = args[0]
    main(repo)
