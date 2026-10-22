# 📚 DocuMind — AI-Powered Document Intelligence & RAG Assistant

**Chat with your PDFs. Find relevant information. Get AI-generated answers grounded in your documents.**

DocuMind is a Python-based document intelligence application that uses **Retrieval-Augmented Generation (RAG)** to help users search and ask questions about PDF documents through an interactive Streamlit interface.

Instead of relying only on an AI model's general knowledge, DocuMind retrieves relevant passages from uploaded documents and uses that information to generate contextual answers with source references.

## ✨ Key Features

- 📄 **Multiple PDF Uploads** — Upload multiple PDF documents in one session.
- 🔍 **Semantic Search** — Retrieve relevant passages based on the meaning of a question.
- 🧠 **AI-Powered Question Answering** — Generate natural-language answers using an LLM.
- 📑 **Source References** — View source document names, page numbers, and relevant text previews.
- 💬 **Conversational Interface** — Ask follow-up questions through a chat interface.
- 🧩 **Text Chunking** — Split lengthy documents into smaller, searchable sections.
- 🔢 **Vector Similarity Search** — Use FAISS to find semantically similar document passages.
- ⚙️ **Configurable Retrieval** — Adjust the number of passages retrieved for a question.
- 🌡️ **Temperature Control** — Adjust the model's response-generation settings.
- 🔐 **API Key Input** — Enter an API key through the application's sidebar.
- ☁️ **Deployment-Friendly Structure** — Run locally or configure the application for a supported Streamlit hosting environment.

## 🛠️ Technology Stack

| Category | Technology | Purpose |
|---|---|---|
| Programming Language | Python | Application logic and RAG pipeline |
| Frontend | Streamlit | Interactive web interface |
| PDF Processing | PyMuPDF | Extract text and page information from PDFs |
| Embeddings | Sentence Transformers | Convert text into numerical vectors |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` | Generate semantic text embeddings |
| Vector Search | FAISS | Retrieve similar document passages |
| Generative AI | Gemini API through an OpenAI-compatible client | Generate answers from retrieved context |
| AI Architecture | Retrieval-Augmented Generation (RAG) | Ground answers in uploaded documents |
| Configuration | Python configuration and environment variables | Manage model and retrieval settings |
| Version Control | Git and GitHub | Track and manage project code |

## 🧠 How DocuMind Works

DocuMind follows a Retrieval-Augmented Generation workflow.

### Document processing pipeline

1. **Upload:** The user uploads one or more PDF files.
2. **Text extraction:** PyMuPDF extracts text and page information from the PDFs.
3. **Chunking:** The extracted text is divided into smaller, overlapping sections.
4. **Embedding generation:** Sentence Transformers converts the text chunks into numerical vectors.
5. **Indexing:** FAISS indexes the vectors for similarity search.
6. **Question processing:** The user's question is converted into an embedding.
7. **Retrieval:** FAISS identifies the most relevant passages.
8. **Answer generation:** The retrieved context and question are sent to the configured language model.
9. **Source display:** The interface displays the answer alongside available source document and page references.

### System architecture

```text
              USER
                |
                v
        Streamlit Interface
                |
                v
        Upload PDF Documents
                |
                v
          PyMuPDF
        Text Extraction
                |
                v
        Text Chunking
                |
                v
       Sentence Transformers
        Embedding Generation
                |
                v
          FAISS Index
                |
                |
    User Question ---> Query Embedding
                |             |
                +------v------+
                |
                v
       Similarity Retrieval
                |
                v
       Relevant Text Chunks
                |
                v
       Gemini Language Model
                |
                v
       Contextual AI Answer
                |
                v
       Answer + Source References
```

## 📂 Project Structure

```text
AI-doc-reader/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── ARCHITECTURE.md
├── LICENSE
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion.py
│   ├── vector_store.py
│   ├── llm.py
│   └── rag.py
│
└── tests/
    └── test_ingestion.py
```

### Main files and their responsibilities

- **`app.py`** — Runs the Streamlit application, accepts PDF uploads, displays the chat interface, and presents source references.
- **`src/ingestion.py`** — Extracts text and metadata from uploaded PDFs.
- **`src/vector_store.py`** — Handles text chunking, embeddings, vector indexing, and similarity retrieval.
- **`src/llm.py`** — Communicates with the configured language model and generates context-grounded responses.
- **`src/rag.py`** — Coordinates retrieval, context preparation, and answer generation.
- **`src/config.py`** — Defines model settings, chunking parameters, retrieval settings, and other configuration values.
- **`requirements.txt`** — Lists Python dependencies.
- **`.env.example`** — Provides a template for environment-based configuration.
- **`ARCHITECTURE.md`** — Documents the application's architecture.
- **`tests/`** — Contains automated tests for supported functionality.

## 🚀 Getting Started

Follow these steps to run DocuMind on your local computer.

### Prerequisites

Install the following before starting:

- Python 3.12
- Git
- Visual Studio Code (recommended)
- An API key for the configured language model

### 1. Clone the repository

Open your terminal and run:

```bash
git clone https://github.com/ohh-abhay/AI-doc-reader.git
```

Navigate into the project folder:

```bash
cd AI-doc-reader
```

### 2. Create a virtual environment

For Windows using Conda:

```bash
conda create -p venv python=3.12 -y
conda activate .\venv
```

If you use a regular Python installation instead, you can create a virtual environment with:

```bash
python -m venv .venv
```

Activate it in Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 3. Install the dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the project's dependencies:

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

The application requires a valid API key for AI answer generation.

For the Gemini-compatible implementation, obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

You can enter the key in the application's sidebar. Never publish the key in your source code or commit it to GitHub.

If you prefer environment-based configuration, copy the template:

**Windows Command Prompt:**

```bat
copy .env.example .env
```

Then edit `.env` and configure the key variable expected by your current application code. Keep `.env` private and ensure it is excluded from version control.

### 5. Run the application

From the project root, run:

```bash
streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser.

