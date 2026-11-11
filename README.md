# Healthcare Info Assistant 🩺

**Your Intelligent Healthcare Information Companion** — a four-language (English, Hindi, Marathi, Spanish), local-Ollama-powered medical education app built with Python 3.11 and Streamlit. Includes a futuristic 3D-inspired glass dashboard, secure user authentication, permanent administrator, medical questions, PDF lab report analysis, voice input, spoken responses, saved history and health charts.

> **Important:** This is a local **educational demonstration**, not a diagnostic tool, medical device, doctor, prescription service or production patient portal. Llama 3.2 3B can make mistakes and cannot independently verify its medical claims. **Never rely on the app for emergency care, diagnoses or medication decisions.** Seek licensed medical advice. Use fictional data for public demos.

## 1. What is included

- **Two user access options** — user login and user signup, plus a dedicated **permanent administrator login**.
- **Permanent admin:** Username **`Mr. Doc`**, securely initialized once; **no public admin registration**. Account cannot be disabled by the UI.
- **User permissions:** Each user sees only their own report and conversation history. Passwords are **Argon2-hashed**, not retrievable by the administrator.
- **Administrator console:** Manage user account states and view registered profiles, stored report extraction/analysis and conversation histories, with audit logging when opening private content.
- **Medical assistant:** English/Hindi/Marathi/Spanish medical and plain-language explanations, symptoms/causes, general dietary information, foods to consider/limit, and when to seek care.
- **Report PDF intelligence:** Extracts digitally generated PDF text, parses recognizable tests, compares numeric values **only against printed reference ranges**, explains results via Ollama, and stores extracted content/summaries.
- **Voice:** Streamlit microphone → local multilingual Faster-Whisper speech-to-text → Ollama → browser text-to-speech. Voice model is downloaded once on first use.
- **History, insights, account profile and deletion, PDF/TXT summary downloads** (PDF export in English UI, UTF-8 TXT for non-English languages), light/dark toggle.
- **Futuristic interface:** Holographic 3D-rendered heart illustration, depth-styled cards, glowing visual effects, pulsing orb, designer sidebar, gradient glass layouts, responsive sizing.
- **No Gemini API keys, no paid model credits.** Ollama is the default and only medical explanation engine.

## 2. Minimum prerequisites

- Windows 10/11 with **Python 3.11.x** and `py -3.11` working.
- **VS Code** (recommended).
- **Ollama** installed and running, with `llama3.2:latest` (3B) already pulled.
- Internet for the **first Python dependency installation** and the **one-time Whisper model download**; Ollama and speech recognition subsequently work offline.
- Browser: current Chrome, Edge or Firefox. Browser spoken answers require a compatible local speech voice, especially for Hindi.
- Suggested hardware: 8 GB RAM and an RTX 2050 4 GB GPU can work for Llama 3.2 3B, though performance depends on system load. Faster-Whisper is set to CPU/int8 to avoid CUDA configuration. Close memory-heavy apps when running both.

## 3. Windows setup — copy/paste commands from the beginning

### Step A: Extract ZIP

If downloaded to `Downloads`, open **PowerShell** and run:

```powershell
cd $HOME\Downloads
Expand-Archive -LiteralPath '.\Healthcare-Info-Assistant.zip' -DestinationPath "$HOME\Documents" -Force
cd "$HOME\Documents\Healthcare-Info-Assistant"
code .
```

If the ZIP is in a different folder, adjust its path. The archive includes the full `Healthcare-Info-Assistant` folder.

### Step B: Create Python 3.11 environment and install dependencies

Open the **VS Code Terminal → PowerShell** inside the project folder:

```powershell
py -3.11 --version
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell prevents activation, you can avoid changing your security policy and run all commands through `\.venv\Scripts\python.exe` instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The project also provides `setup_windows.ps1`, `run_windows.ps1` and `test_windows.ps1` for convenience.

### Step C: Initialize the permanent admin securely

```powershell
Copy-Item .env.example .env
notepad .env
```

In `.env`, **set your own strong password** (at least 12 characters, letters and digits):

```text
ADMIN_INITIAL_PASSWORD=CHOOSE_YOUR_OWN_LONG_PASSWORD_123
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:latest
WHISPER_MODEL=base
```

The example string above **must not** be reused as a real password. Save the file, then:

```powershell
python -m scripts.init_admin
```

You should see `Admin setup: created` or `ready`. The initial password is hashed and saved in `instance/healthcare.db`. **Immediately delete the `ADMIN_INITIAL_PASSWORD=...` value from `.env`**, leaving it empty. The admin remains in the database. Changing this environment variable later **does not reset the account**. Keep an encrypted backup of your admin password — no plaintext recovery feature is supplied.

**Admin username:** `Mr. Doc` (exactly, including space and dot). On the landing page choose **Admin Login** in the designed sidebar.

### Step D: Check Ollama

```powershell
ollama --version
ollama list
ollama run llama3.2:latest
```

If you see a chat response, type `/bye` to exit. Ollama usually runs automatically on Windows. If the server is not running, open the **Ollama application** or start it in another terminal:

```powershell
ollama serve
```

If `ollama list` does not show the model, download it once:

```powershell
ollama pull llama3.2:latest
```

You **do not** need a Gemini API key. Ollama serves a local endpoint at `http://127.0.0.1:11434`.

