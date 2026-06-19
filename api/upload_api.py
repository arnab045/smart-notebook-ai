from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io
import fitz
import os
import shutil

from note_upload.ocr_backend import extract_text

router = APIRouter()

# Create folders automatically

os.makedirs(
    "note_upload/original",
    exist_ok=True
)

os.makedirs(
    "note_upload/pdf",
    exist_ok=True
)

os.makedirs(
    "note_upload/page_images",
    exist_ok=True
)


@router.post("/extract-note")
async def extract_note(file: UploadFile = File(...)):

    print("REQUEST RECEIVED")

    try:

        contents = await file.read()

        print("FILE READ DONE")

        # =========================
        # SAVE ORIGINAL FILE
        # =========================

        original_path = (
            f"note_upload/original/{file.filename}"
        )

        with open(
            original_path,
            "wb"
        ) as f:

            f.write(contents)

        print(
            "ORIGINAL FILE SAVED:",
            original_path
        )

        filename = file.filename.lower()

        # =========================
        # PDF UPLOAD
        # =========================

        if filename.endswith(".pdf"):

            pdf_path = (
                f"note_upload/pdf/{file.filename}"
            )

            shutil.copy(
                original_path,
                pdf_path
            )

            file_type = "pdf"

            pdf_name = os.path.splitext(
                file.filename
            )[0]

            pdf_doc = fitz.open(
                stream=contents,
                filetype="pdf"
            )

            for page_num in range(len(pdf_doc)):

                page = pdf_doc.load_page(page_num)

                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2)
                )

                image_path = (
                    f"note_upload/page_images/"
                    f"{pdf_name}_page_{page_num + 1}.png"
                )

                pix.save(image_path)

            print(
                "PDF PAGE IMAGES CREATED"
            )

            pdf = fitz.open(
                stream=contents,
                filetype="pdf"
            )

            full_text = ""

            for page_num in range(len(pdf)):

                page = pdf.load_page(page_num)

                pix = page.get_pixmap()

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                full_text += (
                    extract_text(image)
                    + "\n"
                )

            extracted_text = full_text

            print(
                "PDF TEXT EXTRACTED"
            )

        # =========================
        # JPG / JPEG / PNG UPLOAD
        # =========================

        elif (

            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".png")

        ):

            pdf_filename = (
                os.path.splitext(
                    file.filename
                )[0]
                + ".pdf"
            )

            pdf_path = (
                f"note_upload/pdf/{pdf_filename}"
            )

            image = Image.open(
                io.BytesIO(contents)
            )

            image.convert(
                "RGB"
            ).save(
                pdf_path,
                "PDF"
            )

            file_type = "image"

            image_path = (
                f"note_upload/page_images/"
                f"{os.path.splitext(file.filename)[0]}_page_1.png"
            )

            image.save(image_path)

            print(
                "PAGE IMAGE CREATED"
            )

            print(
                "PDF CREATED:",
                pdf_path
            )

            extracted_text = extract_text(
                image
            )

            print(
                "IMAGE TEXT EXTRACTED"
            )

        # =========================
        # UNSUPPORTED FILE
        # =========================

        else:

            return {

                "success": False,

                "message":
                "Only PDF, JPG, JPEG and PNG are supported"

            }

        # =========================
        # SUCCESS RESPONSE
        # =========================

        return {

            "success": True,

            "text":
                extracted_text,

            "original_file_path":
                original_path,

            "pdf_path":
                pdf_path,

            "file_type":
                file_type

        }

    except Exception as e:

        print(
            "ERROR:",
            str(e)
        )

        return {

            "success": False,

            "message":
                str(e)

        }