import os
import streamlit as st
from pathlib import Path

from src.config import get_settings
from src.ingestion import ingest_pdfs
from src.rag import RAGEngine

st.set_page_config(
    page_title="DocuMind — RAG Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {font-size: 2.35rem; font-weight: 750; margin-bottom: 0.1rem;}
    .sub-header {color: #6b7280; font-size: 1.02rem; margin-bottom: 1.4rem;}
    .source-card {padding: 0.8rem 1rem; border: 1px solid rgba(128,128,128,.25);
                  border-radius: .7rem; margin-bottom: .6rem;}
    .metric-card {padding: .9rem; border-radius: .7rem; background: rgba(128,128,128,.08);}
</style>
""", unsafe_allow_html=True)

settings = get_settings()

if "rag" not in st.session_state:
    st.session_state.rag = RAGEngine(settings)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "doc_signature" not in st.session_state:
    st.session_state.doc_signature = None

rag = st.session_state.rag

with st.sidebar:
    st.title("📚 DocuMind")
    st.caption("AI-Powered Document Intelligence & RAG Assistant")
    st.divider()

    st.subheader("1. Add documents")
    uploaded = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more text-based PDFs.",
    )

    if uploaded:
        signature = tuple((f.name, len(f.getvalue())) for f in uploaded)
        if signature != st.session_state.doc_signature:
            with st.status("Indexing documents…", expanded=True) as status:
                try:
                    docs = ingest_pdfs(uploaded)
                    stats = rag.build_index(docs)
                    st.session_state.doc_signature = signature
                    st.session_state.messages = []
                    status.update(label="Documents indexed", state="complete")
                    st.success(
                        f"Indexed {stats['documents']} document(s) into "
                        f"{stats['chunks']} searchable chunks."
                    )
                except Exception as exc:
                    status.update(label="Indexing failed", state="error")
                    st.error(str(exc))

    st.divider()
    st.subheader("Settings")
    top_k = st.slider("Retrieved passages", 2, 8, settings.top_k)
    temperature = st.slider("Answer temperature", 0.0, 1.0, settings.temperature, 0.05)
    rag.top_k = top_k
    rag.temperature = temperature

    st.divider()
    st.subheader("OpenAI API key")
    rag.api_key = st.text_input(
        "Enter your API key",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
        help="Used only for this app session. It is not displayed or saved to a file.",
    ).strip()
    if rag.api_key:
        st.caption("API key entered for this session.")
    else:
        st.warning("Enter an OpenAI API key to enable answer generation.")

    st.divider()
    st.subheader("Project status")
    if rag.is_ready:
        st.success("Knowledge base ready")
        st.metric("Indexed chunks", rag.chunk_count)
    else:
        st.info("Upload a PDF to begin.")

    st.caption("Privacy note: documents are processed in this app session. "
               "Only retrieved text is sent to the configured LLM provider.")

st.markdown('<div class="main-header">📚 DocuMind</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Ask questions across your documents using '
    'Retrieval-Augmented Generation with grounded source citations.</div>',
    unsafe_allow_html=True,
)

if not rag.is_ready:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 📄 Upload")
        st.write("Add one or more PDF documents.")
    with c2:
        st.markdown("### 🔎 Retrieve")
        st.write("Find semantically relevant passages.")
    with c3:
        st.markdown("### 💬 Ask")
        st.write("Get grounded answers with page references.")
    st.info("Start by uploading a PDF from the sidebar.")
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("Sources"):
                    for source in message["sources"]:
                        st.markdown(
                            f'<div class="source-card"><b>{source["file"]}</b> — '
                            f'Page {source["page"]}<br>{source["preview"]}</div>',
                            unsafe_allow_html=True,
                        )

    prompt = st.chat_input("Ask a question about your documents…")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if not rag.api_key:
                st.error(
                    "Enter your OpenAI API key in the sidebar, then submit your "
                    "question again. Do not share your key in chat."
                )
            else:
                with st.status("Searching documents and generating answer…", expanded=False):
                    result = rag.answer(prompt, st.session_state.messages[:-1])

                st.markdown(result["answer"])
                st.caption(
                    f"Retrieved {len(result['sources'])} relevant passage(s) • "
                    f"Model: {settings.llm_model}"
                )

                with st.expander("Sources"):
                    for source in result["sources"]:
                        st.markdown(
                            f'<div class="source-card"><b>{source["file"]}</b> — '
                            f'Page {source["page"]}<br>{source["preview"]}</div>',
                            unsafe_allow_html=True,
                        )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                })