### Step E: Run tests and launch

```powershell
python -m pytest -q
python -m streamlit run app.py
```

Open the displayed local URL (usually `http://127.0.0.1:8501`). **Create a user account** from the `Create User Account` tab, or log in as the separately initialized admin.

### Optional: One-command scripts

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_windows.ps1
powershell -ExecutionPolicy Bypass -File .\test_windows.ps1
powershell -ExecutionPolicy Bypass -File .\run_windows.ps1
```

They do not create a password for you; admin initialization requires manually editing `.env`.

## 4. Quick demonstration

1. Register a fictional user with a valid email format, choose English, Hindi, Marathi or Spanish, and read/accept the explicit notice of administrator access to stored health content.
2. Ask the assistant: **"What is Vitamin D deficiency? Define it medically and in simple words, and what foods help?"**
3. Switch the sidebar to `हिंदी` and ask **"कोलेस्ट्रॉल बढ़ने पर किन चीज़ों को कम खाना चाहिए?"**
4. Open **Report Analyzer**, upload `docs/sample_report.pdf`, and click Analyze. The sample is **synthetic data** and includes clearly indicated ranges.
5. Open **Voice Assistant**, allow microphone access, record a short question and click **Ask Ollama**. For local Whisper, the first attempt downloads the `base` model through an internet connection. Click **Read aloud** to hear your answer (language support depends on browser/OS voices).
6. View user history, download a report summary, and open Health Insights.
7. Sign out; in the **Admin Login** tab sign in as `Mr. Doc`. Inspect user profiles, open a stored report or conversation, and confirm the **Audit Log** records sensitive access.

## 5. Optional scanned-PDF OCR

Most text PDFs work without anything else. For scanned/image-only PDFs:

1. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) on Windows and confirm its local executable location.
2. Run `python -m pip install -r requirements-ocr.txt`.
3. Set `ENABLE_OCR=true` and optionally `TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe` in `.env`.
4. Restart Streamlit.

OCR is best-effort and presently configured for **English** lab-report text. It is not validated for handwritten content, damaged scans or uncommon layouts; lab values still require manual verification. No OCR cloud service is used.

## 6. New PUBLIC GitHub repository, first push from zero

**GitHub username:** `Nobelesse`  
**New repository name:** `Healthcare-Info-Assistant`  
**Intended URL:** `https://github.com/Nobelesse/Healthcare-Info-Assistant`

