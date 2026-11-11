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
