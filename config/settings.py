"""Local-first project configuration; secrets are never hardcoded."""
from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
INSTANCE_DIR = ROOT / "instance"
DB_PATH = INSTANCE_DIR / "healthcare.db"
ADMIN_USERNAME = "Mr. Doc"
APP_NAME = "Healthcare Info Assistant"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
ADMIN_INITIAL_PASSWORD = os.getenv("ADMIN_INITIAL_PASSWORD", "")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
ENABLE_OCR = os.getenv("ENABLE_OCR", "false").lower() in {"true", "yes", "1"}
TESSERACT_CMD = os.getenv("TESSERACT_CMD", "")
MAX_REPORT_BYTES = 10 * 1024 * 1024
MAX_REPORT_PAGES = 12
MAX_REPORT_CHARS = 14000
MAX_QUESTION_CHARS = 1800


def database_url() -> str:
    return f"sqlite:///{DB_PATH.as_posix()}"
