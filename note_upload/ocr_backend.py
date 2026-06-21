import requests
import io
import os

API_KEY = os.getenv("OCR_SPACE_API_KEY")

def extract_text(image):

    img_bytes = io.BytesIO()

    image.save(img_bytes, format="PNG")

    img_bytes.seek(0)

    response = requests.post(
        "https://api.ocr.space/parse/image",
        files={
            "filename": (
                "image.png",
                img_bytes,
                "image/png"
            )
        },
        data={
            "apikey": API_KEY,
            "language": "eng",
            "isOverlayRequired": False
        }
    )

    result = response.json()

    if result.get("IsErroredOnProcessing"):
        return "OCR Failed"

    parsed = result.get("ParsedResults")

    if not parsed:
        return "No text found"

    return parsed[0]["ParsedText"]