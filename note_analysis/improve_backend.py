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
from PIL import Image


def improve_note(file_path):

    image = Image.open(file_path)

    prompt = """
    Improve this study note.

    Rules:

    - Fix mistakes
    - Add missing concepts
    - Add explanations
    - Add headings
    - Add bullet points
    - Make exam friendly

    Return clean plain text only.

    Do not use markdown.
    """

    response = model.generate_content(
        [prompt, image]
    )

    return response.text