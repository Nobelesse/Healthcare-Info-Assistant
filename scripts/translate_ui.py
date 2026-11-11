"""Build optional additional-language UI packs using only your local Ollama.

For example: python -m scripts.translate_ui --languages fr de ja zh
The tool sends only pre-authored UI labels; never medical records, usernames,
passwords or chat histories. Translations are locally cached under instance/.
This can be slow on an 8 GB RAM laptop. It may also require human proofreading.
"""
import argparse
import json
import os
from pathlib import Path
import string
import tempfile
import httpx

from config.settings import OLLAMA_BASE_URL, OLLAMA_MODEL, ROOT
from ui.extra_languages import EXTRA_TEXT
from ui.strings import C, LANGUAGES

CACHE = ROOT / 'instance' / 'locale_overrides.json'
FORMATTER = string.Formatter()


def placeholders(text):
    try:
        return sorted(name for _, name, _, _ in FORMATTER.parse(text) if name)
    except ValueError:
        return None


def valid_translation(source, output):
    if not isinstance(output, str) or not output.strip() or len(output) > max(180, len(source) * 6):
        return False
    if placeholders(source) != placeholders(output):
        return False
    if len(source) > 28 and output.strip() == source.strip():
        return False  # An unchanged full English sentence is not a translation
    for fixed in ('Healthcare Info Assistant', 'Mr. Doc', 'Ollama'):
        if fixed in source and fixed not in output:
            return False
    return True


def load_cache():
    try:
        cache = json.loads(CACHE.read_text('utf-8'))
    except (OSError, ValueError):
        return {}
    return cache if isinstance(cache, dict) else {}


def save_cache(data):
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=CACHE.parent,
                                     prefix='.locale_', suffix='.json', delete=False) as temp:
        json.dump(data, temp, ensure_ascii=False, indent=2)
        name = temp.name
    os.replace(name, CACHE)


def translate_batch(language, batch, timeout=190):
    input_text = {key: C[key][0] for key in batch}
    prompt = (
        f'You are a UI localization translator. Translate every JSON VALUE from English to '
        f'{LANGUAGES[language]} (locale code {language}). Return ONLY a JSON object with '
        'EXACTLY the original keys and translated string values. Do not translate keys. '
        'Preserve literal format tokens such as {username}, {count}, {pages}, {name}. '
        'Never modify the exact product names Healthcare Info Assistant, Mr. Doc, Ollama, '
        'Streamlit, PDF, SQLite, AI, URLs, shell commands or technical identifiers. '
        'Preserve any Markdown and the meaning of safety disclaimers, especially medical '
        'warnings and user-consent text. Use natural, accessible professional language. '
        'Never add explanations, extra keys, or quotes outside the JSON.\nJSON INPUT:\n'
        + json.dumps(input_text, ensure_ascii=False)
    )
    response = httpx.post(f'{OLLAMA_BASE_URL}/api/generate',
                          json={'model': OLLAMA_MODEL, 'prompt': prompt,
                                'format': 'json', 'stream': False,
                                'options': {'temperature': 0, 'num_ctx': 4096,
                                            'num_predict': 1150}},
                          timeout=httpx.Timeout(timeout, connect=8.0))
    response.raise_for_status()
    raw = response.json().get('response', '').strip()
    try:
        results = json.loads(raw)
    except ValueError:
        return {}
    return {key: item for key, item in results.items()
            if key in input_text and valid_translation(input_text[key], item)} if isinstance(results, dict) else {}


class TranslationPreparationError(RuntimeError):
    """Local model was unavailable or failed to produce a complete safe locale."""


def remaining_keys(code: str, cache: dict | None = None) -> list[str]:
    """Missing source labels for a language, with no user/private data involved."""
    if code not in EXTRA_TEXT:
        return []
    saved = (cache if cache is not None else load_cache()).get(code, {})
    if not isinstance(saved, dict):
        saved = {}
    return [key for key in C if key not in EXTRA_TEXT[code] and
            not valid_translation(C[key][0], saved.get(key))]


def prepare_language_pack(code: str, *, batch_size: int = 6, rounds: int = 3,
                          progress=None) -> tuple[int, int]:
    """Generate ALL missing page labels locally and persist after every batch.

    Returns (translated, total); UI must never claim full language support until
    translated==total. Safe to resume; failed batches do not delete valid progress.
    This code only submits predefined UI strings, no chat/medical/personal data.
    """
    if code not in EXTRA_TEXT:
        if code in {'en','hi','mr','es'}:
            return len(C), len(C)
        raise TranslationPreparationError('Unsupported locale')
    if not 3 <= batch_size <= 10:
        raise ValueError('Batch size must be between 3 and 10')
    data = load_cache()
    existing = data.setdefault(code, {})
    if not isinstance(existing, dict):
        existing = data[code] = {}
    total = len(C)
    complete = total-len(remaining_keys(code, data))
    if progress:
        progress(complete,total)
    for _ in range(max(1,rounds)):
        missing = remaining_keys(code,data)
        if not missing:
            break
        previous_count = len(missing)
        for index in range(0,len(missing),batch_size):
            batch=missing[index:index+batch_size]
            try:
                updates=translate_batch(code,batch)
            except (httpx.HTTPError,ValueError) as exc:
                save_cache(data)
                raise TranslationPreparationError(
                    'Local Ollama is unreachable or failed to translate the UI') from exc
            # Reject hallucinated JSON or partial batches; only validated keys persist.
            if updates:
                existing.update(updates)
                save_cache(data)
            complete=total-len(remaining_keys(code,data))
            if progress:
                progress(complete,total)
        if len(remaining_keys(code,data)) >= previous_count:
            # Model repeatedly skipped/failed all remaining keys. Do not loop forever.
            break
    return total-len(remaining_keys(code,data)), total


def main():
    parser = argparse.ArgumentParser(description='Build full offline UI language packs using Ollama')
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--languages', nargs='+', help='e.g. fr de ja zh')
    group.add_argument('--all', action='store_true', help='All 10 optional languages (can take a long time)')
    parser.add_argument('--batch-size', type=int, default=6, choices=range(3,11), metavar='3-10')
    parser.add_argument('--dry-run', action='store_true')
    args=parser.parse_args()
    targets=list(EXTRA_TEXT) if args.all else args.languages
    for code in targets:
        if code not in EXTRA_TEXT:
            parser.error(f'No optional language pack for {code!r}. Try: {", ".join(EXTRA_TEXT)}')
    errors=[]
    for code in targets:
        pending=remaining_keys(code)
        print(f'{LANGUAGES[code]}: {len(pending)} untranslated labels; {len(C)} total',flush=True)
        if args.dry_run or not pending:
            continue
        try:
            done,total=prepare_language_pack(code,batch_size=args.batch_size,
                                              progress=lambda c,t: print(f'  {c}/{t} localized',flush=True))
        except TranslationPreparationError as exc:
            errors.append(code)
            print(f'  Failed: {exc}. Progress saved; rerun to resume.',flush=True)
            continue
        print(f'  {done}/{total} localized. '+('Complete!' if done==total else 'Incomplete, rerun to retry.'),flush=True)
        if done!=total: errors.append(code)
    print('Local packs are stored under instance/locale_overrides.json. Restart Streamlit.')
    if errors:
        raise SystemExit('Incomplete packs: '+', '.join(errors))


if __name__ == '__main__':
    main()
