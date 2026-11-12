# Healthcare Info Assistant v2.0 — Fast offline language switching

This maintenance patch changes **only application code and automated tests**. It does not edit `.env`, `.git`, `.venv`, your administrator credentials, your local SQLite database, saved medical records, or existing `instance/locale_overrides.json`.

## Why switching previously failed

Four existing interface languages (`en`, `hi`, `mr`, `es`) have full built-in translations (324 static labels). The other ten initially contain only 78 curated translations each. Previously selecting a missing pack caused a long, synchronous Ollama request inside Streamlit, sometimes failing and leaving the previous language visible. A separate `t(..., language=...)` call could also raise `TypeError: ... multiple values for argument 'language'`.

## New behavior

- Selecting a language changes the *selected language* immediately. It never silently restores the previous language.
- When that language is fully prepared, all page labels load instantly from a local dictionary; no translation requests run during normal navigation.
- On **first use** of any optional language, a lightweight preparation page is displayed **in that language**, showing progress and an explicit retry if the local Ollama translator cannot finish. The old-language login page is never displayed as if it were translated.
- Pack preparation runs on one background worker rather than blocking Streamlit event handlers; preparation only sends **built-in UI labels**, never user data, reports, chat history or passwords.
- Completed batches are saved atomically and persist across restarts. Ollama stays warm between small requests, reducing repeated model-loading overhead.
- Switching *between completed language packs* is immediate without Wi-Fi, Ollama inference or any cloud API.

**Important realistic limit:** A complete translation for a language not yet prepared **cannot be instantaneous** on an offline 3B local model. That first preparation may require several minutes or more, depending on the computer/model and the language. Model-generated translations also need human review for safety-critical wording. If Ollama is unavailable, the preparation screen offers a retry; it does not falsely claim that incomplete content is translated.

## Optional: prepare all language packs ahead of time

While Ollama is installed/running, stop the app and run from your project directory:

```powershell
cd "E:\Projects\Healthcare-Info-Assistant"
.\.venv\Scripts\python.exe -m scripts.translate_ui --all --dry-run
.\.venv\Scripts\python.exe -m scripts.translate_ui --all --batch-size 6
```

This can be **time-consuming** on an 8 GB laptop. No Internet is used: the configured local Ollama model translates curated UI strings. If it reports incomplete languages, run the same command again; valid completed items remain saved. Check one language first if preferred:

```powershell
.\.venv\Scripts\python.exe -m scripts.translate_ui --languages ja --batch-size 6
```

Never delete `instance/locale_overrides.json` if you want to keep prepared packs. It is deliberately private and ignored by Git.

## Verification

```powershell
cd "E:\Projects\Healthcare-Info-Assistant"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Try English → Hindi → Marathi → Spanish (instant), then Japanese (localized preparation screen if not previously prepared). After Japanese reaches full coverage, Japanese navigation/login/pages should display correctly; switch away and back to verify the instant cached path.

**Scope:** static application interface translation only. Older stored medical answers may still require separate local Ollama translation on first viewing in a new language. Translation accuracy and real model performance require on-device verification. The application remains educational, not a clinically validated tool.
