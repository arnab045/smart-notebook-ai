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


def detect_missing_points(text):

    prompt = f"""
    Analyze this study note carefully.

    Find:
    - Missing important points
    - Incomplete concepts
    - Important topics not included
    - Suggestions for improvement

    Give response in clean bullet points.

    Note:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text