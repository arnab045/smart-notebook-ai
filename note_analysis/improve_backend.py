import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

from core.gemini_config import model

def improve_note(text):
    prompt = f"""
    Improve and organize this study note properly:
    Rules:
    - Fix OCR mistakes
    - Fix grammar
    - Add missing concepts
    - Add headings
    - Add bullet points
    - Make exam friendly
    - Preserve original meaning
    {text}
    """

    response = model.generate_content(prompt)

    return response.text