
import fitz  # PyMuPDF

def extract_text(file_path: str):
    doc = fitz.open(file_path)
    chunks = []

    for page in doc:
        text = page.get_text("text").strip()
        if text:
            chunks.append(text)

    return chunks
