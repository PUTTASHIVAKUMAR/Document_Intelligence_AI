from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
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

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

documents_store = {}
indexes_store = {}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(DATA_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        chunks = extract_text(file_path)

        if not chunks:
            return {"status": "error", "message": "No text extracted"}

        embeddings = build_index(chunks)

        doc_name = file.filename.rsplit(".", 1)[0]

        documents_store[doc_name] = chunks
        indexes_store[doc_name] = embeddings

        return {"status": "success", "chunks": len(chunks)}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ask")
def ask(question: str, document: str):
    try:
        if document not in documents_store:
            return {"status": "error", "message": "Document not found"}

        chunks = documents_store[document]
        embeddings = indexes_store[document]

        answer, sources = query_index(question, embeddings, chunks)

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
