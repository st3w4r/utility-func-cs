# Files

Description of the intent of each file.

Example tested on the `transformers` repo.
```bash
git clone https://github.com/huggingface/transformers.git
```

## [parse.py](parse.py)

Using AST to parse the source code and extract the import and import from.
Aggregates the imports based on the number of times they are used.

Use case: detect the most used imports in a project.

Usage: 
```bash
python src/parse.py repos/transformers/src/transformers/
```

Output:
```bash
...
321      utils.add_start_docstrings_to_model_forward
329      typing.TYPE_CHECKING
337      utils.add_start_docstrings
361      utils.is_torch_available
490      torch
497      typing.List
586      typing.Union
609      typing.Tuple
762      typing.Optional
975      utils.logging
```


## [explorer.py](explorer.py)

Look into project repo to find common patterns in the naming. Similar to "utils" or "common", etc.
Count the number of lines and words it the files to have an estimate of the number of tokens before passing it to an LLM.

Use case: Find as quick as possible where the utility functions are stored. Get an estimate of the number of tokens in the files.

Usage:
```bash
python src/explorer.py repos/transformers/
```

Output:
```bash
...
Found utility file: repos/transformers/src/transformers/integrations/integration_utils.py
Found utility file: repos/transformers/src/transformers/data/processors/utils.py
Found utility file: repos/transformers/src/transformers/generation/configuration_utils.py
Found utility file: repos/transformers/src/transformers/generation/flax_utils.py
Found utility file: repos/transformers/src/transformers/generation/utils.py
Found utility file: repos/transformers/src/transformers/generation/tf_utils.py
Total files found: 60
Max files to process: 10
repos/transformers/src/transformers/utils: 0 lines, 0 words
repos/transformers/src/transformers/configuration_utils.py: 1144 lines, 5764 words
repos/transformers/src/transformers/image_utils.py: 760 lines, 3144 words
repos/transformers/src/transformers/tokenization_utils.py: 1043 lines, 4409 words
repos/transformers/src/transformers/pytorch_utils.py: 297 lines, 1270 words
repos/transformers/src/transformers/modeling_flax_utils.py: 1288 lines, 5802 words
repos/transformers/src/transformers/modeling_flax_pytorch_utils.py: 496 lines, 1980 words
repos/transformers/src/transformers/feature_extraction_utils.py: 690 lines, 2704 words
repos/transformers/src/transformers/tokenization_utils_base.py: 4157 lines, 19696 words
repos/transformers/src/transformers/testing_utils.py: 2495 lines, 8614 words
Total lines: 12370
Total words: 53383
```


## [prototypes.py](prototypes.py)

Find the prototypes inside a files, to have an overview of whcih function returns a value and which does not.

Use case: Identify pure function that could be utility function.

Usage:
```bash
python src/prototypes.py repos/transformers/src/transformers/dynamic_module_utils.py
```

Output:
```bash
NO RETURN
--------------
init_hf_modules
create_dynamic_module
...

RETURNS
--------------
get_relative_import_files ['module_file']
...
```


## [imports.py](imports.py)

Find the actual location of the module based on the imports in a file.

Use case: Based on the name of a module get the location to be able to aggregate similar use of the modules, and get the unique ones.

Usage:
```bash
python src/imports.py src/
```

Output:
```bash
pygls.exceptions.JsonRpcException:      /home/vscode/.local/lib/python3.12/site-packages/pygls/__init__.py
explorer.walk_all_files:        /workspaces/interview/codestory/src/explorer.py
pkg_resources:  /usr/local/lib/python3.12/site-packages/pkg_resources/__init__.py
pkgutil:        /usr/local/lib/python3.12/pkgutil.py
```

## [llm.py](llm.py)

Find the utility functions in a file using an LLM model. Based on criterias to identify them.

Usage: Return a list of utility functions and non-utility functions.


Usage:
```bash
python src/llm.py src/parse.py 
```

