import json

from ..services.llm import query_openai
from ..services.parsing import append_code_to_content, clean_code, extract_code
from ..services.manim_runner import run_generated_code

from ..prompts import *

def general(user_query):
    content = {}
    explanation = query_openai(TEXT_PROMPT, user_query)
    type = "text"
    # tool = query_openai(TOOL_PROMPT, user_query)
    tool = "webpage"

    if tool == "Manim":
        type = "Manim"
        code = query_openai(MANIM_PROMPT, user_query)
        print(code)
        # Execute the generated code
        run_result, video_path = run_generated_code(clean_code(extract_code(code)))
        # Build the JSON response in the required format
        if run_result.get("execution_type") == "manim":
            content["video_path"] = video_path
    elif tool == "Plotly":
        type = "code"
        code = query_openai(PLOTLY_PROMPT, user_query)
        content["Plotly"] = code
    else:
        type = "code"
        code = query_openai(CODE_PROMPT, user_query)
        print(code)
        content = append_code_to_content(content, code)

    result_json = {
        "responseData": {"type": type, "content": content, "explanation": explanation}
    }
    print(json.dumps(result_json, indent=4))
    return result_json
