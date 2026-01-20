from transformers import pipeline

qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_new_tokens=120
)

def generate_answer(question, context_chunks):
    if not context_chunks:
        return "No relevant project information found."

    context = "\n".join(context_chunks)

    prompt = f"""
You are extracting information for a company recruiter.

Use ONLY the context.
If not found, say: Not mentioned.

Context:
{context}

Question:
{question}

Answer (bullet points, concise):
"""

    result = qa_pipeline(prompt)
    return result[0]["generated_text"].strip()
