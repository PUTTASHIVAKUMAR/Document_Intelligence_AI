import streamlit as st
import requests

BACKEND_URL = "https://document-intelligence-ai.onrender.com"

st.set_page_config(page_title="Document Intelligence AI", layout="centered")
st.title("📄 Document Intelligence AI")
st.write("Upload a document and ask questions from it.")

st.header("Upload Document")
uploaded_file = st.file_uploader(
    "Choose a PDF or Image",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    files = {"file": uploaded_file}
    response = requests.post(f"{BACKEND_URL}/upload", files=files)

    if response.status_code == 200:
        st.success("Document uploaded and processed successfully")
        document_name = uploaded_file.name.rsplit(".", 1)[0]
    else:
        st.error("Upload failed")

st.header("Ask a Question")
question = st.text_input("Enter your question")
document = st.text_input("Document name (without extension)")
st.header("Ask a Question")
question = st.text_input("Enter your question")

document = None
if uploaded_file:
    document = uploaded_file.name.rsplit(".", 1)[0]
    st.text_input("Document name (auto-filled)", value=document, disabled=True)

st.header("Ask a Question")

question = st.text_input(
    "Enter your question",
    key="question_input"
)

document = None
if uploaded_file:
    document = uploaded_file.name.rsplit(".", 1)[0]
    st.text_input(
        "Document name (auto-filled)",
        value=document,
        disabled=True,
        key="doc_name_display"
    )

if st.button("Ask", key="ask_button"):
    if question and document:
        params = {
            "question": question,
            "document": document
        }
        response = requests.get(f"{BACKEND_URL}/ask", params=params)

        if response.status_code == 200:
            data = response.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Source Text")
            for chunk in data["sources"]:
                st.markdown(f"> {chunk}")
        else:
            st.error("Backend error while answering")
    else:
        st.warning("Upload document and enter a question")

