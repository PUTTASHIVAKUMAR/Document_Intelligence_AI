import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

EMBEDDING_DIR = "data/embeddings"
os.makedirs(EMBEDDING_DIR, exist_ok=True)

# Lazy model load
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def chunk_text(text, chunk_size=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks


def deduplicate(chunks):
    seen = set()
    unique = []
    for c in chunks:
        key = c.strip().lower()
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique


def create_embeddings(text: str, doc_name: str):
    chunks = deduplicate(chunk_text(text))
    model = get_model()

    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, f"{EMBEDDING_DIR}/{doc_name}.index")

    with open(f"{EMBEDDING_DIR}/{doc_name}_chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)


def search_embeddings(query: str, doc_name: str, top_k=5):
    index_path = f"{EMBEDDING_DIR}/{doc_name}.index"
    chunk_path = f"{EMBEDDING_DIR}/{doc_name}_chunks.pkl"

    if not os.path.exists(index_path):
        return []

    model = get_model()
    index = faiss.read_index(index_path)

    with open(chunk_path, "rb") as f:
        chunks = pickle.load(f)

    query_embedding = model.encode([query])
    _, indices = index.search(query_embedding, top_k)

    return [chunks[i] for i in indices[0]]
