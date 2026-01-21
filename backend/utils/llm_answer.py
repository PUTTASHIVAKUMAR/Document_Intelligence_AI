from transformers import pipeline

# 🔴 DO NOT LOAD MODEL AT IMPORT TIME
_qa_pipeline = None

def get_qa_pipeline():
    global _qa_pipeline
    if _qa_pipeline is None:
        _qa_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-small",
            max_new_tokens=150
        )
    return _qa_pipeline


def generate_answer(question, context_chunks):
    if not context_chunks:
        return "Answer not found in the document."

    context = "\n".join(context_chunks)

    prompt = f"""
Answer ONLY the question using the context.
If the answer is not present, say: Answer not found in the document.

Context:
{context}

Question:
{question}

Answer (short, bullet points if possible):
"""

    qa_pipeline = get_qa_pipeline()
    result = qa_pipeline(prompt)

    return result[0]["generated_text"].strip()
