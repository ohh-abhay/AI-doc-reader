# DocuMind — AI-Powered Document Intelligence & RAG Assistant

DocuMind is a professional Retrieval-Augmented Generation (RAG) application that lets users upload PDF documents, semantically search their content, and ask grounded questions with source/page references.

## Features

- Multi-PDF ingestion
- PDF text extraction with PyMuPDF
- Configurable text chunking with overlap
- Local semantic embeddings using Sentence Transformers
- FAISS vector similarity search
- Top-K retrieval
- LLM-generated answers grounded in retrieved context
- Source and page citations
- Conversational chat history
- Streamlit web UI
- Environment-based configuration
- Unit tests
- Deployment-ready project structure

## Architecture

```text
PDFs
  │
  ▼
PyMuPDF
  │
  ▼
Text + Page Metadata
  │
  ▼
Chunking
  │
  ▼
Sentence Transformers
  │
  ▼
FAISS Vector Index
  │
  ├─────────────── User Question
  │                       │
  │                       ▼
  │                  Query Embedding
  │                       │
  └──────────────► Similarity Search
                          │
                          ▼
                    Top-K Context
                          │
                          ▼
                    OpenAI LLM
                          │
                          ▼
                 Grounded Answer
                          │
                          ▼
                  Sources / Pages
```

## Project structure

```text
DocuMind_RAG_Assistant/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── .streamlit/
│   └── config.toml
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion.py
│   ├── vector_store.py
│   ├── llm.py
│   └── rag.py
└── tests/
    └── test_ingestion.py
```

## Setup — Windows / Conda

```powershell
conda create -p .venv python=3.12 -y
conda activate .\.venv
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks Conda activation, run:

```powershell
conda init powershell
```

then restart VS Code/PowerShell.

## Configure the API key

You can enter your OpenAI API key in the app's sidebar under **OpenAI API key**.
It is kept only in the current app session and is not saved to a file.

Alternatively, copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

Then edit `.env` and add your API key:

```text
OPENAI_API_KEY=your_real_key
```

Never commit `.env` to GitHub.

## Run

```powershell
streamlit run app.py
```

Open the local URL shown by Streamlit, upload a PDF, and ask a question.

## Test

```powershell
pytest -q
```

## Example questions

- What is the main purpose of this document?
- What are the key requirements?
- What is the leave policy?
- Summarize the section on eligibility.
- Which page discusses termination?
- What information is missing from the document?

## Engineering notes

### Why local embeddings?

Embeddings are generated locally with Sentence Transformers. This keeps the retrieval layer independent of the LLM provider and avoids sending every document chunk to an embedding API.

### Why FAISS?

FAISS provides fast local vector similarity search and is simple to demonstrate in an internship project.

### Why RAG?

RAG grounds generation in retrieved document passages instead of relying only on the model's pretrained knowledge. The application explicitly instructs the model not to invent information outside the supplied context.

## Limitations

- The current version expects text-based PDFs.
- Scanned/image-only PDFs need OCR.
- FAISS is in-memory, so the index is rebuilt when the app session is restarted.
- The application is intended as a portfolio/educational project, not a production secure document-management system.

## Future improvements

- OCR with Tesseract
- DOCX/PPTX support
- Persistent vector database such as Qdrant/Chroma
- Hybrid keyword + semantic retrieval
- Reranking
- RAG evaluation with a benchmark dataset
- LangSmith tracing/observability
- Authentication and user workspaces
- Background ingestion jobs
- Docker deployment
- Streaming model responses

## Resume project description

**AI-Powered Document Intelligence & RAG Assistant** — Developed a Python-based RAG application that processes PDF documents, generates semantic embeddings with Sentence Transformers, indexes content in FAISS, retrieves relevant passages, and generates grounded LLM responses with source/page citations through a Streamlit interface.

## Technology stack

Python · NLP · Generative AI · LLMs · RAG · Semantic Search · Embeddings · Sentence Transformers · FAISS · PyMuPDF · Prompt Engineering · Streamlit · OpenAI API · Git/GitHub
