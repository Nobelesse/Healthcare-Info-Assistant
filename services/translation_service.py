"""Per-login localized display of existing medical answers without altering SQLite.

Translations are computed by the user's local Ollama server only. Original medical
answers are retained verbatim; local translations are cached exclusively in that
Streamlit browser session, and discarded by the existing logout/session reset.
"""
from collections.abc import MutableMapping, Callable
import hashlib
from typing import Any

from services.ollama_service import OllamaUnavailable, translate_answer

CACHE_LIMIT = 60


def display_in_language(
    state: MutableMapping[str, Any], text: str, target_lang: str,
    original_lang: str | None = None, user_id: int | None = None,
    translator: Callable[[str, str], str] = translate_answer,
) -> tuple[str, bool]:
    """Return (display_text, translated_ok), without editing the source record.

    This is deliberately a session-private cache, NOT st.cache_data/global cache:
    medical records or user conversations must not leak between user accounts.
    """
    if not text or (original_lang and original_lang == target_lang):
        return text, True
    scope = user_id if user_id is not None else 'local'
    if state.get('_translation_scope') != scope:
        state['_translation_scope'] = scope
        state['_translation_cache'] = {}
    cache = state.setdefault('_translation_cache', {})
    key = hashlib.sha256((target_lang + '\0' + text).encode('utf-8')).hexdigest()
    if key in cache:
        return cache[key]
    try:
        localized = translator(text, target_lang)
        if not isinstance(localized, str) or not localized.strip():
            raise OllamaUnavailable('Local translator returned an empty translation.')
        result = (localized.strip(), True)
    except (OllamaUnavailable, ValueError):
        # Never represent untranslated English text as a successful Hindi answer.
        result = (text, False)
    if len(cache) >= CACHE_LIMIT:
        cache.pop(next(iter(cache)))
    cache[key] = result
    return result


def preferred_voice_language(selected_lang: str, detected_lang: str | None, autodetect: bool, known_languages) -> str:
    """Prefer the spoken language, not the interface language, for new voice queries."""
    if autodetect and detected_lang:
        code = detected_lang.lower().replace('_', '-').split('-')[0]
        if code in known_languages:
            return code
    return selected_lang


def voice_display_language(selected_lang: str, spoken_lang: str | None,
                           current_revision: int, response_revision: int) -> str:
    """First show spoken-language reply; after explicit locale change use the selection."""
    if current_revision == response_revision and spoken_lang:
        return spoken_lang
    return selected_lang