Output:
```jsonc
RAW:
extract_imports(source: str): True
read_content(filepath: str): True
aggregates_imports(imports): True
filter_stdlib(imports_agg): True
main(repo): False
walk_all_files(repo): False (not provided)

FORMATTED:
{
  "utility_functions": [
    "extract_imports",
    "read_content",
    "aggregates_imports",
    "filter_stdlib"
  ],
  "non_utility_functions": [
    "main",
    "walk_all_files"
  ]
}
```


## [module_loc.py](module_loc.py)

Find the location of a module based on the name of the module. For a file.

Use case: identity the standard library modules, the extenal and internal ones.

Usage:
```bash
python src/module_loc.py repos/transformers/utils/models_to_deprecate.py 
```

Output:
```bash
argparse: /usr/local/lib/python3.12/argparse.py
glob: /usr/local/lib/python3.12/glob.py
json: /usr/local/lib/python3.12/json/__init__.py
os: frozen
collections: /usr/local/lib/python3.12/collections/__init__.py
datetime: /usr/local/lib/python3.12/datetime.py
pathlib: /usr/local/lib/python3.12/pathlib.py
git: Module git not found
huggingface_hub: /home/vscode/.local/lib/python3.12/site-packages/huggingface_hub/__init__.py
```

### example 2

Usage:
```bash
python src/module_loc.py src/parse.py 
```
Output:
```bash
sys: built-in
python src/module_loc.py src/parse.py 
ast: /usr/local/lib/python3.12/ast.py
os: frozen
explorer: /workspaces/interview/codestory/src/explorer.py
```


## [lsp_clt.py](lsp_clt.py)

Client to communicate with the LSP server. Send a request to the server and get the response.

Use case: Get an accurate imports list.

Usage:
```bash
# Start the server
pylsp -v --tcp --host localhost 
--port 2087
```

```bash
python src/lsp_clt.py 
```


Output: Not fully functional yet. Server capabilities are displayed.
```bash
Server capabilities: {'codeActionProvider': True, 'codeLensProvider': {'resolveProvider': False}, 'completionProvider': {'resolveProvider': True, 'triggerCharacters': ['.']}, 
...
```


## [pyright.py](pyright.py)

Use the Pyright LSP server to get the imports list. Use the verbose mode with dependencies to get the full list. Parse the list into JSON.

Use case: Get an accurate imports list.

Usage:
```bash
# Install pyright
npm install -g pyright

# Run extraction
python src/pyright.py repos/transformers/src/transformers/ > output.json
```

Output:
```json
[
  {
    "file": "repos/transformers/src/transformers/utils/versions.py",
    "imports": [],
    "imported_by": [
      "file:///workspaces/interview/codestory/repos/transformers/src/transformers/dependency_versions_check.py",
      "file:///workspaces/interview/codestory/repos/transformers/src/transformers/models/code_llama/tokenization_code_llama_fast.py",
      "file:///workspaces/interview/codestory/repos/transformers/src/transformers/models/cohere/tokenization_cohere_fast.py",
      "file:///workspaces/interview/codestory/repos/transformers/src/transformers/models/gemma/tokenization_gemma_fast.py",
      "file:///workspaces/interview/codestory/repos/transformers/src/transformers/models/llama/tokenization_llama_fast.py",
...
```


## [pyright_count.py](pyright_count.py)

Aggregate the imports based on the number of times they are used.

Use case: detect the most used imports in a project.

Usage:
```bash
python src/pyright_count.py output.json
```

Output:
```json
[
  {
    "file": "repos/transformers/src/transformers/configuration_utils.py",
    "imports_count": 6,
    "imported_by_count": 274
  },
  {
    "file": "repos/transformers/src/transformers/utils/logging.py",
    "imports_count": 0,
    "imported_by_count": 1087
  },
  {
    "file": "repos/transformers/src/transformers/utils/__init__.py",
    "imports_count": 8,
    "imported_by_count": 1446
  }
]
```



