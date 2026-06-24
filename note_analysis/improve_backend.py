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
    You are an expert academic note reviewer.

    Analyze the uploaded note page by page.

    IMPORTANT RULES:

    1. Do NOT generate long reports.
    2. Do NOT generate proofs.
    3. Do NOT generate Hall's theorem.
    4. Do NOT generate research-level explanations.
    5. Do NOT generate unnecessary formulas.
    6. Focus only on the most important missing or weak points.
    7. Maximum 2-3 improvements per page.
    8. Tell what can be improved 
    9. Keep explanations simple and student-friendly.

    Output format:

    Page X

    Issue:
    What is missing, incorrect, or difficult to understand?

    Improved Version:
    Write a clearer and easier version.

    Example:
    Give one short example if necessary.

    --------------------------------

    Page Y

    Issue:
    ...

    Improved Version:
    ...

    Example:
    ...
    """

    response = model.generate_content(
        [prompt] + images
    )

    return response.text