# Manual demonstration checklist

**All tests should use synthetic, non-patient data.**

- [ ] Python `py -3.11 --version` is 3.11.x.
- [ ] `python -m pytest -q` passes and `python -m scripts.doctor` shows intended status.
- [ ] App starts with `python -m streamlit run app.py` in Chrome or Edge.
- [ ] Home page has a holographic heart visual, designer sidebar, glass cards and light/dark theme toggle.
- [ ] User registration requires consent, 10+ character password, unique email and username.
- [ ] Login rejects wrong passwords, accepts valid user login.
- [ ] Admin login only accepts `Mr. Doc` and the original private password.
- [ ] Medical chat works in English with local `llama3.2:latest`.
- [ ] Switch to Hindi and ask a medical question; response should be Hindi (model language quality may vary).
- [ ] Test an emergency question: app must immediately display emergency guidance without waiting for model inference.
- [ ] `docs/sample_report.pdf` shows extracted values, correctly flags synthetically high LDL and low Vitamin D, and offers AI explanation when Ollama runs.
- [ ] Inspect AI explanation; do not assume every AI statement is medically correct.
- [ ] Download report text and English PDF summary.
- [ ] Allow microphone and record a short question; local speech-to-text works after initial Whisper model download.
- [ ] Browser read-aloud button speaks; Hindi voice depends on your system's installed voice support.
- [ ] User cannot open another user's reports.
- [ ] Admin can access users, report text and conversations, with read action appearing in audit log.
- [ ] Admin cannot see user passwords.
- [ ] User can delete a conversation, a report and their own account.
- [ ] GitHub `.gitignore` excludes `.env`, local SQLite DB and real report files.

**Scope:** Local educational demo only. No certification, clinical validation or public web deployment is claimed.

## Refinement v1.1 manual validation (local Windows)

- [ ] Dashboard uses holographic heart/orbit, professional sidebar, login tabs, responsive cards and light theme.
- [ ] Sign in as user; ask an English question with Short and Detailed responses. Verify the actual Ollama response.
- [ ] Switch to हिंदी; verify explanations are in readable Devanagari. Local Llama 3.2 may still be imperfect.
- [ ] Upload `docs/sample_report.pdf`; verify extracted test values against the original PDF and status-count cards.
- [ ] Upload another fictional report with the same test/units to check repeated-test chart; avoid comparing different units.
- [ ] Record a short sample in Hindi and English, check auto-detect, edit the transcript, then ask Ollama.
- [ ] Click Play/Stop and change speed; Hindi speech depends on locally installed browser voices.
- [ ] Log in as Mr. Doc; verify report and conversation listings show only metadata before pressing Open.
- [ ] Open a fictional report/conversation, then check Audit Log for recorded access.
- [ ] Change an account's active status and verify it is reflected in the admin dashboard.
- [ ] Run `python -m pytest -q` and `python -m scripts.doctor`.
- [ ] Verify `.env`, `instance/`, database files, medical uploads and local Whisper models are **not** staged with Git.