## 💻 How to Use DocuMind

1. Launch the application.
2. Upload one or more text-based PDF documents from the sidebar.
3. Wait for document processing and indexing to finish.
4. Enter your language-model API key if it is not already configured.
5. Type a question about the uploaded documents.
6. Read the generated answer.
7. Expand the **Sources** section to inspect the retrieved document passages and page references.
8. Ask follow-up questions to explore the documents further.

### Example questions

- What is the main purpose of this document?
- Summarize the most important points.
- What are the eligibility requirements?
- Which page discusses the termination policy?
- What are the key findings of this report?
- Compare the information presented in these documents.
- Is the answer to my question available in the uploaded documents?

The quality of the response depends on the extracted text, retrieved passages, and language model.

## ⚙️ Configuration

DocuMind supports configuration of several RAG parameters.

| Parameter | Purpose |
|---|---|
| `LLM_MODEL` | Selects the language model |
| `EMBEDDING_MODEL` | Selects the embedding model |
| `TOP_K` | Controls how many relevant passages are retrieved |
| `TEMPERATURE` | Controls variation in generated responses |
| `CHUNK_SIZE` | Sets the approximate text chunk size |
| `CHUNK_OVERLAP` | Sets the overlap between consecutive chunks |

The default embedding model is `sentence-transformers/all-MiniLM-L6-v2`.

The chunking, retrieval, and generation settings can be adjusted to experiment with different RAG configurations. Environment-variable names and API-key configuration should match the current implementation.

## 🎯 Why RAG?

A conventional language model may answer using its pretrained knowledge, which can lead to unsupported responses about a particular document.

RAG improves document question answering by retrieving relevant text before generating an answer.

**Benefits of this approach:**

- Uses document-specific context to answer questions.
- Helps reduce unsupported or fabricated information.
- Makes it easier to trace answers to relevant source passages.
- Supports semantic retrieval rather than depending only on exact keyword matches.
- Allows the language model to work with information supplied at query time.

RAG reduces hallucination risk but does not eliminate it completely. Retrieved context and generated answers should still be checked.

## 🔒 Security and Privacy

- Never commit API keys, passwords, or private configuration files.
- Use environment variables or the application's password-style API key field.
- Restrict access to deployed applications that process confidential documents.
- Understand that retrieved document text is sent to the configured language-model provider for answer generation.
- Avoid uploading sensitive or confidential files unless the deployment and provider settings are appropriate for that data.

The current application is intended as an educational and portfolio project, not a complete enterprise document-security platform.

## ⚠️ Current Limitations

- The current interface accepts PDF files.
- Scanned PDFs without extractable text may require an OCR pipeline.
- Retrieval quality depends on document extraction, chunking, embeddings, and the selected retrieval count.
- Language-model requests require network access and a valid API key.
- External model providers may experience rate limits or temporary service interruptions.
- The in-memory vector index may need to be rebuilt when the application session restarts.
- Answers can still be incomplete or inaccurate despite context-grounding instructions.

## 🔮 Future Improvements

Potential extensions include:

- OCR support for scanned documents.
- DOCX, TXT, and additional document formats.
- Persistent vector storage.
- Hybrid keyword and semantic retrieval.
- Reranking for more relevant search results.
- RAG evaluation using a benchmark question set.
- Improved page-level citations and answer-grounding checks.
- Streaming responses and enhanced error recovery.
- User authentication and separate document workspaces.
- Automated testing and continuous integration.

## 🎓 Learning Outcomes

This project demonstrates practical application of:

- Python application development.
- Natural Language Processing (NLP).
- Generative AI and Large Language Models (LLMs).
- Retrieval-Augmented Generation (RAG).
- Semantic search and vector embeddings.
- PDF text extraction and document preprocessing.
- Vector similarity search using FAISS.
- Prompt engineering and context-grounded generation.
- Streamlit application development.
- API integration and environment-based configuration.
- Git and GitHub project management.

## 📌 Project Summary

**DocuMind — AI-Powered Document Intelligence & RAG Assistant** is an AI application that combines PDF processing, semantic embeddings, vector similarity search, and language-model generation to answer questions about uploaded documents through a web interface.

The project demonstrates how retrieval and generation can be combined to build a practical document question-answering system.

## 👨‍💻 Author

**Abhay**

GitHub: [@ohh-abhay](https://github.com/ohh-abhay)

Project repository: [AI-doc-reader](https://github.com/ohh-abhay/AI-doc-reader)

---

*Built as an AI/ML learning and portfolio project.*
