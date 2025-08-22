from ..services.llm import query_openai
from ..prompts import *


def quiz(history):
    quiz_questions = query_openai(QUIZ_PROMPT.format(history=history), history)
    return quiz_questions
