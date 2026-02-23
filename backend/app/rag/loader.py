import os
import faiss
import numpy as np
import fitz  # PyMuPDF - Xử lý PDF cực tốt cho tiếng Việt
import json
from openai import OpenAI
from tqdm import tqdm
from app.core.config import (
    OPENAI_API_KEY,
    RAG_DATA_DIR,
    VECTOR_STORE_DIR,
)

client = OpenAI(api_key=OPENAI_API_KEY)
EMBEDDING_MODEL = "text-embedding-3-large"

def load_pdf_files():
    """
    Quét thư mục RAG_DATA_DIR, đọc tất cả file PDF và chia nhỏ theo từng trang.
    Mỗi trang sẽ là một 'document' để dễ dàng dẫn hướng sau này.
    """
    documents = []
    
    if not os.path.exists(RAG_DATA_DIR):
        print(f"❌ Thư mục dữ liệu không tồn tại: {RAG_DATA_DIR}")
        return documents

    for file_name in os.listdir(RAG_DATA_DIR):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(RAG_DATA_DIR, file_name)
            try:
                doc = fitz.open(file_path)
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text = page.get_text("text").strip()
                    
                    if text:  # Chỉ lấy trang có nội dung
                        documents.append({
                            "text": text,
                            "metadata": {
                                "source": file_name,
                                "page": page_num + 1  # Page 1-based index
                            }
                        })
                doc.close()
            except Exception as e:
                print(f"⚠ Lỗi khi đọc file {file_name}: {e}")
                
    return documents

def build_vector_store():
    # 1. Tải toàn bộ dữ liệu PDF
    documents = load_pdf_files()
    if not documents:
        print("⚠ No PDF data found in RAG_DATA_DIR")
        return

    # 2. Xóa dữ liệu cũ (Xóa file index.faiss và metadata cũ nếu có)
    index_path = os.path.join(VECTOR_STORE_DIR, "index.faiss")
    meta_path = os.path.join(VECTOR_STORE_DIR, "metadata.json")
    
    if os.path.exists(index_path):
        os.remove(index_path)
        print("🗑 Đã xóa Vector Store cũ.")

    # 3. Tạo Embeddings
    embeddings = []
    texts_to_embed = [doc["text"] for doc in documents]
    
    print(f"🚀 Đang xử lý {len(texts_to_embed)} trang PDF...")
    
    # Gửi batch lên OpenAI (tối ưu hơn gửi từng câu)
    for i in tqdm(range(0, len(texts_to_embed), 20), desc="Embedding Progress"):
        batch = texts_to_embed[i:i+20]
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=batch
        )
        embeddings.extend([e.embedding for e in response.data])

    # 4. Khởi tạo FAISS và lưu trữ
    embeddings_np = np.array(embeddings).astype("float32")
    dim = embeddings_np.shape[1]
    
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings_np)

    # 5. Lưu xuống đĩa
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    faiss.write_index(index, index_path)

    # Quan trọng: Lưu Metadata dưới dạng JSON thay vì txt để giữ cấu trúc file/trang
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=4)

    print(f"✅ Đã cập nhật Vector Store với {len(documents)} trang từ PDF.")

if __name__ == "__main__":
    build_vector_store()