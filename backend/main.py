from fastapi import FastAPI, UploadFile, File
import os
from utils.pdf_reader import extract_text
from utils.embedder import create_embeddings, search_embeddings
from utils.llm_answer import generate_answer

app = FastAPI(title="Document Intelligence AI")

os.makedirs("data/processed", exist_ok=True)

@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    filename = file.filename
    name = filename.rsplit(".", 1)[0]

    file_path = f"data/processed/{filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)
    create_embeddings(text, name)

    return {
        "filename": filename,
        "characters_extracted": len(text)
    }

@app.get("/search")
def semantic_search(query: str, document: str):
    results = search_embeddings(query, document)
    return {"query": query, "results": results}

@app.get("/ask")
def ask_question(question: str, document: str):
    chunks = search_embeddings(question, document)
    answer = generate_answer(question, chunks)

    return {
        "question": question,
        "answer": answer,
        "sources": chunks
    }
