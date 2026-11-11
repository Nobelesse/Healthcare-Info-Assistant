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


def main():
    parser = argparse.ArgumentParser(description='Translate remaining UI labels using local Ollama')
    parser.add_argument('--languages', nargs='+', required=True, help='e.g. fr de ja zh')
    parser.add_argument('--batch-size', type=int, default=7, choices=range(3, 11), metavar='3-10')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    for code in args.languages:
        if code not in EXTRA_TEXT:
            parser.error(f'No additional-language pack for {code!r}. Try: {", ".join(EXTRA_TEXT)}')
    cache = load_cache()
    for code in args.languages:
        existing = cache.setdefault(code, {})
        missing = [key for key in C if key not in EXTRA_TEXT[code] and key not in existing]
        print(f'{LANGUAGES[code]}: {len(missing)} untranslated labels; {len(C)} total')
        if args.dry_run:
            continue
        count = 0
        for index in range(0, len(missing), args.batch_size):
            batch = missing[index:index + args.batch_size]
            try:
                updates = translate_batch(code, batch)
            except (httpx.HTTPError, ValueError) as exc:
                print(f'Cannot translate this batch: {type(exc).__name__}. Remaining labels fall back to English.')
                print('Check Ollama with: ollama list')
                break
            existing.update(updates)
            count += len(updates)
            save_cache(cache)  # partial progress survives interruption
            print(f'  {min(index + args.batch_size,len(missing))}/{len(missing)} processed; '
                  f'{count} valid new translations', flush=True)
        print('Saved local pack to:', CACHE)
    print('Restart Streamlit to load the updated language pack.')


if __name__ == '__main__':
    main()
