import os
import re
import csv
import pdfplumber
import pytesseract
from docx import Document
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def extract_text_from_pdf(pdf_path):
    results = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                results.append(text)
            else:
                img = page.to_image(resolution=300).original.convert('RGB')
                ocr_text = pytesseract.image_to_string(img)
                results.append(ocr_text)
    return "\n\n".join(results)

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def parse_cv_info(text):
    info = {}
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    # Email first
    email_match = re.findall(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
    info["email"] = email_match[0] if email_match else "N/A"

    # Name logic
    name = "N/A"
    excluded_keywords = ['experience', 'education', 'summary', 'contact', 'skills', 'objective', 'developer', 'engineer', 'science']
    for line in lines[:20]:
        clean = line.strip()
        if (
            re.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+)+$", clean) and
            not any(word.lower() in clean.lower() for word in excluded_keywords)
        ):
            name = clean
            break
    if name == "N/A" and email_match:
        username = email_match[0].split('@')[0]
        parts = re.split(r'[._\d]+', username)
        cap = [p.capitalize() for p in parts if p]
        name = ' '.join(cap) if len(cap) >= 2 else cap[0]
    info["name"] = name

    # Phone
    phone_match = re.findall(r"(\+?\d[\d\s\-()]{8,15})", text)
    info["phone"] = re.sub(r"[^\d+]", "", phone_match[0]) if phone_match else "N/A"

    # Skills
    skill_keywords = [
        "python", "java", "c++", "html", "css", "javascript", "sql", "gcp", "aws",
        "azure", "docker", "kubernetes", "tensorflow", "pytorch", "linux", "git",
        "fastapi", "rest", "api", "selenium", "flask", "django", "oop"
    ]
    skills_found = set()
    for skill in skill_keywords:
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE):
            skills_found.add(skill.lower())
    info["skills"] = ", ".join(sorted(skills_found))

    # Education
    degree_keywords = [
        r"B\.?Tech", r"M\.?Tech", r"B\.?E", r"M\.?E", r"M\.?Sc", r"B\.?Sc", r"Ph\.?D", r"MBA",
        r"Bachelor(?:'s)? of [A-Za-z ]+", r"Master(?:'s)? of [A-Za-z ]+"
    ]
    education = []
    for pattern in degree_keywords:
        education.extend(re.findall(pattern, text, re.IGNORECASE))
    info["education"] = ", ".join(set(education))

    # Experience
    experience_lines = [
        line for line in lines
        if re.search(r"(experience|intern|years|developer|engineer|worked at|responsible for)", line, re.IGNORECASE)
    ]
    info["experience"] = ", ".join(experience_lines[:6])

    # Certifications
    certs = re.findall(r"(certified[^,\n\.]*|certification in [^,\n\.]*)", text, re.IGNORECASE)
    info["certifications"] = ", ".join(set(certs))

    return info

def process_all_cvs(folder_path):
    all_data = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.lower().endswith((".pdf", ".docx")):
            try:
                print(f"\n📄 Processing: {filename}")
                text = extract_text(file_path)
                data = parse_cv_info(text)
                data['filename'] = filename
                all_data.append(data)
                print("✅ Extracted Info:", data)
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")
    return all_data

def export_to_csv(data, output_file="output.csv"):
    if not data:
        print("No data to write.")
        return
    keys = data[0].keys()
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"\n📦 Data exported to {output_file}")

# ------------------ MAIN ------------------

if __name__ == "__main__":
    folder_path = "app/data/sample_cvs"
    extracted_data = process_all_cvs(folder_path)
    export_to_csv(extracted_data)