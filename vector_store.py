from typing import List
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.items = []

    def build(self, items):
        texts = [item.text for item in items]
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)
        self.items = list(items)

    def search(self, query: str, top_k: int = 5):
        if self.index is None or not self.items:
            return []
        vector = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")
        scores, indices = self.index.search(vector, min(top_k, len(self.items)))
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            item = self.items[int(idx)]
            results.append((float(score), item))
        return results
