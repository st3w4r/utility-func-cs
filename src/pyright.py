import re
import json
import sys
import subprocess


def run_pyright_command(relative_path):
    try:
        command = ["pyright", "--verbose", "--dependencies", relative_path]
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"An error occurred while executing Pyright: {e}")
        return None

def parse_imports(raw_text, relative_path):
    import_info = []
    current_file = None
    imports = []
    imported_by = []
    section = None
    
    lines = raw_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith((relative_path, '../../../')):
            if current_file:
                import_info.append({
                    'file': current_file,
                    'imports': imports,
                    'imported_by': imported_by
                })
                imports = []
                imported_by = []
            
            current_file = line
            section = None
        elif 'Imports' in line:
            section = 'imports'
        elif 'Imported by' in line:
            section = 'imported_by'
        elif line.startswith('file://'):
            if section == 'imports':
                imports.append(line)
            elif section == 'imported_by':
                imported_by.append(line)
    
    if current_file:
        import_info.append({
            'file': current_file,
            'imports': imports,
            'imported_by': imported_by
        })

    return import_info

def parse_raw_text_to_json(raw_text):
    lines = raw_text.split('\n')
    
    result = []
    current_file = {}
    current_section = None
    
    file_path_regex = re.compile(r'^[./\w]+/\w+\.pyi?$')
    imports_regex = re.compile(r'^\s+file://.+')
    imported_by_regex = re.compile(r'^\s+file://.+')

    for line in lines:
        if file_path_regex.match(line.strip()):
            if current_file:
                current_file['imported_by_count'] = len(current_file['imported_by'])
                result.append(current_file)
            current_file = {'filepath': line.strip(), 'imports': [], 'imported_by': []}
            current_section = None
        elif 'Imports' in line:
            current_section = 'imports'
        elif 'Imported by' in line:
            current_section = 'imported_by'
        elif imports_regex.match(line) and current_section == 'imports':
            current_file['imports'].append(line.strip())
        elif imported_by_regex.match(line) and current_section == 'imported_by':
            current_file['imported_by'].append(line.strip())

        if "files not explicitly imported" in line:
            current_section = None
            current_file = {'filepath': line.strip(), 'imports': [], 'imported_by': []}
    
    if current_file:
        current_file['imported_by_count'] = len(current_file['imported_by'])
        result.append(current_file)
    
    return result



def extract_between(text, start_phrase, end_phrase):
    start_index = text.find(start_phrase)
    if start_index == -1:
        return "Start phrase not found."
    start_line_end = text.find('\n', start_index) + 1

    end_index = text.find(end_phrase, start_index)
    if end_index == -1:
        return "End phrase not found."
    end_line_start = text.rfind('\n', start_index, end_index)

    extracted_text = text[start_line_end:end_line_start].strip()

    return extracted_text

def filter_file_lines(text, prefix):
    filtered_lines = []
    for line in text.split('\n'):
        if not line.strip().startswith('file:///') or line.strip().startswith(prefix):
            filtered_lines.append(line)
    return '\n'.join(filtered_lines)

def filter_files(data, prefix):
    filtered_data = []
    for item in data:
        if item["file"].startswith(prefix):
            filtered_data.append(item)
    return filtered_data

def main(relative_path):
    raw_text = run_pyright_command(relative_path)
    if raw_text:
        try:
            extracted_text = extract_between(raw_text, "Completed in", "not explicitly imported")
            filtered_text = filter_file_lines(extracted_text, 'file:///workspaces/interview/codestory')
            parsed_json = parse_imports(filtered_text, relative_path)
            filtered_data = filter_files(parsed_json, relative_path)

            print(json.dumps(filtered_data, indent=2))
        except Exception as e:
            print(f"An error occurred during parsing or filtering: {e}")
    else:
        print("No output was generated by the Pyright command.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_utils.py <repo_path>")
        sys.exit(1)
    relative_path = sys.argv[1]
    main(relative_path)
