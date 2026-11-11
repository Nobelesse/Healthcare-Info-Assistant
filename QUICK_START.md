# QUICK START — Healthcare Info Assistant

This folder is a **complete application**, not a partial phase. For the full beginner guide, see `README.md`.

## Step 1. Open in VS Code

Extract `Healthcare-Info-Assistant.zip` and open the **Healthcare-Info-Assistant** folder in VS Code.

## Step 2. Setup Python 3.11 (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

## Step 3. Setup permanent admin

Edit `.env` and set `ADMIN_INITIAL_PASSWORD` to your own strong 12+ character password containing letters and numbers, then run:

```powershell
python -m scripts.init_admin
```

After success, REMOVE the initial password from `.env` and save. Your admin username is exactly **Mr. Doc**; it persists in the local database.

## Step 4. Ollama

```powershell
ollama list
ollama run llama3.2:latest
```

Type `/bye` to exit Ollama chat. If necessary, start the Ollama desktop application first. No Gemini API key needed.

## Step 5. Tests and start

```powershell
python -m pytest -q
python -m streamlit run app.py
```

Create a user with **Signup**, or sign in with permanent **Admin Login**. Try the fictional `docs/sample_report.pdf` file.

## GitHub first push

First create a **new empty PUBLIC repo** called `Healthcare-Info-Assistant` in `Nobelesse` on GitHub, with no starter README, then:

```powershell
git init
git branch -M main
git add .
git status
git commit -m "Initial commit - Healthcare Info Assistant"
git remote add origin https://github.com/Nobelesse/Healthcare-Info-Assistant.git
git push -u origin main
```

**Never push `.env`, `instance/`, real medical reports, or local databases.** The `.gitignore` already excludes them. Verify before pushing. Details, patch updates, OCR, microphone setup, privacy and troubleshooting: `README.md`.
