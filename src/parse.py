import ast
import os
import sys
from explorer import walk_all_files

def extract_imports(source: str):
    """
    Extract the imports from a source code.
    """
    imports = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return imports

    for node in tree.body:
        if isinstance(node, ast.Import):
            for imp_node in node.names:
                import_name = imp_node.name
                imports.append(import_name)
        elif isinstance(node, ast.ImportFrom):
            for imp_node in node.names:
                if node.module:
                    imports.append(f"{node.module}.{imp_node.name}")
                else:
                    imports.append(f"{imp_node.name}")
    return imports


def read_content(filepath: str):
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'r') as f:
                source = f.read()
                return source
        except UnicodeDecodeError as e:
            return None
    return None

def aggregates_imports(imports):
    """
    Aggreate the imports, count them
    """
    imports_dict = {}
    for impt in imports:
        if imports_dict.get(impt):
            imports_dict[impt] += 1
        else:
            imports_dict[impt] = 1
    return imports_dict


def filter_stdlib(imports_agg):
    """
    Exclude the standard library imports.
    """
    return {impt: nb for impt, nb in imports_agg.items() if not sys.modules.get(impt)}


def main(repo):

    # List files
    files = walk_all_files(repo)
    files = [filepath for filepath in files if os.path.isfile(filepath)]

    # Read files content
    imports = []
    for file in files:
        content = read_content(file)
        if content is None:
            continue
        impts = extract_imports(content)
        imports.extend(impts)

    imports_agg = aggregates_imports(imports)
    imports_filtered = filter_stdlib(imports_agg)

    # Sort by most used
    sorted_agg = sorted(list(imports_filtered.items()), key=lambda x: x[1])
    for impt, nb in sorted_agg:
        print(nb, "\t", impt)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python find_utils.py <repo_path>")
        sys.exit(1)
    repo = args[0]
    main(repo)
