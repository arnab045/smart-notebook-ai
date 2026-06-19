from core.gemini_config import model

def prepare_exam(note_text):

    prompt = f"""
    You are an expert exam preparation assistant.

    Analyze this study note.

    Generate:

    1. Most Important Topics
    2. Frequently Asked Exam Questions
    3. Important Short Questions
    4. Important MCQ Concepts
    5. Last Minute Revision Tips

    Format clearly using headings and bullet points.

    NOTE:

    {note_text}
    """

    response = model.generate_content(prompt)

    return response.text