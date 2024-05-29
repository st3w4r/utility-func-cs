import json
import sys


def summarize_imports(data):
    summary = []
    for entry in data:
        file = entry['file']
        num_imports = len(entry['imports'])
        num_imported_by = len(entry['imported_by'])
        summary.append({
            'file': file,
            'imports_count': num_imports,
            'imported_by_count': num_imported_by
        })
    summary.sort(key=lambda x: x['imported_by_count'], reverse=False)
    return summary


def main(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
        summary = summarize_imports(data)
        print(json.dumps(summary, indent=2))
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pyright_count.py <file>")
        sys.exit(1)
    main(sys.argv[1])
