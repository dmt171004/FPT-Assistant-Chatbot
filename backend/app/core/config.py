import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in .env")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

RAG_DATA_DIR = os.path.join(BASE_DIR, "rag", "data")
RAG_CHUNKS_DIR = os.path.join(BASE_DIR, "rag", "chunks")
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "rag", "vector_store")
PROMPT_DIR = os.path.join(BASE_DIR, "prompts")
