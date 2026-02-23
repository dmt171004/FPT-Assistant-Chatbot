# app/rag/parser.py
import pdfplumber

def load_pdf(path: str):
    documents = []

    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            cleaned = (
                text.replace("\u00a0", " ")
                    .replace("\n\n", "\n")
                    .strip()
            )

            documents.append({
                "content": cleaned,
                "page": i + 1
            })

    return documents
