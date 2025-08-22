import re

def clean_code(code: str) -> str:
    return code.strip().strip("`")


def extract_code(response_text):
    code_blocks = re.findall(r"```(?:python)?(.*?)```", response_text, re.DOTALL)
    return "\n\n".join(block.strip() for block in code_blocks) if code_blocks else ""


def append_code_to_content(content: dict, code_prompt_output: str):
    """
    Extracts HTML, CSS, and JS from the `code_prompt_output` and appends it to `content` dictionary.
    """
    # Regular expressions to capture HTML, CSS, and JS content
    html_match = re.search(r"html:\s*```(.*?)```", code_prompt_output, re.DOTALL)
    css_match = re.search(r"css:\s*```(.*?)```", code_prompt_output, re.DOTALL)
    js_match = re.search(r"js:\s*```(.*?)```", code_prompt_output, re.DOTALL)

    # Extracted values (replace escaped quotes)
    html_content = html_match.group(1) if html_match else ""
    css_content = css_match.group(1) if css_match else ""
    js_content = js_match.group(1) if js_match else ""

    # Append extracted values to `content`
    content["html"] = html_content
    content["css"] = css_content
    content["js"] = js_content

    return content
