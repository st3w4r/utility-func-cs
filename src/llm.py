import anthropic
import os
import sys


utility_function_prompt = """
Which function is an utlility function.
The set of critetias:
- Single, Specific Purpose
- Reusability
- Minimal Dependencies
- Simplicity
- Self-Contained
- General Use
- Utility
Just list the name of the function with True if it is an utility function False if not. No explanation,
"""

format_to_json_prompt = """
Use JSON format, return a list of object with "function_name" as string "is_utility" as boolean.
"""

format_to_json_prompt2 = """
Use JSON format, return a list of function names for all the utility function, and one list for the none utility function.
"""

claud_api_key = os.getenv("CLAUDE_API_KEY")

if claud_api_key is None:
    raise Exception("CLAUDE_API_KEY is not set")


class LLM():
    
    client = None

    def __init__(self):
        self.client = anthropic.Client(api_key=claud_api_key)

    def call(self, message):
        response = self.client.beta.tools.messages.create(
            max_tokens=300,
            # model="claude-2.1",
            # model="claude-3-opus-20240229",
            model="claude-3-sonnet-20240229",
            # model="claude-3-haiku-20240307",
            system=utility_function_prompt,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response

    def format_to_json(self, message):
        response = self.client.beta.tools.messages.create(
            max_tokens=1024,
            model="claude-3-haiku-20240307",
            system=format_to_json_prompt2,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response


if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python find_utils.py <file_path>")
        sys.exit(1)
    file = args[0]

    llm = LLM()
    with open(file, "r") as f:
        content = f.read()

    res = llm.call(content)

    print("RAW:")
    print(res.content[0].text)

    text = res.content[0].text
    format_to_json_res = llm.format_to_json(text)
    print("\nFORMATTED:")
    print(format_to_json_res.content[0].text)
