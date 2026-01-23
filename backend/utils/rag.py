from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def query_index(question, embeddings, chunks, top_k=3):
    if len(embeddings) == 0:
        return "No data available", []

    model = get_model()
    q_emb = model.encode([question])

    sims = cosine_similarity(q_emb, embeddings)[0]
    top_idx = sims.argsort()[-top_k:][::-1]

    top_chunks = [chunks[i] for i in top_idx]

    answer = " ".join(top_chunks[:2])

    return answer, top_chunks
