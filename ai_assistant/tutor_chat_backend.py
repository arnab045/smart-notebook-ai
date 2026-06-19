from core.gemini_config import model

def ask_tutor(
    note_text,
    chat_history,
    user_question
):

    prompt = f"""
You are Dr. Albert Einstein,
a friendly AI tutor.

Use the student's note and previous conversation.

NOTE:

{note_text}

PREVIOUS CONVERSATION:

{chat_history}

CURRENT QUESTION:

{user_question}

Rules:

- Answer based on the note whenever possible.
- Remember previous questions.
- Explain step-by-step.
- Use examples.
- Use bullet points when useful.
"""

    response = model.generate_content(prompt)

    return response.text