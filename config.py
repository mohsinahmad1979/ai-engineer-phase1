import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def get_gemini_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing GEMINI_API_KEY in the environment or .env file")
    return api_key


def get_chroma_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(str(BASE_DIR / ".chromadb"))


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-3.6-flash"
gemini_client = None
chroma_client = None

__all__ = [
    "BASE_DIR",
    "GEMINI_API_KEY",
    "MODEL_NAME",
    "gemini_client",
    "chroma_client",
    "get_gemini_api_key",
    "get_chroma_client",
]
