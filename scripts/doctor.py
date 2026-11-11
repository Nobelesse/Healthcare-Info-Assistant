"""Check local installation without starting Streamlit or touching stored medical records."""
import importlib.util
import platform
import sys
from auth.service import admin_exists
from config.settings import OLLAMA_BASE_URL, OLLAMA_MODEL
from database.store import initialize_database
from services.ollama_service import check_ollama


def main():
    print("Healthcare Info Assistant · Environment checker")
    print("Python:", platform.python_version())
    if sys.version_info[:2] != (3, 11):
        print("WARNING: Target Python version is 3.11.x")
    for mod in ("streamlit", "sqlalchemy", "argon2", "httpx", "pymupdf", "faster_whisper", "pandas", "plotly", "reportlab"):
        print(f"{'OK' if importlib.util.find_spec(mod) else 'MISSING'}: {mod}")
    initialize_database()
    print("Permanent admin:", "initialized" if admin_exists() else "not initialized")
    status, message = check_ollama()
    print("Ollama:", "ONLINE" if status else "NOT READY", message)
    print("No medical data was uploaded or sent to cloud APIs by this checker.")


if __name__ == "__main__":
    main()
