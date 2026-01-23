from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def build_index(chunks):
    if not chunks:
        return []

    model = get_model()
    embeddings = model.encode(chunks)
    return embeddings
