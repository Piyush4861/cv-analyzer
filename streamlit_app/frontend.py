import streamlit as st
import requests
import os

st.title("📄 CV Analyzer with GenAI\n(Open-Source Model - Piyush Pate)")

uploaded_files = st.file_uploader("Upload CVs (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
query = st.text_input("Ask a question across all uploaded CVs")

if uploaded_files:
    os.makedirs("temp", exist_ok=True)
    files = []

    for file in uploaded_files:
        path = os.path.join("temp", file.name)
        with open(path, "wb") as f:
            f.write(file.read())
        files.append(("files", (file.name, open(path, "rb"), "application/octet-stream")))

    res = requests.post("http://localhost:8000/upload/", files=files)
    if res.status_code == 200:
        st.success("✅ Files uploaded successfully")
        st.json(res.json())
    else:
        st.error("❌ Upload failed")

if st.button("Ask") and query:
    response = requests.get(f"http://localhost:8000/ask/", params={"query": query})
    st.write("🤖", response.json().get("answer"))