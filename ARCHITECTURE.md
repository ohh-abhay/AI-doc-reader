# DocuMind Architecture

## Online query path

1. User enters a question in Streamlit.
2. Sentence Transformer converts the question into an embedding.
3. FAISS performs cosine-style inner-product similarity search.
4. Top-K chunks are selected.
5. Retrieved chunks are labeled with file and page metadata.
6. The LLM receives the question plus retrieved context.
7. The application displays the grounded answer and source cards.

## Offline ingestion path

1. User uploads one or more PDFs.
2. PyMuPDF extracts text page-by-page.
3. Text is normalized and split into overlapping chunks.
4. Sentence Transformer generates normalized vectors.
5. FAISS builds an in-memory vector index.
6. Page/file metadata remains attached to each chunk.
