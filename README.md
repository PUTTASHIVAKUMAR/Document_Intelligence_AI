# Document Intelligence AI

An end-to-end AI system that understands private documents and answers questions using semantic search and retrieval-augmented generation (RAG).

## Features
- PDF and image document ingestion
- OCR for scanned documents
- Semantic search using embeddings and FAISS
- LLM-based question answering
- Simple interactive Streamlit UI

## Tech Stack
- FastAPI
- OCR (Tesseract)
- Sentence Transformers
- FAISS
- Transformers (Flan-T5)
- Streamlit

## How It Works
1. Upload a document
2. Text is extracted and embedded
3. Relevant content is retrieved using semantic search
4. An LLM generates grounded answers from the document

## Use Cases
- Resume analysis
- Company recognition from documents
- Document search
- Internal knowledge assistants
