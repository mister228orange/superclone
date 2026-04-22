import os
from pathlib import Path
from typing import Optional

class Config:
    # Ollama model to use (default: llama3)
    OLLAMA_MODEL: str = os.getenv("SUPERCLONE_OLLAMA_MODEL", "llama3.1:latest")

    # Maximum file size to include in context (in KB)
    MAX_FILE_SIZE_KB: int = int(os.getenv("SUPERCLONE_MAX_FILE_SIZE_KB", "500"))

    # Maximum context size (characters) before truncation
    MAX_CONTEXT_CHARS: int = int(os.getenv("SUPERCLONE_MAX_CONTEXT_CHARS", "50000"))

    # Ollama host URL (if not using default localhost)
    OLLAMA_HOST: Optional[str] = os.getenv("OLLAMA_HOST")

    # Binary file extensions to skip
    BINARY_EXTENSIONS: set = {
        ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".pdf", ".exe", ".bin",
        ".so", ".dylib", ".dll", ".pyc", ".pyo", ".class", ".zip", ".tar", ".gz",
        ".7z", ".rar", ".mp4", ".avi", ".mov", ".mp3", ".wav", ".flac"
    }

config = Config()
