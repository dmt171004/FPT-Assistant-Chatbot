from parser import load_pdf
from chunker import semantic_chunk
from embedder import VectorStore

PDF_PATH = r"E:\FPT\Chatbot_Module\backend\app\rag\data\HD_THI _EOS.pdf"
INDEX_PATH = "app/rag/data/eos_manual"

docs = load_pdf(PDF_PATH)
chunks = semantic_chunk(docs)

texts = [c["text"] for c in chunks]
metas = [{"text": c["text"], "page": c["page"]} for c in chunks]

store = VectorStore()
store.add(texts, metas)
store.save(INDEX_PATH)

print("✅ RAG index built successfully")
