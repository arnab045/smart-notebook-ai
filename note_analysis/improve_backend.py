from core.gemini_config import model
from PIL import Image
import fitz

def improve_note(file_path):

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

    prompt = f"""
    You are an expert university professor.

    The uploaded document contains {max_pages} pages.

    Read ALL pages carefully before answering.

    Do not summarize.

    For every topic found:

    1. Topic Name
    2. Existing Content
    3. Missing Concepts
    4. Missing Definitions
    5. Missing Formulas
    6. Missing Examples
    7. Missing Diagrams
    8. Detailed Explanation
    9. Exam Preparation Tips

    Mention page references whenever possible.

    Return a detailed enhancement report.
    """

    response = model.generate_content(
        [prompt] + images
    )

    return response.text