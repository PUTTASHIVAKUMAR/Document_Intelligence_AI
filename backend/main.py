from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import fitz  # PyMuPDF

from embeddings import create_embeddings
from rag import query_index

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text using PyMuPDF
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()

    doc_name = file.filename.rsplit(".", 1)[0]
    create_embeddings(text, doc_name)

    return {"status": "success", "document": doc_name}

@app.get("/ask")
def ask(question: str, document: str):
    answer, sources = query_index(question, document)
    return {
        "answer": answer,
        "sources": sources
    }
