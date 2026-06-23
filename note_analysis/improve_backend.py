from core.gemini_config import model
from PIL import Image
import fitz

def improve_note(file_path):

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
    Improve this study note.

    Rules:

    - Fix mistakes
    - Add missing concepts
    - Add explanations
    - Add headings
    - Add bullet points
    - Make exam friendly

    Return clean plain text only.
    """

    response = model.generate_content(
        [prompt, image]
    )

    return response.text