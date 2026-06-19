from core.gemini_config import model


def ask_general_tutor(user_question):

    prompt = f"""
    You are a friendly AI tutor.

    Help the student with their question.

    QUESTION:
    {user_question}

    Answer in a simple, educational, and helpful way.
    """

    response = model.generate_content(prompt)

    return response.text