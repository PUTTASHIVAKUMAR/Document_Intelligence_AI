import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Document Intelligence AI", layout="centered")

st.title("📄 Document Intelligence AI")
st.write("Upload a document and ask questions from it.")

# Upload section
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
        st.info(f"Document name: {document_name}")
    else:
        st.error("Upload failed")

# Ask section
st.header("Ask a Question")
question = st.text_input("Enter your question")
document = st.text_input("Document name (without extension)")

if st.button("Ask"):
    if question and document:
        params = {"question": question, "document": document}
        response = requests.get(f"{BACKEND_URL}/ask", params=params)

        if response.status_code == 200:
            data = response.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Source Text")
            for chunk in data["sources"]:
                st.markdown(f"> {chunk}")
        else:
            st.error("Failed to get answer")
    else:
        st.warning("Enter both question and document name")
