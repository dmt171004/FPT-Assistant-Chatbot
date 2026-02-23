# app/rag/embedder.py
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "intfloat/multilingual-e5-base"

class VectorStore:
    def __init__(self, dim=768):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, texts, metadatas):
        embeddings = self.model.encode(
            ["query: " + t for t in texts],
            normalize_embeddings=True
        )
        self.index.add(np.array(embeddings))
        self.metadata.extend(metadatas)

    def save(self, path):
        faiss.write_index(self.index, f"{path}.index")
        with open(f"{path}.meta", "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self, path):
        self.index = faiss.read_index(f"{path}.index")
        with open(f"{path}.meta", "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query, top_k=4):
        q_emb = self.model.encode(
            ["query: " + query],
            normalize_embeddings=True
        )
        scores, idxs = self.index.search(np.array(q_emb), top_k)

        results = []
        for i in idxs[0]:
            results.append(self.metadata[i])

        return results
