from ..services.llm import query_openai
from ..prompts import *

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
        youtube_links = [link for link in citations if "youtube.com/watch" in link]

    except (json.JSONDecodeError, AttributeError):
        youtube_links = []

    content = youtube_links

    result_json = {
        "responseData": {
            "type": "links",
            "content": content,
            "explanation": explanation,
        }
    }
    print(json.dumps(result_json, indent=4))
    return result_json
