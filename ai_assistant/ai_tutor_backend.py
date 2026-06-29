from core.gemini_config import model


def ask_ai_tutor(
    question,
    note_title,
    note_content
):

    prompt = f"""
You are Smart Notebook AI Tutor.

A student has opened one specific study note.

Title:
{note_title}

Study Note:
{note_content}

Student Question:
{question}

Rules:

- Answer ONLY using this study note as the primary context.
- If necessary, use your own academic knowledge only to explain the note more clearly.
- Do not change the topic.
- Explain in simple language.
- Use bullet points when appropriate.
- Give examples whenever helpful.
- If the student asks for exam tips, provide concise exam-focused advice.
- If the answer is not present in the note, clearly mention that it is additional explanation.

Return only the answer.
"""

    response = model.generate_content(prompt)

    return response.text