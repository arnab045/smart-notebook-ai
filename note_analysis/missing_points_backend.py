from core.gemini_config import model
from PIL import Image
import fitz

def detect_missing_points(file_path):

    if file_path.lower().endswith(".pdf"):

        pdf = fitz.open(file_path)

        max_pages = min(len(pdf), 10)

        images = []

        for page_num in range(max_pages):

            page = pdf.load_page(page_num)

            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2)
            )

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            images.append(image)

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
        [prompt] + images
    )

    return response.text