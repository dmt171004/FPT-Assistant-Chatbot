# app/rag/chunker.py
import re

def semantic_chunk(documents, max_length=800):
    chunks = []

    for doc in documents:
        text = doc["content"]
        page = doc["page"]

        # Tách theo heading / bullet / bước
        sections = re.split(
            r"\n(?=(?:BƯỚC|LƯU Ý|CHÚ Ý|HƯỚNG DẪN|NOTE|STEP|\d+\.) )",
            text,
            flags=re.IGNORECASE
        )

        buffer = ""
        for sec in sections:
            if len(buffer) + len(sec) < max_length:
                buffer += "\n" + sec
            else:
                chunks.append({
                    "text": buffer.strip(),
                    "page": page
                })
                buffer = sec

        if buffer.strip():
            chunks.append({
                "text": buffer.strip(),
                "page": page
            })

    return chunks
