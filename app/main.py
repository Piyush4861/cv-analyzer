from fastapi import FastAPI, UploadFile, File
from app.parser import extract_text, parse_cv_info
from app.llm_agent import ask_llm
import os
import shutil

app = FastAPI()
cv_storage = []

@app.post("/upload/")
async def upload_cvs(files: list[UploadFile] = File(...)):
    global cv_storage
    cv_storage.clear()  # Clear previous uploads
    results = []

    folder = "app/data/sample_cvs"
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)

    for file in files:
        path = os.path.join(folder, file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())

        text = extract_text(path)
        data = parse_cv_info(text)
        data["filename"] = file.filename
        cv_storage.append(data)
        results.append(data)

    return {"status": "uploaded", "parsed": results}

@app.get("/ask/")
async def ask_query(query: str):
    if not cv_storage:
        return {"answer": "❌ No CVs uploaded yet."}

    # Optionally limit context size if model fails with long input
    context = "\n".join(str(cv) for cv in cv_storage)
    answer = ask_llm(context, query)
    return {"answer": answer}