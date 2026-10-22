from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    llm_model: str = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    top_k: int = int(os.getenv("TOP_K", "5"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.2"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))

def get_settings() -> Settings:
    return Settings()