The repo **does not exist automatically** just because you downloaded this ZIP. First go to [GitHub's new repository page](https://github.com/new), sign in as `Nobelesse`, make the repository **Public**, and create it **without initializing a README, .gitignore or license** (this ZIP already includes these).

From your project root in VS Code PowerShell:

```powershell
git --version
git init
git branch -M main
git status
# Check your secrets and data are ignored (expected: .env, instance/healthcare.db)
git check-ignore .env
# If you already have a local DB, the next command should show its ignored path:
git check-ignore instance/healthcare.db
# Configure your Git identity if this computer has not done so:
git config --global user.name "Your GitHub Display Name"
git config --global user.email "your-github-email@example.com"
git add .
git status
git commit -m "Initial commit - Healthcare Info Assistant"
git remote add origin https://github.com/Nobelesse/Healthcare-Info-Assistant.git
git remote -v
git push -u origin main
```

If the GitHub repo has already been created with starter commits, do not blindly force-push — resolve the remote history first. GitHub may ask you to sign in using your browser or a credential manager. For later changes:

```powershell
git status
git add .
git commit -m "Improve Healthcare Info Assistant"
git push origin main
```

The `.gitignore` excludes `.env`, local SQLite databases, patient reports, credentials, audio and generated runtime caches. Always inspect `git status` before pushing. Public GitHub repositories should contain **only source code and fictitious example reports**, never real medical records or credentials.

## 7. Future small PATCH ZIP workflow

Updates can be distributed as smaller ZIPs containing only changed files. When you request one, you can include which feature changed and the patch will list expected files and commands. Basic workflow:

```powershell
# Run from project root after backing up the project and local DB.
Copy-Item -Path .\instance\healthcare.db -Destination .\healthcare-backup-local.db -ErrorAction SilentlyContinue
# Put your specific patch ZIP here and review its contents BEFORE overwriting:
Expand-Archive -LiteralPath '.\Healthcare-Patch-001.zip' -DestinationPath '.\_patch_review' -Force
# Copy only approved application files from the reviewed folder, not .env or instance.
# e.g. Copy-Item '.\_patch_review\pages\user_views.py' '.\pages\user_views.py' -Force
python -m pytest -q
python -m streamlit run app.py
git status
git add .
git commit -m "Apply Healthcare Info Assistant patch 001"
git push origin main
```

The backup file in the snippet is deliberately ignored by `.gitignore` (extension `.db`). Do not overwrite `instance/healthcare.db` unless an explicit database migration is included.

## 8. Troubleshooting

| Problem | What to try |
|---|---|
| `'py' is not recognized` | Install Python 3.11 and the Python Launcher, then restart VS Code. |
| PowerShell activation blocked | Use `.\.venv\Scripts\python.exe -m ...` without activating. |
| `ModuleNotFoundError` | Activate `.venv`, then rerun `python -m pip install -r requirements.txt`. |
| Ollama offline | Start Ollama and run `ollama list`; verify `OLLAMA_BASE_URL` and `OLLAMA_MODEL`. |
| AI out-of-memory or slow | Close large programs; use `ollama pull llama3.2:1b`, then set `OLLAMA_MODEL=llama3.2:1b` in `.env`. The 1B model is less capable. |
| Voice recording doesn't work | Grant microphone permission, use `http://127.0.0.1:8501` locally, and use an up-to-date browser. |
| Faster-Whisper first use fails | Connect to the internet once to download the speech model; then retry. |
| Hindi read-aloud is not pronounced properly | Install a Hindi voice in Windows/browser speech settings; browser voice support varies. |
| Scanned PDF unreadable | Install Tesseract + optional OCR dependencies (section 5). |
| Admin not initialized | Edit `.env`, run `python -m scripts.init_admin`, and then clear its initial-password entry. |
| Can't view the app remotely | It is intentionally bound to `127.0.0.1` for local privacy. It is not internet-deployed. |

## 9. Project structure

```text
Healthcare-Info-Assistant/
├── app.py                       # entrypoint, login, sidebar, page routing
├── auth/service.py              # signup, login, Argon2, admin bootstrap
├── config/settings.py           # .env-based configuration
├── database/models.py           # SQLAlchemy tables
├── database/store.py            # privacy-scoped persistence + audit logs
├── views/user_views.py          # dashboards, chat, reports, voice, history, settings
├── views/admin_views.py         # admin directory, reports, conversations, audit
├── views/about_view.py          # about this project, not academic details
├── services/ollama_service.py   # local chat and report explanations
├── services/report_service.py   # PDF extraction and lab comparisons
├── services/voice_service.py    # local Faster-Whisper
├── services/export_service.py   # PDF summary generation
├── ui/components.py             # 3D-inspired visual components + browser speech
├── ui/strings.py                # English/Hindi/Marathi/Spanish interface labels
├── assets/heart.webp            # original holographic heart visual
├── assets/style.css             # custom visual theme
├── docs/sample_report.pdf       # synthetic demo document
├── scripts/init_admin.py        # one-time permanent admin setup
├── tests/                       # automated unit / integration tests
├── .streamlit/config.toml       # local server and dark theme
├── requirements.txt
├── requirements-ocr.txt
├── .env.example
├── .gitignore
├── setup_windows.ps1
├── run_windows.ps1
└── test_windows.ps1
```

## 10. Privacy and safety — important limitations

- Medical histories and user details are **stored locally in an unencrypted SQLite database**. Even with app-level account control, anyone with physical/file-system access to the computer or a backup may read this database. Use only sample/synthetic records for public demos.
- The permanent admin is intended to have broad access, including stored health data. Users receive notice and must consent at signup. Authorized app views are logged, but this is not a substitute for a full enterprise security/compliance program.
- Original uploaded PDFs are **not retained**; text/parsed values/AI summaries are retained until deleted. Conversation content is retained in SQLite. Data does not go to Gemini; Ollama is on your device. The Whisper model is downloaded from a third-party model host once.
- **No email verification or forgotten-password flow**, multi-factor authentication, encrypted database, rate-limiting for public networks, hardened session middleware, medical validation, regulatory certification, or multi-user web deployment is included. This is intentionally a **local demonstration**, not ready for public Internet or handling real patient data.
- Lab-report regex extraction is deliberately conservative but can still misread columns, labels or unit notation. A high/low label is an automatic comparison **only with the range found on the same text line**, not a clinical interpretation. The patient and clinician must confirm every value, unit and reference range.
- AI responses may be fabricated or incomplete and dietary suggestions can conflict with personal allergies, prescriptions or conditions. This app must never suggest medication dosage or encourage ignoring emergencies.
- A rendered 3D-style heart asset and CSS depth/animation create the visual appearance; the heart is **not a freely rotatable medical 3D anatomy viewer**. Graphics are decorative only.

## 11. External documentation

- [Streamlit documentation](https://docs.streamlit.io/)
- [Ollama model library](https://ollama.com/library/llama3.2)
- [Ollama REST API](https://docs.ollama.com/api)
- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [MedlinePlus](https://medlineplus.gov/), [WHO](https://www.who.int/health-topics), [NHS](https://www.nhs.uk/conditions/)

---

**Healthcare Info Assistant** — an educational project for understanding health information, with transparent privacy boundaries and a local-first AI workflow.

## Refinement v1.1 — 11 November 2026

This optional patch keeps the original SQLite schema and `instance/healthcare.db` unchanged.

- **Design:** extra 3D-inspired CSS orbit/depth layers, glowing navigation, a dashboard journey guide, refined responsive layouts.
- **AI:** selectable short/standard/detailed medical answers and optional vegetarian dietary suggestions; clearer Hindi prompting and explicit Ollama error messages. Medical advice remains educational and may be wrong.
- **Reports:** supports additional *recognizable names* (eGFR, CRP, uric acid, etc.), status-count cards, and repeated-measurement charts limited to the same units. Automated reading remains heuristic and must be checked against the original PDF.
- **Voice:** automatic language detection option, editable transcription before sending, browser audio playback with speed and stop controls. Speech quality depends on installed OS/browser voices; medical names may transcribe incorrectly.
- **Admin:** metadata-only private-record listings, per-record explicit consent checks, atomic audit logging for report/conversation opens, profile viewing audit, account-status chart and audit log filters. These controls are designed for a **local demo only**, not production handling of patient medical records.
- **Maintenance:** replaced deprecated `fitz` imports with `pymupdf`, replaced `use_container_width` with `width="stretch"`, and added regression tests.

For the patch-only installation and backup instructions, see the ZIP's `PATCH_README.md`.


## Refinement v1.2 — streamlined navigation and clinical color system

- **Blank page fix:** Internal implementation files moved from Streamlit's special `pages/` directory to `views/`. The Streamlit auto-generated `app`, `user views`, `admin views`, and `about view` sidebar entries are no longer shown. `app.py` alone handles authenticated, role-scoped navigation.
- **Guest access:** A newly organized sidebar separates **User Portal** (Login, Registration), **Admin Portal** (permanent Mr. Doc login), and **Project** (About). Login forms appear beside the hero instead of three page-level tabs.
- **Section labels:** Each navigation group has a concise description and a dividing line. The logged-in user and admin menus are also grouped by purpose.
- **Accessible bilingual controls:** Navigation, access forms, and consent notice display English or Hindi according to the selected language.
- **Professional healthcare palette:** Calmer deep-navy, clinical teal, soft mint and muted blue palette with accessible input contrasts, refined light mode and restrained 3D glass effects.
- **No migration required:** Database schema, patient records, administrator login, voice, Ollama and report services have not been changed.

This patch deliberately moves code files and deletes the obsolete `pages/*.py` entrypoints. Always apply it using the bundled patch installer; simply copying new files without removing `pages/*.py` will leave the unwanted default navigation. Existing `.env`, `.venv`, databases and Git settings are not modified.


## Refinement v1.3 — multilingual UI, premium sidebar, and clinical light theme

- **Fixed language controls:** Four fully curated application UI language choices: **English / हिन्दी / मराठी / Español**. Language choice is made using radio buttons; users cannot type in an unsupported language. Preferences are stored per user and applied to relevant AI prompts, report summaries and speech-recognition selections.
- **Localized interface:** Landing, registration, user dashboard, medical chat, report analyzer, result statuses, history, profile and account deletion, administrator, About, warnings, and voice playback labels are translated into each listed language. The **Healthcare Info Assistant** project name and technical brand/model names are intentionally kept unchanged. Uploaded report text, original test names, usernames, earlier saved responses and browser-native controls are not automatically translated.
- **More premium sidebar:** Increased spacing between Portal, Project, Dashboard and Preferences groups; elegant deep-teal navigation, distinct active actions, teal dividers and gentle depth effects in both themes.
- **Readable light theme:** Fixed dark text on dark hero and dark sidebar conflicts; using an always-dark teal navigation panel, a dark hero with white headings, and fresh pale clinic-inspired cards and forms. Charts use dynamic dark/light text colors.
- **No database migration:** Existing accounts, admin password, conversations and reports remain as they are. The patch installer backs up modified code files and never touches `.env`, `.git`, `.venv`, or `instance/`.

**Localization boundaries:** The app authors all visible interface labels in four languages, but browser-provided widget chrome may use the browser's locale, medical laboratory terms may remain in the report's original language, and Llama 3.2 3B does not guarantee fluent medically accurate content in every language. For medical decisions, consult a licensed clinician. Hindi PDF export is not bundled; use the UTF-8 `.txt` export for non-English summaries.

Run `python -m pytest -q` after applying the patch, then restart with `python -m streamlit run app.py`.


## v1.4 refinement — Healing Pearl UI and expanded language picker

- New pale mint / pearl / soft blue light mode, high-contrast hero, and refined clinical-teal sidebar.
- Heart illustration now has an animated double-beat pulse with reduced-motion support.
- Language is selected from a **fixed dropdown**; users cannot add arbitrary languages.
- Four complete curated interface catalogs: English, हिन्दी, मराठी and Español.
- Ten **preview languages** (curated main navigation, forms, emergencies and other common labels):
  Français, Deutsch, 日本語, 简体中文, Português, Русский, العربية, বাংলা, தமிழ், తెలుగు.
- Important: preview languages fall back to English for any UI label not yet translated.
  To locally translate remaining static app-authored text using your Ollama model, run
  `python -m scripts.translate_ui --languages fr de ja zh` (or any selected preview codes)
  **once**; this can take considerable time on an 8 GB laptop, is not guaranteed
  to be perfect, and may require proofreading. It never sends patient data or
  passwords. Local translations are saved to `instance/locale_overrides.json`.
  Restart Streamlit after generating a pack. Browser-generated controls, historical
  AI answers, uploaded reports and names are not automatically translated.
- Voice transcription and speech output for newly added languages depend on the
  local recognition model and installed browser/system voices.


### Refinement v1.5 (session chat, auto voice, and visual placement)

- The animated heart is positioned higher and farther to the right, with a
  contrast veil behind text, so medical guidance remains readable.
- Once a microphone recording is finished, local Whisper transcription is sent
  automatically to Ollama. There is no mandatory **Ask Ollama** click. A manual
  correction option appears only if you edit the recognized text (or AI fails).
  One recording is processed at most once automatically; record a new clip to retry.
- Browser speech playback options are now **1×, 1.25× (default), 1.5×**.
  Actual perceived speed varies across browser voices and languages.
- Active AI chat is private to the current login session and **starts empty**
  after sign-out/sign-in. Prior conversations remain in **My History** for the
  same user. Refreshing the tab also clears active chat because Streamlit
  sessions are browser-connection scoped; records remain available in History.
- The patch installer does not alter the local SQLite database, `.env`, Git
  history, saved reports, or administrator credentials.


## v1.6 refinement: multilingual answer re-display and voice fidelity

- The animated heart and orbit are kept within the hero card on typical desktop widths.
- A language change translates **already displayed** chat answers via local Ollama and caches the result only in the signed-in Streamlit session. The saved original in SQLite remains untouched. Translation may take additional time on Llama 3.2 3B; it is not clinically verified. If Ollama is unavailable, the original is shown with a warning, and wrong-language speech playback is disabled.
- Existing saved report summaries and the currently selected history answer are translated on display as well. New reports remember their source language for the current login, avoiding needless retranslation. Open history sparingly on low-power laptops because many long answers can require multiple local translation requests.
- Voice recognition now explicitly uses Whisper's `task='transcribe'`, preserving the language rather than translating it to English. Automatic language detection steers the **initial reply** to the spoken language, even if the interface is set differently. Once the user explicitly changes the language dropdown, the existing voice reply is translated to the newly selected language.
- A larger futuristic SVG microphone icon replaces the small emoji on the Voice Assistant page. Playback requires a compatible voice installed in the browser/operating system. Missing voices are reported rather than reading Hindi with an English voice.
- This update does not change the database structure, user accounts, saved patient data, or credentials.
