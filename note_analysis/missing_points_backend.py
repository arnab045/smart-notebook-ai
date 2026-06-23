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


def detect_missing_points(file_path):

    image = Image.open(file_path)

    prompt = """
    Analyze this study note.

    Find:

    - Missing important points
    - Incomplete concepts
    - Important topics not included
    - Suggestions for improvement

    Give response in clean bullet points.
    """

    response = model.generate_content(
        [prompt, image]
    )

    return response.text