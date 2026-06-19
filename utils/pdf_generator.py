from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    text,
    output_path
):

    doc = SimpleDocTemplate(
        output_path
    )

    styles =
        getSampleStyleSheet()

    content = []

    paragraphs =
        text.split("\n")

    for line in paragraphs:

        if line.strip():

            content.append(

                Paragraph(
                    line,
                    styles["BodyText"]
                )

            )

            content.append(
                Spacer(1, 8)
            )

    doc.build(content)

    return output_path