import fitz
import textwrap
import os


def create_enhanced_pdf(
    original_pdf_path,
    improved_content,
    title
):

    pdf = fitz.open(
        original_pdf_path
    )

    wrapped_pages = textwrap.wrap(
        improved_content,
        width=2500
    )

    for chunk in wrapped_pages:

        page = pdf.new_page()

        page.insert_text(

            (50, 50),

            f"""
AI ENHANCED NOTES

Title:
{title}

--------------------------------

{chunk}
            """,

            fontsize=11

        )

    output_path = (

        original_pdf_path
        .replace(
            ".pdf",
            "_enhanced.pdf"
        )

    )

    pdf.save(output_path)

    pdf.close()

    return output_path