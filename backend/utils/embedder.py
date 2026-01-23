from sentence_transformers import SentenceTransformer

# Load model once (global singleton)
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def build_index(chunks: list[str]):
    """
    Convert text chunks into embeddings (in-memory)
    """
    if not chunks:
        return []

    model = get_model()
    embeddings = model.encode(chunks)
    return embeddings
