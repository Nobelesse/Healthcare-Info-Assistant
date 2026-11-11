"""Read-only offline prerequisites inspection (does not contact the public internet)."""
import importlib.util
import shutil
from pathlib import Path
from urllib.parse import urlparse
from config.settings import OLLAMA_BASE_URL, OLLAMA_MODEL, ENABLE_OCR, TESSERACT_CMD, ROOT, WHISPER_MODEL


def is_loopback_base(url: str) -> bool:
    try:
        parsed=urlparse(url)
        return parsed.scheme in ('http','https') and parsed.hostname in ('127.0.0.1','localhost','::1')
    except ValueError:
        return False


def inspect_offline():
    from services.ollama_service import check_ollama
    local=is_loopback_base(OLLAMA_BASE_URL)
    if local:
        online,msg=check_ollama()
    else:
        online,msg=False,'Ollama URL is not local. Offline operation is not guaranteed.'
    whisper_root=Path.home()/'.cache'/'huggingface'/'hub'
    # Detection is advisory: custom cache directories are also supported.
    whisper_cached=bool(list(whisper_root.glob(f'models--Systran--faster-whisper-{WHISPER_MODEL}*'))) if whisper_root.is_dir() else False
    tesseract=bool(shutil.which('tesseract') or (TESSERACT_CMD and Path(TESSERACT_CMD).is_file()))
    return {
        'ollama_local':local,'ollama_model_ready':online,'ollama_message':msg,
        'whisper_installed':importlib.util.find_spec('faster_whisper') is not None,
        'whisper_cache_detected':whisper_cached,
        'ocr_enabled':ENABLE_OCR,'tesseract_found':tesseract,
        'knowledge_packaged':(ROOT/'data'/'medical_knowledge.json').is_file(),
        'network_apis_required':False,
        'offline_ready_for_text':bool(local and online and (ROOT/'data'/'medical_knowledge.json').is_file()),
    }
