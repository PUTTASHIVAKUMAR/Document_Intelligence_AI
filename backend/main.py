from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import traceback

from utils.pdf_reader import extract_text
from utils.embedder import build_index
from utils.rag import query_index

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

documents_store = {}
embeddings_store = {}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(DATA_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract text
        text_chunks = extract_text(file_path)

        if not text_chunks or len(text_chunks) == 0:
            return {"status": "error", "message": "No text extracted from document"}

        # Build embeddings
        embeddings = build_index(text_chunks)

        doc_name = file.filename.rsplit(".", 1)[0]

        documents_store[doc_name] = text_chunks
        embeddings_store[doc_name] = embeddings

        return {
            "status": "success",
            "document": doc_name,
            "chunks": len(text_chunks)
        }

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        print(traceback.format_exc())
        return {
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }

@app.get("/ask")
def ask(question: str, document: str):
    try:
        if document not in embeddings_store:
            return {"status": "error", "message": "Document not found"}

        chunks = documents_store[document]
        embeddings = embeddings_store[document]

        answer, sources = query_index(question, embeddings, chunks)

        return {
            "status": "success",
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        print("ASK ERROR:", str(e))
        print(traceback.format_exc())
        return {
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }
