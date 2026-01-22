def generate_answer(question, context_chunks):
    if not context_chunks:
        return "Answer not found in the document."

    # Render-safe extractive RAG answer
    return "\n".join(context_chunks[:3])
