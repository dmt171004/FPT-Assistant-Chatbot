import os
import faiss
import json
import numpy as np
from openai import OpenAI
from app.core.config import OPENAI_API_KEY, VECTOR_STORE_DIR, RAG_DATA_DIR

client = OpenAI(api_key=OPENAI_API_KEY)
EMBEDDING_MODEL = "text-embedding-3-large"

# Load Index và Metadata khi khởi tạo service
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index.faiss")
META_PATH = os.path.join(VECTOR_STORE_DIR, "metadata.json")

# Khởi tạo biến toàn cục để lưu trữ index và dữ liệu
_index = None
_metadata = []

def load_resources():
    global _index, _metadata
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        _index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "r", encoding="utf-8") as f:
            _metadata = json.load(f)
        print("✅ RAG Resources loaded successfully")
    else:
        print("⚠ RAG Index or Metadata not found. Please run loader.py first.")

# Load ngay khi import
load_resources()

def retrieve_context(query: str, top_k: int = 3):
    if _index is None:
        return "Hệ thống dữ liệu đang được cập nhật, vui lòng thử lại sau.", []

    # 1. Tạo embedding cho câu hỏi
    query_emb = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    ).data[0].embedding
    
    # 2. Search trên FAISS
    D, I = _index.search(np.array([query_emb]).astype("float32"), top_k)
    
    context = ""
    source_documents = [] # Để trả về thông tin file và trang cho frontend

    for i in I[0]:
        if i != -1 and i < len(_metadata):
            item = _metadata[i]
            context += f"--- Nguồn: {item['metadata']['source']} (Trang {item['metadata']['page']}) ---\n"
            context += f"{item['text']}\n\n"
            
            # Lưu lại thông tin để hiển thị PDF sau này
            source_documents.append({
                "file_name": item['metadata']['source'],
                "page": item['metadata']['page']
            })

    return context.strip(), source_documents

async def retrieve_context_from_image(image_description: str):
    # Trả về context từ mô tả hình ảnh
    context, _ = retrieve_context(image_description)
    return context