from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
import os

def extract_text(file_path: str) -> str:
    text = ""

    # PDF handling
    if file_path.lower().endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
        except Exception:
            text = ""

    # Image handling (OCR)
    else:
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
        except Exception:
            text = ""

    return text.strip()
