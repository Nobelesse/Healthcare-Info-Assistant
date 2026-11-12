"""Resume stubborn Healthcare Info Assistant interface translations locally.

Safe to stop and rerun. Preserves all existing valid translations and does not
change app.py, users, credentials, saved reports, or Ollama model files.
Requires the project's existing ``scripts.translate_ui`` implementation.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys

import httpx

from config.settings import OLLAMA_BASE_URL, OLLAMA_MODEL
from scripts import translate_ui as catalog
from ui.strings import C, LANGUAGES
from ui.extra_languages import EXTRA_TEXT


FIXED = ("Healthcare Info Assistant", "Mr. Doc", "Ollama")
TOKEN = re.compile(r"\{[a-zA-Z_][a-zA-Z0-9_]*(?:![rsa])?(?::[^{}]+)?\}")


def backup_once():
    path = catalog.CACHE
    if not path.is_file():
        return None
    backup = path.with_name("locale_overrides.before_recovery.json")
    if not backup.exists():
        shutil.copy2(path, backup)
    return backup


def candidate_text(raw: str, key: str) -> str:
    raw = (raw or "").strip()
    raw = re.sub(r"^```(?:json|text)?\s*|\s*```$", "", raw, flags=re.IGNORECASE).strip()
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, str):
            return parsed.strip()
        if isinstance(parsed, dict):
            for pick in ("translation", "translated", "text", "value", key):
                if isinstance(parsed.get(pick), str):
                    return parsed[pick].strip()
            values = [v for v in parsed.values() if isinstance(v, str)]
            if len(values) == 1:
                return values[0].strip()
    except (ValueError, TypeError):
        pass
    raw = re.sub(r"^(?:translation|translated text|answer)\s*:\s*", "", raw, flags=re.I)
    return raw.strip().strip('"').strip()


def lock_tokens(source: str):
    names = list(FIXED) + [token.group() for token in TOKEN.finditer(source)]
    names = list(dict.fromkeys(t for t in names if t in source))
    locked = source
    substitutions = {}
    for index, value in enumerate(names):
        marker = f"ZXQ{index}QXZ"
        locked = locked.replace(value, marker)
        substitutions[marker] = value
    return locked, substitutions


def restore_tokens(translation: str, substitutions: dict[str, str]):
    result = translation
    for marker, value in substitutions.items():
        result = re.sub(re.escape(marker), lambda _: value, result, flags=re.I)
    return result


def local_response(prompt: str, timeout: float, *, as_json: bool = False, length: int = 100):
    num_predict = min(1500, max(220, int(length * 2.7)))
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "10m",
        "options": {"temperature": 0.05, "num_ctx": 4096, "num_predict": num_predict},
    }
    if as_json:
        payload["format"] = "json"
    result = httpx.post(
        f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate",
        json=payload,
        timeout=httpx.Timeout(timeout, connect=8.0),
    )
    result.raise_for_status()
    return result.json().get("response", "")


def prompt_for(source: str, language: str, *, json_mode: bool, guarded: bool):
    instruction = (
        f"Translate this healthcare app interface message from English into "
        f"{LANGUAGES[language]} (language code {language}). "
        "Preserve its exact meaning, including medical cautions, consent, and warnings. "
        "Keep unchanged all product names (Healthcare Info Assistant, Mr. Doc, Ollama), "
        "literal placeholders in curly braces, technical identifiers, URLs, "
        "Markdown and commands. Do not add any explanation or extra content. "
    )
    if guarded:
        instruction += "Protected markers like ZXQ0QXZ MUST remain exactly as typed. "
    if json_mode:
        instruction += 'Return ONLY a JSON object such as {"translation":"translated message"}. '
    else:
        instruction += "Return ONLY the translated text, without quotation marks or a heading. "
    return instruction + "\nEnglish message:\n" + source


def repair_one(code: str, key: str, timeout: float, tries: int):
    source = C[key][0]
    guarded_source, substitutions = lock_tokens(source)
    strategies = [(source, True, False), (source, False, False),
                  (guarded_source, False, True)]
    attempts = strategies[:tries]
    reasons = []
    for prompt_source, json_mode, guarded in attempts:
        prompt = prompt_for(prompt_source, code, json_mode=json_mode, guarded=guarded)
        try:
            raw = local_response(prompt, timeout, as_json=json_mode, length=len(source))
            translation = candidate_text(raw, key)
            if guarded:
                translation = restore_tokens(translation, substitutions)
            if catalog.valid_translation(source, translation):
                return translation, None
            reasons.append("output rejected (missing token, unchanged, or invalid format)")
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            reasons.append(f"{type(exc).__name__}: {str(exc)[:110]}")
    return None, reasons[-1] if reasons else "no valid output"


def main():
    parser = argparse.ArgumentParser(
        description="Repair missing local UI translations one label at a time"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true")
    group.add_argument("--languages", nargs="+", metavar="CODE")
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--tries", type=int, default=3, choices=(1, 2, 3))
    parser.add_argument("--max-labels", type=int, default=0, help="Limit repairs per language; 0 = all")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.timeout < 10 or args.max_labels < 0:
        parser.error("Timeout must be >= 10; max-labels must be >= 0")
    targets = list(EXTRA_TEXT) if args.all else args.languages
    if any(code not in EXTRA_TEXT for code in targets):
        parser.error("Supported language codes: " + ", ".join(EXTRA_TEXT))

    if not args.dry_run:
        try:
            probe = httpx.get(f"{OLLAMA_BASE_URL.rstrip('/')}/api/tags", timeout=6)
            probe.raise_for_status()
            models = {model.get("name") for model in probe.json().get("models", [])}
            if models and OLLAMA_MODEL not in models:
                print(f"Required model {OLLAMA_MODEL!r} was not found in Ollama. Installed: {', '.join(sorted(models))}")
                return 3
        except (httpx.HTTPError, ValueError) as exc:
            print(f"Local Ollama is unavailable: {exc}")
            print("Start Ollama and rerun this command. Existing translations are safe.")
            return 3
        before = backup_once()
        if before:
            print(f"Original translation cache backed up once: {before}", flush=True)
        print(f"Ollama model: {OLLAMA_MODEL} | Local endpoint: {OLLAMA_BASE_URL}", flush=True)
    all_failures = {}
    for code in targets:
        remaining = catalog.remaining_keys(code)
        print(f"{LANGUAGES[code]}: {len(remaining)} missing of {len(C)}", flush=True)
        if args.dry_run or not remaining:
            continue
        chosen = remaining[:args.max_labels] if args.max_labels else remaining
        failed = []
        for number, key in enumerate(chosen, 1):
            try:
                result, error = repair_one(code, key, args.timeout, args.tries)
            except KeyboardInterrupt:
                print("\nStopped by user; completed labels remain saved.", flush=True)
                return 130
            if result is not None:
                cache = catalog.load_cache()
                cache.setdefault(code, {})[key] = result
                catalog.save_cache(cache)
                print(f"  [{number}/{len(chosen)}] saved {key}", flush=True)
            else:
                failed.append(key)
                print(f"  [{number}/{len(chosen)}] skipped {key}: {error}", flush=True)
        pending = catalog.remaining_keys(code)
        print(f"  {len(C)-len(pending)}/{len(C)} complete, {len(pending)} remaining", flush=True)
        if failed:
            all_failures[code] = failed

    print("\nFinal status:", flush=True)
    pending_total = 0
    for code in targets:
        pending = catalog.remaining_keys(code)
        pending_total += len(pending)
        print(f"  {code}: {len(pending)} missing", flush=True)
    if args.dry_run:
        return 0
    if pending_total:
        print("Some labels still require review; existing translations were kept.", flush=True)
        return 2
    print("All selected language packs complete. Restart Streamlit.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
