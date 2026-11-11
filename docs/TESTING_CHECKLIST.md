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

## v1.8 — manual security and locale checks

- [ ] Admin conversation: wrong/blank password denies the read.
- [ ] Admin conversation: correct password opens exactly the requested record, with an audit entry.
- [ ] Admin report and user profile: same current-password check before private fields are shown.
- [ ] After rerun/navigation, a previous successful read is not retained on the screen.
- [ ] Registered user cannot invoke an admin open using even the real admin password.
- [ ] Hindi/Marathi/Spanish: every authored UI label on all pages is translated.
- [ ] Japanese/French/Chinese and other added languages: first switch prepares full local pack; no false success while incomplete.
- [ ] Changing language updates admin, reports, chat, voice, history, and About; user data and source medical values are not silently modified.
- [ ] Instance/locales, .env, database and Git remain unchanged during patch installation.

### v1.9 dashboard visual checks
- [ ] All four quick-access cards have equal height and width at desktop sizes.
- [ ] All four Open buttons have matching dimensions and a shared horizontal baseline.
- [ ] Icon boxes, titles and descriptions have consistent interior spacing.
- [ ] Buttons open Chat, Reports, Voice and Insights respectively.
- [ ] Switch to Hindi/Spanish and check longer titles and descriptions still fit.
- [ ] In light theme, text and buttons remain readable; in dark theme, 3D glow remains subtle.
- [ ] On narrow/mobile windows, card content stays readable and buttons stay reachable.
- [ ] About Project cards and user/admin data remain unchanged.

## v2.0 manual offline and privacy checks

- [ ] Stop internet/Wi-Fi **after** Ollama model and Whisper downloads; verify AI chat is local.
- [ ] Ask about vitamin D and cholesterol; ensure offline source titles appear and no source is invented.
- [ ] Check that text appears progressively during a normal Ollama chat answer.
- [ ] Compare two sample reports with the same test and unit; verify changes and the CSV locally.
- [ ] Compare reports with different units, duplicate same-test rows or missing values; app must not guess.
- [ ] With OCR disabled, PNG/JPG upload must be rejected; enable only after installing local OCR.
- [ ] Verify the Offline Readiness page with Ollama stopped and running, and in Hindi / another selected locale.
- [ ] Admin must re-enter correct password to create encrypted backup. Wrong password is denied.
- [ ] Encrypted `.hiaenc` must not show plaintext patient data. Restore to NEW filename and validate records.
- [ ] Confirm `instance/healthcare.db`, `.env`, `.git`, registered users and saved history were not modified by patch.
- [ ] Confirm language packs/voice playback for the target language are usable **with Wi-Fi off**.
