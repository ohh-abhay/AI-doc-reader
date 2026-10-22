from src.ingestion import DocumentChunk
from src.vector_store import VectorStore
from src.llm import LLMClient

class RAGEngine:
    def __init__(self, settings):
        self.settings = settings
        self.top_k = settings.top_k
        self.temperature = settings.temperature
        self.vector_store = VectorStore(settings.embedding_model)
        self.llm = None
        self.api_key = None
        self._llm_api_key = None
        self.is_ready = False
        self.chunk_count = 0

    def build_index(self, chunks: list[DocumentChunk]):
        self.vector_store.build(chunks)
        self.chunk_count = len(chunks)
        self.is_ready = True
        return {
            "documents": len(set(c.source for c in chunks)),
            "chunks": len(chunks),
        }

    def _format_context(self, retrieved):
        blocks = []
        sources = []
        for i, (score, item) in enumerate(retrieved, start=1):
            blocks.append(
                f"[Source {i}] File: {item.source}; Page: {item.page}\n"
                f"{item.text}"
            )
            sources.append({
                "file": item.source,
                "page": item.page,
                "score": round(score, 4),
                "preview": item.text[:320] + ("…" if len(item.text) > 320 else ""),
            })
        return "\n\n".join(blocks), sources

    def answer(self, question, history=None):
        if not self.is_ready:
            raise RuntimeError("Upload and index a document first.")

        retrieved = self.vector_store.search(question, self.top_k)
        if not retrieved:
            return {"answer": "I could not find relevant information.", "sources": []}

        context, sources = self._format_context(retrieved)
        api_key = self.api_key or None
        if self.llm is None or self._llm_api_key != api_key:
            self.llm = LLMClient(
                self.settings.llm_model,
                self.temperature,
                api_key=api_key,
            )
            self._llm_api_key = api_key

        answer = self.llm.generate(question, context, history=history)
        return {"answer": answer, "sources": sources}
