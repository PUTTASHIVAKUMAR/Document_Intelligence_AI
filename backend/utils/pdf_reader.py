import fitz  # PyMuPDF
import io

def extract_text(pdf_bytes: bytes) -> str:
    text = ""
    pdf_stream = io.BytesIO(pdf_bytes)
    doc = fitz.open(stream=pdf_stream, filetype="pdf")

    for page in doc:
        text += page.get_text()

    return text
