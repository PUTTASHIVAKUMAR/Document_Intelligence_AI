import streamlit as st
import requests

# ===============================
# CONFIG
# ===============================
BACKEND_URL = "https://your-backend-name.onrender.com"   # <-- CHANGE THIS to your real Render backend URL

st.set_page_config(page_title="Document Intelligence AI", layout="centered")

# ===============================
# UI
# ===============================
st.title("📄 Document Intelligence AI")
st.caption("Upload a document and ask questions from it.")

# ===============================
# UPLOAD
# ===============================
st.header("Upload Document")

uploaded_file = st.file_uploader(
    "Choose a PDF or Image",
    type=["pdf", "png", "jpg", "jpeg"],
    key="file_uploader"
)

# ===============================
# PROCESS UPLOAD
# ===============================
document_name = None

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    document_name = uploaded_file.name.rsplit(".", 1)[0]

    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue())
    }

    with st.spinner("Uploading & processing document..."):
        try:
            res = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=120)

            if res.status_code == 200:
                st.success("Document processed successfully ✅")
            else:
                st.error("Backend error while processing document ❌")

        except Exception as e:
            st.error(f"Connection error to backend ❌")
            st.stop()

# ===============================
# ASK QUESTION
# ===============================
st.header("Ask a Question")

question = st.text_input(
    "Enter your question",
    key="question_input_unique"
)

if document_name:
    st.text_input(
        "Document name",
        value=document_name,
        disabled=True,
        key="document_name_display_unique"
    )

ask_clicked = st.button("Ask", key="ask_button_unique")

# ===============================
# QUERY BACKEND
# ===============================
if ask_clicked:
    if not uploaded_file:
        st.warning("Please upload a document first")
        st.stop()

    if not question.strip():
        st.warning("Please enter a question")
        st.stop()

    params = {
        "question": question,
        "document": document_name
    }

    with st.spinner("Searching answer..."):
        try:
            res = requests.get(f"{BACKEND_URL}/ask", params=params, timeout=120)

            if res.status_code == 200:
                data = res.json()

                st.subheader("✅ Answer")
                st.write(data.get("answer", "No answer found"))

                st.subheader("📚 Source Chunks")
                sources = data.get("sources", [])
                if sources:
                    for i, chunk in enumerate(sources, 1):
                        st.markdown(f"**{i}.** {chunk}")
                else:
                    st.info("No source chunks returned")

            else:
                st.error("Backend error while answering ❌")

        except Exception as e:
            st.error("Failed to connect to backend ❌")
