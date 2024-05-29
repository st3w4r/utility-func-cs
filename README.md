# CodeStory - Utlity functions

Project:
- Discover as fast as possible utility functions in a codebase
- Utility function are useful to help the user and reuse existing code as much as possible

Use case:
- When coding in a porject and I want to do something specific with the current variable/object i'm manipulating
- I want to know if there is a utility function that can help me with that
- The utility function is proposed if it already exists in the codebase
- I can chose the utility function
- It will be inserted in the codebase


In python:
- Utility functions have no side effect
- Simple one responsability
- Stateless


To detect them
- Filter them by arguemnts types
- Look for functions with a single responsibility
- Look for functions that are used in multiple places
- They have lot of references to it in the codebase
- They have a single level of abstraction



To explore:
- LSP
- Static Code analysis
- Automated refactoring tool
- Dependency graph
- Dynamic code analysis
- Code metrics, cohesion, low coupling
- Test coverage isolation
- ML model to detect utility functions
- TreeSitter to extract imports


- Common pattern in naming
- Common place a directory
- Analyze function signature
- Stateless and no side effect
- High use in the codebase
- Single responsability
- Corresponding unit test
- Pure function
- A pure function need to call only pure functions


### Criterias

- Single, Specific Purpose
- Reusability
- Minimal Dependencies
- Simplicity
- Self-Contained
- General Use
- Utility


### Example criterias

Example:
- ./repos/transformers/tests/utils/test_audio_utils.py

| Function                     | Single, Specific Purpose | Reusability | Minimal Dependencies | Simplicity | Self-Contained | General Use | Utility |
|------------------------------|--------------------------|-------------|----------------------|------------|----------------|-------------|---------|
| `hertz_to_mel`               | True                     | True        | True                 | True       | True           | True        | True    |
| `mel_to_hertz`               | True                     | True        | True                 | True       | True           | True        | True    |
| `hertz_to_octave`            | True                     | True        | True                 | True       | True           | True        | True    |
| `_create_triangular_filter_bank` | True                 | False       | False                | True       | False          | False       | False   |
| `chroma_filter_bank`         | False                    | False       | False                | False      | False          | False       | False   |
| `mel_filter_bank`            | False                    | False       | False                | False      | False          | False       | False   |
| `optimal_fft_length`         | True                     | True        | True                 | True       | True           | True        | True    |
| `window_function`            | True                     | True        | True                 | True       | True           | True        | True    |
| `spectrogram`                | False                    | False       | False                | False      | False          | False       | False   |
| `power_to_db`                | True                     | True        | True                 | True       | True           | True        | True    |
| `amplitude_to_db`            | True                     | True        | True                 | True       | True           | True        | True    |
| `get_mel_filter_banks`       | True                     | True        | True                 | True       | True           | True        | True    |
| `fram_wave`                  | False                    | False       | False                | False      | False          | False       | False   |
| `stft`                       | False                    | False       | False                | False      | False          | False       | False   |




## Proposals

- Scan with LLM check for criterias
- Narrow the search based on determinic rules


## Example output:

```json
{
  "utility_functions": [
    "hertz_to_mel",
    "mel_to_hertz",
    "hertz_to_octave",
    "_create_triangular_filter_bank",
    "optimal_fft_length",
    "window_function",
    "power_to_db",
    "amplitude_to_db",
    "get_mel_filter_banks",
    "fram_wave"
  ],
  "non_utility_functions": [
    "chroma_filter_bank",
    "mel_filter_bank",
    "spectrogram",
    "stft"
  ]
}
```


## Detect dependencies

- extract deps
- count deps
- graph the deps
- calulcate the weights of the deps 


- AST
    - extract all the imports
    - filter out the std libs, built-in imports
    - filter the external imports from 3rd party libs
- LSP, detect the imports


### LSP

Use 'textDocument/prepareImportSuggestions'


### AST

- Find the most imported modules
- Get the definiton of it
- Check if utility function
- Match the types of it


- List all the funcitons and their prototypes
- Exclude the function that return None, as they are likely to have side effect

- Get the type hints from AST


```
NO RETURN
--------------
hertz_to_mel
mel_to_hertz
_create_triangular_filter_bank
chroma_filter_bank
optimal_fft_length
get_mel_filter_banks
stft

RETURNS
--------------
hertz_to_octave
mel_filter_bank
window_function
spectrogram
power_to_db
amplitude_to_db
fram_wave
```


## Start pylsp server

```bash
pylsp -v --tcp --host localhost --port 2087
```

```bash
python src/lsp_clt.py 
```



## Using pyright

```bash
npm install -g pyright
```

```bash
pyright --verbose --dependencies src/parse.py > pyright_output.txt

python src/pyright_count.py pyright_output.txt
```


## Plan

- Use pyright verbose with dependencies flag
- Filter all the files to exclude
- Parse output to json
- Aggregate by imported by
- Keep 10
- Read files
- Extract functions
- LLM the function to confirm they are utility function
