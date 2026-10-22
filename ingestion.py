from dataclasses import dataclass
from io import BytesIO
from typing import Iterable
import fitz

@dataclass
class DocumentChunk:
    text: str
    source: str
    page: int
    chunk_id: str

def _split_text(text: str, chunk_size: int, overlap: int):
    text = " ".join(text.split())
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return chunks

def ingest_pdfs(uploaded_files: Iterable, chunk_size=900, overlap=150):
    chunks = []
    for uploaded in uploaded_files:
        data = uploaded.getvalue()
        pdf = fitz.open(stream=BytesIO(data), filetype="pdf")
        for page_index, page in enumerate(pdf):
            text = page.get_text("text")
            page_chunks = _split_text(text, chunk_size, overlap)
            for local_index, chunk in enumerate(page_chunks):
                chunks.append(
                    DocumentChunk(
                        text=chunk,
                        source=uploaded.name,
                        page=page_index + 1,
                        chunk_id=f"{uploaded.name}:{page_index+1}:{local_index}",
                    )
                )
        pdf.close()

    if not chunks:
        raise ValueError(
            "No readable text was found. This version expects text-based PDFs. "
            "OCR support can be added for scanned PDFs."
        )
    return chunks
