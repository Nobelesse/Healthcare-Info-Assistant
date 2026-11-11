"""Whisper speech-to-text; preserve detected input language, never force translation."""
import os
import tempfile
from functools import lru_cache
from config.settings import WHISPER_MODEL


class VoiceError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _whisper_model():
    from faster_whisper import WhisperModel
    # CPU int8 avoids CUDA requirements on Windows RTX 2050 systems.
    return WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")


def transcribe_audio_with_language(audio_bytes: bytes, language: str | None = None) -> tuple[str, str | None]:
    """Return verbatim recognized speech and the auto-detected ISO language code.

    Whisper's task='transcribe' is important: task='translate' would turn Hindi
    speech into English instead of preserving the original language/script.
    """
    if not audio_bytes or len(audio_bytes) > 8 * 1024 * 1024:
        raise VoiceError('Recording is empty or larger than 8 MB.')
    path = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            path = tmp.name
            tmp.write(audio_bytes)
        model = _whisper_model()
        segments, info = model.transcribe(
            path, beam_size=3, language=language, task='transcribe', vad_filter=True
        )
        transcript = ' '.join(s.text.strip() for s in segments).strip()
        if not transcript:
            raise VoiceError('No clear speech detected. Try recording closer to the microphone.')
        detected = getattr(info, 'language', None)
        return transcript[:1800], (detected or language)
    except VoiceError:
        raise
    except Exception as exc:
        raise VoiceError('Local speech recognition is unavailable. The first use needs internet to download the Whisper model; check the setup guide and retry.') from exc
    finally:
        if path and os.path.exists(path):
            os.remove(path)


def transcribe_audio(audio_bytes: bytes, language: str | None = None) -> str:
    """Backward-compatible text-only API for existing callers."""
    return transcribe_audio_with_language(audio_bytes, language)[0]
