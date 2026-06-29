from core.gemini_config import model


def ask_ai_tutor(

    question,
    note_title,
    note_content,
    history

):

    conversation = ""

    for message in history:

        if message["role"] == "user":

            conversation += f"Student: {message['content']}\n"

        else:

            conversation += f"Tutor: {message['content']}\n"

    prompt = f"""
You are Smart Notebook AI Tutor.

A student is studying one uploaded note.

----------------------------------------

NOTE TITLE:
{note_title}

----------------------------------------

NOTE CONTENT:
{note_content}

----------------------------------------

PREVIOUS CONVERSATION:

{conversation}

----------------------------------------

CURRENT QUESTION:

{question}

----------------------------------------

Rules:

1. Always answer based on the uploaded note.

2. Use previous conversation as context.

3. If the student says:
- Explain more
- Continue
- Give another example
- Why?
- Simplify it
- Explain again

You MUST understand what they are referring to from the previous conversation.

4. Explain like a friendly university tutor.

5. Use simple English.

6. Use bullet points whenever helpful.

7. Give examples whenever appropriate.

8. If the answer is outside the uploaded note, clearly mention that it is additional explanation.

Return only the answer.
"""

    response = model.generate_content(prompt)

    return response.text