from core.gemini_config import model

def explain_note(text):
    prompt = f"""
    Explain this study note in simple language:

    {text}
    """

    response = model.generate_content(prompt)

    return response.text