from .llm import query_openai


def get_intent(user_input):
    prompt = (
        "You are an AI tutor. Your sole purpose is tutoring. "
        "Analyze the following user input. If it is related to tutoring or study, reply with 'tutoring'. "
        "If it is unrelated, reply with 'unrelated'. "
        "Simulations are considered tutoring. "
        "Return only the keyword.\n\n"
    )

    # return query_openai(prompt, user_input)
    return "tutoring"


def get_subject(user_input):
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
    )
    return query_openai(subject_prompt, user_input)
