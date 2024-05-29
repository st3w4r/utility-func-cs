import os
import sys


scan_dir = ["src"]

# Look for directory or files that could contains utils
utility_names = [
    "utils", "util",
    "tools", "tool",
    "helpers", "helper",
    "common", "commons",
    "shared", "share",
]


def walk_all_files(root_dir):
    all_files = []
    root = root_dir
    print("SCANNING:", root)
    for root, dirs, files in os.walk(root):
        for file_name in files:
            a_file = os.path.join(root, file_name)
            all_files.append(a_file)
    return all_files


def walk_dir(root_dir):
    found_files = []

    for dir_to_scan in scan_dir:
        root = os.path.join(root_dir, dir_to_scan)
        for root, dirs, files in os.walk(root):
            for dir_name in dirs:
                if any(utility_name in dir_name for utility_name in utility_names):
                    found_dir = os.path.join(root, dir_name)
                    print(f"Found utility directory: {found_dir}")
                    found_files.append(found_dir)

            for file_name in files:
                if any(utility_name in file_name for utility_name in utility_names):
                    found_file = os.path.join(root, file_name)
                    print(f"Found utility file: {found_file}")
                    found_files.append(found_file)

    return found_files

def count_nb_lines(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            return len(file.readlines())
    else:
        return 0

def count_nb_words(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            content = file.read()
            words = content.split()
            return len(words)
    else:
        return 0

def main(repo):
    files = walk_dir(repo)
    print(f"Total files found: {len(files)}")

    total_lines = 0
    total_words = 0
    max_files = 10  # Maximum number of files to process
    print(f"Max files to process: {max_files}")
    processed_files = 0
    for file in files:
        if processed_files >= max_files:
            break
        nb_lines = count_nb_lines(file)
        nb_words = count_nb_words(file)
        print(f"{file}: {nb_lines} lines, {nb_words} words")
        total_lines += nb_lines
        total_words += nb_words
        processed_files += 1
    print(f"Total lines: {total_lines}")
    print(f"Total words: {total_words}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python find_utils.py <repo_path>")
        sys.exit(1)
    repo_path = args[0]
    main(repo_path)
