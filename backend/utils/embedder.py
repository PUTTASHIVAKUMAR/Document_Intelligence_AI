import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Directory to store embeddings
EMBEDDING_DIR = "data/embeddings"
os.makedirs(EMBEDDING_DIR, exist_ok=True)

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# Helper: Chunk text
# -----------------------------
def chunk_text(text: str, chunk_size: int = 400):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))

    return chunks


# -----------------------------
# Helper: Deduplicate chunks
# -----------------------------
def deduplicate(chunks):
    seen = set()
    unique = []

    for c in chunks:
        key = c.strip().lower()
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return unique


# -----------------------------
# Create embeddings
# -----------------------------
def create_embeddings(text: str, doc_name: str):
    chunks = chunk_text(text)

    if not chunks:
        return

    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, f"{EMBEDDING_DIR}/{doc_name}.index")

    with open(f"{EMBEDDING_DIR}/{doc_name}_chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)


# -----------------------------
# Search embeddings
# -----------------------------
def search_embeddings(query: str, doc_name: str, top_k: int = 5):
    index_path = f"{EMBEDDING_DIR}/{doc_name}.index"
    chunk_path = f"{EMBEDDING_DIR}/{doc_name}_chunks.pkl"

    if not os.path.exists(index_path) or not os.path.exists(chunk_path):
        return []

    index = faiss.read_index(index_path)

    with open(chunk_path, "rb") as f:
        chunks = pickle.load(f)

    query_embedding = model.encode([query])
    _, indices = index.search(query_embedding, top_k)

    retrieved = [chunks[i] for i in indices[0]]

    # 🔥 HARD FILTER FOR PROJECT QUESTIONS
    if "project" in query.lower():
        retrieved = [
            c for c in retrieved
            if any(word in c.lower() for word in [
                "project", "developed", "system", "classification", "model"
            ])
        ]

    # ✅ Deduplicate + limit output
    retrieved = deduplicate(retrieved)

    return retrieved[:5]
