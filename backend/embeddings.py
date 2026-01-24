import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

DATA_DIR = "data/embeddings"
os.makedirs(DATA_DIR, exist_ok=True)

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def chunk_text(text, size=400):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

def create_embeddings(text: str, doc_name: str):
    model = get_model()
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, f"{DATA_DIR}/{doc_name}.index")

    with open(f"{DATA_DIR}/{doc_name}.pkl", "wb") as f:
        pickle.dump(chunks, f)

def search_embeddings(query: str, doc_name: str, top_k=5):
    index_path = f"{DATA_DIR}/{doc_name}.index"
    chunk_path = f"{DATA_DIR}/{doc_name}.pkl"

    if not os.path.exists(index_path):
        return []

    model = get_model()
    index = faiss.read_index(index_path)

    with open(chunk_path, "rb") as f:
        chunks = pickle.load(f)

    q_emb = model.encode([query])
    _, idx = index.search(q_emb, top_k)

    return [chunks[i] for i in idx[0]]
