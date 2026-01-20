import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io


def extract_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    full_text = []

    for page in doc:
        text = page.get_text().strip()

        # If text exists → normal PDF
        if text:
            full_text.append(text)
        else:
            # OCR fallback (scanned PDFs)
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            full_text.append(ocr_text)

    return "\n".join(full_text)
