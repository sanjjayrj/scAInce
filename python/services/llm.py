import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def query_openai(system_prompt, user_input, model="gpt-4o"):
    response = client.responses.create(
        model=model,
        instructions=system_prompt,
        input=user_input,
    )
    print(response.output_text)
    return response.output_text
    # return "unrelated"


# def codegen_openai(system_prompt, user_input):
#     response = openai.ChatCompletion.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_input},
#         ],
#         temperature=0.5,
#     )
#     return response.choices[0].message.content.strip()


def query_perplexity(system_prompt, user_input):
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "sonar",
        "prompt": system_prompt,
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.1,
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
        "Content-Type": "application/json",
    }

    return requests.request("POST", url, json=payload, headers=headers)
