from core.gemini_config import model
from PIL import Image
import fitz

def detect_missing_points(file_path):

    if file_path.lower().endswith(".pdf"):

        pdf = fitz.open(file_path)

        page = pdf.load_page(0)

        pix = page.get_pixmap(
            matrix=fitz.Matrix(3, 3)
        )

        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

    else:

        image = Image.open(file_path)

    prompt = """
    Analyze this study note.

    Find:

    - Missing important points
    - Incomplete concepts
    - Important topics not included
    - Suggestions for improvement

    Return clean bullet points only.
    """

    response = model.generate_content(
        [prompt, image]
    )

    return response.text