import fitz
import os


def create_enhanced_pdf(
    original_pdf_path,
    improved_content,
    title
):

    pdf = fitz.open(
        original_pdf_path
    )

    page = pdf.new_page()

    y = 50

    # Main Title

    page.insert_text(
        (50, y),
        "AI ENHANCED REPORT",
        fontsize=20
    )

    y += 35

    page.insert_text(
        (50, y),
        f"Title: {title}",
        fontsize=12
    )

    y += 35

    page.insert_text(
        (50, y),
        "=" * 60,
        fontsize=10
    )

    y += 25

    lines = improved_content.split("\n")

    for line in lines:

        line = line.strip()

        if not line:

            y += 10
            continue

        # New page if current page full

        if y > 750:

            page = pdf.new_page()
            y = 50

        # ### Heading

        if line.startswith("###"):

            line = line.replace(
                "###",
                ""
            ).strip()

            page.insert_text(
                (50, y),
                line,
                fontsize=14
            )

            y += 24

        # ## Sub Heading

        elif line.startswith("##"):

            line = line.replace(
                "##",
                ""
            ).strip()

            page.insert_text(
                (50, y),
                line,
                fontsize=16
            )

            y += 28

        # # Main Heading

        elif line.startswith("#"):

            line = line.replace(
                "#",
                ""
            ).strip()

            page.insert_text(
                (50, y),
                line,
                fontsize=18
            )

            y += 32

        # Bullet Point

        elif (
            line.startswith("-")
            or line.startswith("*")
        ):

            page.insert_text(
                (70, y),
                f"• {line[1:].strip()}",
                fontsize=11
            )

            y += 18

        # Normal Text

        else:

            wrapped_lines = []

            words = line.split()

            current_line = ""

            for word in words:

                temp = (
                    current_line
                    + " "
                    + word
                ).strip()

                if len(temp) < 100:

                    current_line = temp

                else:

                    wrapped_lines.append(
                        current_line
                    )

                    current_line = word

            if current_line:

                wrapped_lines.append(
                    current_line
                )

            for wrapped in wrapped_lines:

                if y > 750:

                    page = pdf.new_page()
                    y = 50

                page.insert_text(
                    (50, y),
                    wrapped,
                    fontsize=11
                )

                y += 16

    output_path = (
        original_pdf_path.replace(
            ".pdf",
            "_enhanced.pdf"
        )
    )

    pdf.save(output_path)

    pdf.close()

    return output_path