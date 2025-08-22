import json
import traceback
from fastapi import FastAPI, HTTPException

from .models import ChatRequest
from .services.classifiers import get_intent, get_subject
from .tools import general, math, phyChem, quiz, youtube_links

app = FastAPI(title="Concept Explanation API", version="1.0", debug=True)

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    POST /chat
    JSON body: { "prompt": "...", "mode": "explain" or "visual" }
    """
    try:
        intent = get_intent(request.prompt)
        print(intent)
        user_input = request.prompt

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
    except Exception as e:
        traceback.print_exc()
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
            quiz_output = (
                quiz_output.replace("const questions =", "").strip().rstrip(";")
            )
        questions = json.loads(quiz_output)
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
