# list all the porotypes of a file
import sys
import ast


def get_function_protoypes(code):

    prototypes = []
    tree = ast.parse(code)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):

            prototype = {
                "name": node.name,
                "params": [param.arg for param in node.args.args],
                "return": [],
                "code": None,
                "doc": None,
            }

            for child_node in ast.walk(node):

                if isinstance(child_node, ast.arg) and child_node.annotation:
                    prototype["code"] = ast.unparse(child_node)

                
                if isinstance(child_node, ast.Constant):
                    if isinstance(child_node.value, str):
                        prototype["doc"] = child_node.value.strip()


                if isinstance(child_node, ast.Return):
                    value = child_node.value

                    if isinstance(value, ast.Name):
                        prototype['return'].append(value.id)
                    elif isinstance(value, ast.Subscript):
                        prototype["return"].append(f"{value.value}[{value.slice}]")
                    elif isinstance(value, ast.Attribute):
                        if isinstance(value.value, ast.Name):
                            print("ID",value.value.id)
                    elif isinstance(value, ast.BinOp):
                        print(value.op)
                    elif isinstance(value, ast.Call):
                        print("FUNC:", value.func)
                    else:
                        print(value)
            prototypes.append(prototype)
    return prototypes



def main(file):

    with open(file, 'r') as f:
        content = f.read()

    prototypes = get_function_protoypes(content)

    no_returns = [p for p in prototypes if len(p["return"]) == 0]

    print("NO RETURN")
    print('--------------')
    for p in no_returns:
        print(p["name"])

    print()
    print("RETURNS")
    print('--------------')
    returns = [p for p in prototypes if len(p["return"])]
    for p in returns:
        print(p["name"], p["params"])

    print()
    print("RETURN CODE")
    code = [p for p in prototypes]
    for p in code:
        print(f"===============CODE: { p["name"] }================")
        print(p["code"])
        print()

    print()
    print("DOCSTRING")
    doc = [p for p in prototypes if p["doc"]]
    for p in doc:
        print(f"===========DOC: {p['name']}===========")
        print(p["doc"])
        print()



if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python find_utils.py <file_path>")
        sys.exit(1)
    file = args[0]
    main(file)
