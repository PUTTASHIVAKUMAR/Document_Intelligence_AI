from sklearn.metrics.pairwise import cosine_similarity

def query_index(question, embeddings, chunks, top_k=3):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")

    q_emb = model.encode([question])
    sims = cosine_similarity(q_emb, embeddings)[0]

    top_idx = sims.argsort()[-top_k:][::-1]
    top_chunks = [chunks[i] for i in top_idx]

    answer = " ".join(top_chunks[:2])

    return answer, top_chunks
