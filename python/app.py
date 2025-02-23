import re
import os
import sys
import json
import openai
import subprocess
from dotenv import load_dotenv
import requests
import shutil

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException


# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_intent(user_input):
    prompt = (
        "You are an AI tutor. Your sole purpose is tutoring. "
        "Analyze the following user input. If it is related to tutoring or study, reply with 'tutoring'. "
        "If it is unrelated, reply with 'unrelated'. "
        "Simulations are considered tutoring. "
        "Return only the keyword.\n\n"
        f"User input: {user_input}\nResponse:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()


def get_subject(user_input):
    # Replace the prompt below with your ready subject identification prompt.
    subject_prompt = (
        """You are an AI designed to classify questions into their corresponding academic subject. Your task is to read a given question and **respond with only one word** indicating the subject it belongs to.  
        ## Core Rules
            1. **Only respond with one-word subject names** (e.g., "Math", "History", "Chemistry", "English", "Geography", "Physics", etc.).
            2. **Do not provide explanations, additional text, or formatting.**
            3. **Ensure the subject classification is accurate based on the question\u2019s content.**
            4. **If the subject is unclear, return "General".**
            5. **Never ask for clarification\u2014make the best classification based on the given question.**
            6. **Do not return topics or descriptions\u2014only the academic subject name.**

        ---

        ## Example Responses

            - **User Query:** "What is the Pythagorean theorem?"  
            **Response:**  
            ```
            Math
            ```

            - **User Query:** "Who wrote 'Romeo and Juliet'?"  
            **Response:**  
            ```
            English
            ```

            - **User Query:** "When did World War II end?"  
            **Response:**  
            ```
            History
            ```

            - **User Query:** "What is Newton's First Law of Motion?"  
            **Response:**  
            ```
            Physics
            ```

            - **User Query:** "What are the main layers of the Earth?"  
            **Response:**  
            ```
            Geography
            ```
    """
        f"User input: {user_input}\nSubject:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": subject_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()


def query_openai(system_prompt, user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()


def query_perplexity(system_prompt, user_input):
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "sonar",
        "prompt": system_prompt,
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
        "Content-Type": "application/json"
    }

    return requests.request("POST", url, json=payload, headers=headers)


def codegen_openai(system_prompt, user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


def clean_code(code: str) -> str:
    return code.strip().strip("`")


def extract_code(response_text):
    code_blocks = re.findall(r"```(?:python)?(.*?)```",
                             response_text, re.DOTALL)
    return "\n\n".join(block.strip() for block in code_blocks) if code_blocks else ""


def run_generated_code(code):
    temp_filename = "temp_generated.py"
    print("[DEBUG] Saving generated code to:", temp_filename)

    with open(temp_filename, "w") as f:
        f.write(code)

    try:
        if "from manim import" in code:
            print("[DEBUG] Detected Manim script. Searching for Scene class...")

            match = re.search(r"class\s+(\w+)\(Scene\):", code)
            scene_class = match.group(1) if match else None

            if scene_class:
                print(
                    f"[DEBUG] Found Scene class: {scene_class}. Executing Manim...")
                cmd = ["manim", "-pql", temp_filename, scene_class]
                print("[DEBUG] Running command:", " ".join(cmd))

                proc = subprocess.run(
                    cmd, capture_output=True, text=True, check=True)

                output_log = proc.stdout + "\n" + proc.stderr

                original_video_path = os.path.join(
                    os.getcwd(), "media", "videos", "temp_generated", "480p15", f"{scene_class}.mp4"
                )

                destination_dir = os.path.join(os.getcwd(), "..", "app", "public", "videos")
                return_dir = os.path.join("videos", f"{scene_class}.mp4")

                os.makedirs(destination_dir, exist_ok=True)  # Ensure directory exists
                final_video_path = os.path.join(destination_dir, f"{scene_class}.mp4")

                if os.path.exists(original_video_path):
                    print(f"[DEBUG] Moving video from {original_video_path} to {final_video_path}")
                    shutil.move(original_video_path, final_video_path)
                else:
                    print("[WARNING] Generated video not found at:", original_video_path)


                # print(f"[DEBUG] Video Path: {video_path if video_path != 'Not found' else 'No output found'}")
                return {"execution_type": "manim", "output_log": output_log, "video_path": return_dir}, return_dir

            else:
                print("[DEBUG] No Scene class found. Skipping Manim execution.")

        print("[DEBUG] Running as standard Python script...")
        proc = subprocess.run([sys.executable, temp_filename],
                              capture_output=True, text=True, check=True)
        output_log = proc.stdout + "\n" + proc.stderr

        print("[DEBUG] Python script execution completed.")
        return {"execution_type": "python", "output_log": output_log}, return_dir

    except subprocess.CalledProcessError as e:
        print("[ERROR] Execution failed:", e)
        print("[ERROR] STDERR:", e.stderr)
        return {"execution_type": "error", "output_log": f"Execution failed: {e}\n{e.stderr}"}, "Not Found"


def append_code_to_content(content: dict, code_prompt_output: str):
    """
    Extracts HTML, CSS, and JS from the `code_prompt_output` and appends it to `content` dictionary.
    """
    # Regular expressions to capture HTML, CSS, and JS content
    html_match = re.search(r'html:\s*```(.*?)```',
                           code_prompt_output, re.DOTALL)
    css_match = re.search(r'css:\s*```(.*?)```', code_prompt_output, re.DOTALL)
    js_match = re.search(r'js:\s*```(.*?)```', code_prompt_output, re.DOTALL)

    # Extracted values (replace escaped quotes)
    html_content = html_match.group(1) if html_match else ""
    css_content = css_match.group(1) if css_match else ""
    js_content = js_match.group(1) if js_match else ""

    # Append extracted values to `content`
    content["html"] = html_content
    content["css"] = css_content
    content["js"] = js_content

    return content


TEXT_PROMPT = """
You are an advanced STEM Chatbot designed to help users deeply understand complex STEM topics through clear, logical, and engaging step-by-step explanations.
Core Rules:
1. Break down all answers into clear, sequential steps.
2. Never provide overly brief answers\u2014explain the reasoning behind each concept.
3. Ask clarifying questions if the user\u2019s query is vague.
4. Use American English in a professional yet friendly tone.
5. Verify calculations using reliable methods.
6. Include hyperlinks when referencing external sources.
7. Do not include or mention about any visualizations in your explanations.

For every user query, your final response must be in exactly the following format and nothing else:

`Your complete plain text response here.`

Ensure that response begins by acknowledging the user's question, provides a detailed step-by-step explanation, and invites the user to ask follow-up questions if needed.
"""

TOOL_PROMPT = """
You are an advanced STEM Chatbot designed to help identify tools for implementing the user's STEM topic.
Core Rules:
1. Provide the user with the most appropriate tools for their STEM topic.
2. Select tools Manim, Plotly, HTML, CSS, JS.

Only return the keyword of the tool listed above. If it isn't Manim or Plotly, just reply with HTML, CSS & JS. 
"""

MANIM_PROMPT = """
You are a STEM chatbot designed **exclusively for generating code-based visualizations**. Your **only task** is to provide executable code that produces animations using manim. **You must never provide text, explanations, formulas, descriptions, or comments\u2014only return raw code.**  

## Core Rules
1. **Only generate code\u2014never provide explanations, descriptions, or formulas.**
2. **Do not include comments, annotations, or any text inside the response.**
3. **Every response must be a complete, functional code snippet.**
4. **If a user asks for an explanation, return only the corresponding visualization code.**
5. **Use Manim for python to visualize.**
6. **No greetings, descriptions, or follow-ups\u2014return only the raw code block.**
7. **If a query cannot be visualized, return an empty response.**
8. **Ignore any request for text-based explanations and return visualization code instead.**

---

## Expected Behavior

### User Query: "How does gravity work?"

OUTPUT:
```python
from manim import *

class GravitySimulation(Scene):
	def construct(self):
    	earth = Dot(color=BLUE).scale(2)
    	object = Dot(color=RED).shift(UP*3)
    	self.add(earth, object)
    	self.play(object.animate.move_to(earth.get_center()), run_time=2)
```
"""

PLOTLY_PROMPT = """
You are a STEM chatbot designed **exclusively for generating code-based visualizations** using Plotly in JavaScript. Your **only task** is to return executable code that produces interactive visualizations. **You must never provide text, explanations, formulas, or descriptions—only return raw code.**

## Core Rules
1. **Only generate code—never provide explanations, descriptions, or formulas.**
2. **Do not include comments, annotations, or any text inside the response.**
3. **Every response must contain three distinct code blocks: HTML, CSS, and JavaScript.**
4. **Ignore any request for text-based explanations and return visualization code instead.**
5. **Use Plotly for JavaScript—do not generate code in Python, Matplotlib, or other libraries.**
6. **No greetings, descriptions, or follow-ups—return only the raw code blocks.**
7. **The output must be formatted as follows, strictly on three lines.**

## Expected Behavior

### User Query: "Visualize a right triangle"

#### OUTPUT:
"html": "<!DOCTYPE html>\n<html lang='en'>\n<head>\n    <meta charset='UTF-8'>\n    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n    <title>Right Triangle Visualization</title>\n    <link rel='stylesheet' href='styles.css'>\n    <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>\n</head>\n<body>\n    <div id='triangle-plot'></div>\n    <script src='script.js'></script>\n</body>\n</html>",
"css": "body {\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    height: 100vh;\n    background-color: #f0f0f0;\n}\n#triangle-plot {\n    width: 600px;\n    height: 600px;\n}",
"js": "document.addEventListener('DOMContentLoaded', function() {\n    var trace = {\n        x: [0, 3, 0, 0],\n        y: [0, 0, 4, 0],\n        type: 'scatter',\n        mode: 'lines+markers',\n        marker: { size: 8, color: 'red' },\n        line: { width: 3 }\n    };\n\n    var layout = {\n        title: 'Right Triangle',\n        xaxis: { range: [-1, 5] },\n        yaxis: { range: [-1, 5] },\n        showlegend: false\n    };\n\n    Plotly.newPlot('triangle-plot', [trace], layout);\n});"

"""

CODE_PROMPT = """
You are an AI designed to generate code snippets for the user's query. Your task is to provide the user with the most appropriate code snippet based on their query. You can generate code snippets in JavaScript, HTML and CSS.

## Core Rules
1. **Only generate code\u2014never provide explanations, descriptions, or formulas.**
2. **If a user asks for an explanation, return only the corresponding visualization code.**
3. **No greetings, descriptions, or follow-ups\u2014return only the raw code block in the format given at the bottom.**
4. **If a query cannot be visualized, return an empty response.**
5. **Ignore any request for text-based explanations and return visualization code instead.**
6. **Do not give matplotlib code for visualizations.**
7. **The visualization code must contain HTML, CSS, and JS.**

For every user query, your final response must be in exactly the following JSON format and nothing else:

html: ```<h1>Hello from AI</h1>```,
css: ```h1 { color: blue; text-align: center; }```,
js: ```console.log("AI-generated JavaScript running!");```

"""

LINK_PROMPT = """

You are an AI designed to **retrieve only YouTube video links** based on a user's query. Your responses **must contain only valid YouTube URLs** and nothing else\u2014no explanations, summaries, citations, or non-YouTube links.

## Core Rules
1. **Only return real YouTube links**\u2014never generate fake or placeholder links.
2. **Do not provide any explanations, descriptions, or text\u2014only YouTube URLs.**
3. **Each link must be on a new line, with no bullet points, formatting, or additional text.**
4. **If no relevant YouTube videos exist, return an empty response.**
5. **Never return website citations, summaries, or non-YouTube sources.**

---

## Expected Response Format

- **User Query:** "Best video explaining the Russian Revolution"  
  **Response:**  
  ```
  https://www.youtube.com/watch?v=abc123xyz
  https://www.youtube.com/watch?v=def456ghi
  ```

- **User Query:** "Show me a video about the Pythagorean theorem"  
  **Response:**  
  ```
  https://www.youtube.com/watch?v=jkl789mno
  ```

- **User Query:** "How does gravity work?"  
  **Response:**  
  ```
  https://www.youtube.com/watch?v=uvw987rst
  https://www.youtube.com/watch?v=xyz654mnp
  ```

- **User Query:** "Explain Shakespeare's Hamlet"  
  **Response:**  
  ```
  https://www.youtube.com/watch?v=qrs234tuv
  ```

- **User Query:** "Tell me about the Industrial Revolution"  
  **Response:**  
  ```
  https://www.youtube.com/watch?v=lmn567opq
  ```

- **User Query:** "Who is Albert Einstein?" *(Not relevant to YouTube videos)*  
  **Response:**  
  *(Returns an empty response.)*

"""

QUIZ_PROMPT = """
You are an AI designed to generate quiz questions based only on the conversation's chat history. Your task is to provide the user with the most appropriate quiz question based on the history. You can generate quiz questions in multiple-choice format.
The input query given by the user here is the history.
The questions are to be based on the history returned by the user. The correct answer should be one of the options provided.
Here is the history: {history}

## Core Rules
1. **Use only the chat history** to generate the quiz.
2. **Do not use any external sources, transcripts, or additional content.**
3. **Identify key concepts, facts, and discussions to form quiz questions.**
4. **Each quiz should have at least 5\u201310 questions** based on chat length.
5. **Keep questions clear, relevant, and well-structured.**
6. **Avoid unnecessary repetition**\u2014focus on distinct concepts from the chat history.
7. **Only generate the quiz**\u2014do not explain, summarize, or provide answers unless explicitly requested.


The multiple-choice questions generated **must** follow the format below:

const questions = [
    {
      question: "In a standard RGB color model, which color does 'G' represent?",
      options: ["Gray", "Green", "Gold", "Garnet"],
      correctAnswerIndex: 1,
    },
    {
      question: "Which HTML tag is used to define an unordered list?",
      options: ["<ul>", "<ol>", "<li>", "<list>"],
      correctAnswerIndex: 0,
    },
    {
      question: "In CSS, which property is used to change the text color?",
      options: ["font-color", "text-color", "color", "font-style"],
      correctAnswerIndex: 2,
    },
  ];
"""


def math(user_query):
    content = {}
    explanation = query_openai(TEXT_PROMPT, user_query)
    type = "text"
    tool = query_openai(TOOL_PROMPT, user_query)
    if tool == "Manim":
        type = "Manim"
        code = codegen_openai(MANIM_PROMPT, user_query)
        print(code)
        # Execute the generated code
        run_result, video_path = run_generated_code(
            clean_code(extract_code(code)))
        # Build the JSON response in the required format
        if run_result.get("execution_type") == "manim":
            content = video_path
    elif tool == "Plotly":
        type = "code"
        code = codegen_openai(PLOTLY_PROMPT, user_query)
        content = code
    else:
        type = "code"
        code = codegen_openai(CODE_PROMPT, user_query)
        print(code)
        content = append_code_to_content(content, code)

    result_json = {
        "responseData": {
            "type": type,
            "content": content,
            "explanation": explanation
        }
    }
    print(json.dumps(result_json, indent=4))
    return result_json

def phyChem(user_query):
    content = {}
    explanation = query_openai(TEXT_PROMPT, user_query)
    tool = query_openai(TOOL_PROMPT, user_query)
    type = "text"
    if tool == "Manim":
        type = "Manim"
        code = codegen_openai(MANIM_PROMPT, user_query)
        print(code)
        # Execute the generated code
        run_result, video_path = run_generated_code(
            clean_code(extract_code(code)))
        # Build the JSON response in the required format
        if run_result.get("execution_type") == "manim":
            content = video_path
    else:
        type = "code"
        code = codegen_openai(CODE_PROMPT, user_query)
        content = append_code_to_content(content, code)

    result_json = {
        "responseData": {
            "type": type,
            "content": content,
            "explanation": explanation
        }
    }
    print(json.dumps(result_json, indent=4))
    return result_json


def youtube_links(user_query):
    content = {}
    explanation = query_openai(TEXT_PROMPT, user_query)
    links = query_perplexity(LINK_PROMPT, user_query)

    try:
        # Parse the JSON response from Perplexity
        response_json = json.loads(links.text)

        # Extract citations if available
        citations = response_json.get("citations", [])

        # Filter out only YouTube links
        youtube_links = [
            link for link in citations if "youtube.com/watch" in link]

    except (json.JSONDecodeError, AttributeError):
        youtube_links = []

    content = youtube_links

    result_json = {
        "responseData": {
            "type": "links",
            "content": content,
            "explanation": explanation
        }
    }
    print(json.dumps(result_json, indent=4))
    return result_json


def quiz(history):
    quiz_questions = query_openai(QUIZ_PROMPT.format(history=history), history)
    return quiz_questions

def general(user_query):
    content = {}
    explanation = query_openai(TEXT_PROMPT, user_query)
    type = "text"
    tool = query_openai(TOOL_PROMPT, user_query)
    if tool == "Manim":
        type = "Manim"
        code = codegen_openai(MANIM_PROMPT, user_query)
        print(code)
        # Execute the generated code
        run_result, video_path = run_generated_code(
            clean_code(extract_code(code)))
        # Build the JSON response in the required format
        if run_result.get("execution_type") == "manim":
            content["video_path"] = video_path
    elif tool == "Plotly":
        type = "code"
        code = codegen_openai(PLOTLY_PROMPT, user_query)
        content["Plotly"] = code
    else:
        type = "code"
        code = codegen_openai(CODE_PROMPT, user_query)
        print(code)
        content = append_code_to_content(content, code)

    result_json = {
        "responseData": {
            "type": type,
            "content": content,
            "explanation": explanation
        }
    }
    print(json.dumps(result_json, indent=4))
    return result_json

def main():
    user_input = input("Enter your query: ")
    intent = get_intent(user_input)
    print(f"Intent: {intent}")

    if intent == "tutoring":
        subject = get_subject(user_input)
        print(f"Subject: {subject}")
        if subject == "Math":
            print("This is a Math-related query.")
            return math(user_input)
        elif subject == "Chemistry":
            print("This is a Chemistry-related query.")
            return phyChem(user_input)
        elif subject == "History":
            print("This is a History-related query.")
            return youtube_links(user_input)
        elif subject == "English":
            print("This is an English-related query.")
            return youtube_links(user_input)
        elif subject == "Geography":
            print("This is a Geography-related query.")
            return youtube_links(user_input)
        elif subject == "Physics":
            print("This is a Physics-related query.")
            return phyChem(user_input)
        else:
            print("General subject.")
            return general(user_input)
    else:
        print("Input not related to tutoring.")


app = FastAPI(title="Concept Explanation API", version="1.0")


class ChatRequest(BaseModel):
    prompt: str


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    POST /chat
    JSON body: { "prompt": "...", "mode": "explain" or "visual" }
    """
    try:
        intent = get_intent(request.prompt)
        user_input = request.prompt

        if intent == "tutoring":
            subject = get_subject(user_input)
            print(f"Subject: {subject}")
            if subject == "Math":
                print("This is a Math-related query.")
                return math(user_input)
            if subject == "Math":
                print("This is a Math-related query.")
                return math(user_input)
            elif subject == "Chemistry":
                print("This is a Chemistry-related query.")
                return phyChem(user_input)
            elif subject == "History":
                print("This is a History-related query.")
                return youtube_links(user_input)
            elif subject == "English":
                print("This is an English-related query.")
                return youtube_links(user_input)
            elif subject == "Geography":
                print("This is a Geography-related query.")
                return youtube_links(user_input)
            elif subject == "Physics":
                print("This is a Physics-related query.")
                return phyChem(user_input)
            else:
                print("General subject.")
                return general(user_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/quiz")
def chat_endpoint(request: ChatRequest):
    """
    POST /chat
    JSON body: { "prompt": "...", "mode": "explain" or "visual" }
    """
    try:
        quiz_output = quiz(request.chat_history)
        if quiz_output.startswith("const questions ="):
            quiz_output = quiz_output.replace("const questions =", "").strip().rstrip(";")
        questions = json.loads(quiz_output)
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))