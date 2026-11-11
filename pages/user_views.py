"""User dashboards, AI questions, reports, voice, insights, history and account management."""
from collections import Counter
from datetime import datetime
import hashlib
import io
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from auth.service import AuthError, change_password, confirm_password
from config.settings import MAX_REPORT_BYTES
from database import store
from services.ollama_service import medical_answer, report_answer, emergency_notice, OllamaUnavailable, check_ollama
from services.report_service import extract_pdf, analyze_labs, ReportError, clean_filename
from services.voice_service import transcribe_audio, VoiceError
from services.export_service import make_english_pdf
from ui.components import hero, section, metric, feature_card, advisory, speech_button
from ui.strings import t


def when(value):
    return value.strftime("%d %b %Y · %I:%M %p") if isinstance(value, datetime) else "—"


def ai_status():
    @st.cache_data(ttl=18, show_spinner=False)
    def _status():
        return check_ollama()
    return _status()


def _navigate(page):
    st.session_state.page = page
    st.rerun()


def dashboard(user, lang):
    hero(user["full_name"].split()[0], lang)
    st.write("")
    numbers = store.counts(user["id"])
    cols = st.columns(4)
    stats = [("Medical conversations" if lang == "en" else "स्वास्थ्य बातचीत", numbers["questions"], "💬", "rgba(20,199,232,.19)"),
             ("Reports analyzed" if lang == "en" else "रिपोर्ट विश्लेषण", numbers["reports"], "📄", "rgba(185,119,243,.17)"),
             ("Voice questions" if lang == "en" else "आवाज़ से सवाल", numbers["voice"], "🎙", "rgba(41,226,165,.15)"),
             ("Local AI" if lang == "en" else "स्थानीय AI", "3.2", "✧", "rgba(250,185,81,.16)")]
    for col, item in zip(cols, stats):
        with col:
            metric(*item)
    st.write("")
    section("Everything you need, in one place" if lang == "en" else "आपके स्वास्थ्य की जानकारी एक ही जगह",
            "Start a conversation, understand a lab report or ask with your voice." if lang == "en" else
            "सवाल पूछें, लैब रिपोर्ट समझें या आवाज़ से बात करें।", overline="YOUR HEALTHSPACE")
    cards = [
        ("AI Health Assistant" if lang == "en" else "AI स्वास्थ्य सहायक", "Explore diseases, deficiencies and practical nutrition guidance." if lang == "en" else "बीमारियों, कमियों और खानपान की जानकारी पाएँ।", "🧠", "chat"),
        ("Report Analyzer" if lang == "en" else "रिपोर्ट विश्लेषण", "Understand lab results with careful range comparisons." if lang == "en" else "लैब जांच का मतलब आसान भाषा में समझें।", "📋", "reports"),
        ("Voice Assistant" if lang == "en" else "वॉइस सहायक", "Speak naturally; get an answer you can listen to." if lang == "en" else "बोलकर सवाल पूछें और जवाब सुनें।", "🎙️", "voice"),
        ("Health Insights" if lang == "en" else "स्वास्थ्य जानकारी", "See trends across your stored report findings." if lang == "en" else "अपनी रिपोर्ट का सार देखें।", "📊", "insights"),
    ]
    cols = st.columns(4)
    for col, (title, desc, icon, target) in zip(cols, cards):
        with col:
            feature_card(title, desc, icon)
            if st.button("Open ↗" if lang == "en" else "खोलें ↗", key="quick_" + target, use_container_width=True):
                _navigate(target)
    st.write("")
    ok, label = ai_status()
    if ok:
        st.success(f"🟢 {label}")
    else:
        st.warning(f"🟠 {label}")
    advisory(lang)


def chat(user, lang):
    section(t("chat", lang),
            "Ask about medical conditions, symptoms, deficiencies, diet and general wellness." if lang == "en" else
            "बीमारी, लक्षण, विटामिन की कमी, भोजन या स्वास्थ्य से जुड़ा सवाल पूछें।", "AI MEDICAL CHAT")
    advisory(lang)
    history = list(reversed(store.list_interactions(user["id"], limit=30)))
    medical_history = [x for x in history if x["kind"] in {"medical", "voice"}]
    if not medical_history:
        st.info("Try: 'What is Vitamin B12 deficiency?' • 'PCOS के लक्षण क्या हैं?' • 'Foods to limit with high LDL cholesterol?' ")
    for item in medical_history[-12:]:
        with st.chat_message("user", avatar="👤"):
            st.markdown(item["question"])
        with st.chat_message("assistant", avatar="🩺"):
            st.markdown(item["response"])
    last = medical_history[-1] if medical_history else None
    if last:
        speech_button(last["response"], lang, key="chat_tts")
    prompt = st.chat_input("Ask anything about health..." if lang == "en" else "स्वास्थ्य से जुड़ा सवाल लिखें...")
    if prompt:
        urgent = emergency_notice(prompt, lang)
        if urgent:
            # Emergency symptoms: show actionable guidance immediately instead of waiting for a model.
            store.save_interaction(user["id"], prompt, urgent)
            st.error(urgent)
            st.stop()
        try:
            with st.spinner("Asking local AI / Ollama..." if lang == "en" else "स्थानीय AI से जवाब लिया जा रहा है..."):
                response = medical_answer(prompt, lang, medical_history)
            store.save_interaction(user["id"], prompt, response)
            st.rerun()
        except (OllamaUnavailable, ValueError) as exc:
            st.error(str(exc))
    st.caption("AI-generated health education can contain errors. Seek licensed medical advice for diagnosis and treatment.")


def _labs_dataframe(labs):
    if not labs:
        st.info("No reliably structured lab value/reference pairs detected. The AI can still explain the text, but numeric findings must be verified manually.")
        return
    df = pd.DataFrame(labs)[["name", "value", "unit", "reference", "status"]]
    df.columns = ["Test", "Result", "Unit", "Report range", "Range comparison"]
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.caption("Values/ranges are extracted heuristically. Verify every measurement against the original PDF before acting on it.")


def _report_export(report, lang, prefix="my"):
    text_data = f"Healthcare Info Assistant\nReport: {report['filename']}\n\n{report['ai_summary']}\n\nEducational only; verify against the original PDF."
    st.download_button("⬇ Download summary (.txt)" if lang == "en" else "⬇ सारांश (.txt) डाउनलोड करें",
                       text_data.encode("utf-8"), f"{prefix}_report_{report['id']}.txt", mime="text/plain", key=f"txt_{prefix}_{report['id']}")
    if lang == "en":
        pdf = make_english_pdf(report["filename"], report["ai_summary"])
        st.download_button("⬇ Download PDF summary", pdf, f"{prefix}_report_{report['id']}.pdf",
                           mime="application/pdf", key=f"pdf_{prefix}_{report['id']}")
    else:
        st.caption("Hindi Unicode is preserved in the UTF-8 text download; PDF export is available in English mode.")


def report_analyzer(user, lang):
    section(t("reports", lang), "Upload your lab report and understand reported values, reference ranges and possible next steps." if lang == "en" else
            "अपनी लैब रिपोर्ट अपलोड करें और जांच के नतीजों का अर्थ जानें।", "DOCUMENT INTELLIGENCE")
    advisory(lang)
    st.markdown('''<div class="glass-panel"><b>📄 SMART DOCUMENT SCAN</b><p style="color:#93bbc7;font-size:13px">Text PDFs · Maximum 10 MB · Up to 12 pages · No original PDFs stored</p></div>''', unsafe_allow_html=True)
    upload = st.file_uploader("Choose a medical lab PDF" if lang == "en" else "लैब रिपोर्ट PDF चुनें", type=["pdf"], accept_multiple_files=False)
    st.caption("Only upload your own report or one you are authorized to share. Stored extracted report content is accessible to the administrator, as agreed during signup.")
    if upload is not None:
        if upload.size > MAX_REPORT_BYTES:
            st.error("File exceeds 10 MB limit.")
        elif st.button("✦ Analyze report with local AI" if lang == "en" else "✦ स्थानीय AI से रिपोर्ट समझें", type="primary"):
            try:
                with st.spinner("Extracting tests and reading values..."):
                    text, n_pages = extract_pdf(upload.getvalue())
                    labs = analyze_labs(text)
                st.success(f"Parsed {n_pages} page(s) and {len(labs)} possible lab values. Verify against the original.")
                _labs_dataframe(labs)
                with st.spinner("Generating careful medical explanation with Ollama..."):
                    summary = report_answer(text, labs, lang)
                report_id = store.save_report(user["id"], clean_filename(upload.name), n_pages, text, labs, summary)
                st.session_state.last_report_id = report_id
                st.success("Analysis saved to your report history.")
            except (ReportError, OllamaUnavailable, ValueError) as exc:
                st.error(str(exc))
    reports = store.list_reports(user["id"], limit=20)
    if reports:
        st.write("")
        section("Your saved reports" if lang == "en" else "आपकी सहेजी रिपोर्ट", "Select a report to review its analysis.", "REPORT LIBRARY")
        options = {f"#{r['id']}  ·  {r['filename']}  ·  {when(r['created_at'])}": r["id"] for r in reports}
        selected = st.selectbox("Report", list(options))
        if selected:
            report = store.get_report(options[selected], user["id"])
            if report:
                _labs_dataframe(report["labs"])
                st.markdown(report["ai_summary"])
                speech_button(report["ai_summary"], lang, key="report_tts")
                _report_export(report, lang)
                with st.expander("View extracted source text (contains personal data)"):
                    st.text(report["extracted_text"])
                with st.expander("Delete this saved report"):
                    st.warning("This permanently removes the extracted report and summary; the original PDF was never stored.")
                    if st.button("Confirm report deletion", key=f"del_r_{report['id']}"):
                        store.delete_report(user["id"], report["id"])
                        st.rerun()


def voice_assistant(user, lang):
    section(t("voice", lang), "Record in English or Hindi, transcribe locally and hear the AI response." if lang == "en" else
            "हिंदी या अंग्रेज़ी में बोलें, सवाल लिखित रूप में देखें और जवाब सुनें।", "VOICE INTELLIGENCE")
    st.markdown('''<div class="voice-scene"><div class="voice-ring"></div><div class="voice-ring r2"></div><div class="voice-ring r3"></div>
    <div class="voice-orb">🎙</div></div>''', unsafe_allow_html=True)
    st.caption("🎤 Microphone permission required. The first transcription needs a one-time download of the local Whisper model; after that transcription runs offline. Spoken playback uses your browser's installed voices.")
    recording = st.audio_input("Record a health question" if lang == "en" else "स्वास्थ्य से जुड़ा सवाल बोलें", sample_rate=16000)
    if recording is not None:
        digest = hashlib.sha256(recording.getvalue()).hexdigest()
        if st.session_state.get("voice_hash") != digest:
            try:
                with st.spinner("Transcribing audio locally..."):
                    transcript = transcribe_audio(recording.getvalue(), "hi" if lang == "hi" else "en")
                st.session_state.voice_hash = digest
                st.session_state.voice_transcript = transcript
            except VoiceError as exc:
                st.error(str(exc))
        if st.session_state.get("voice_hash") == digest:
            transcript = st.session_state.get("voice_transcript", "")
            st.info(f"📝 **Transcribed:** {transcript}")
            if st.button("✦ Ask Ollama" if lang == "en" else "✦ Ollama से पूछें", type="primary"):
                urgent = emergency_notice(transcript, lang)
                if urgent:
                    store.save_interaction(user["id"], transcript, urgent, kind="voice")
                    st.session_state["last_voice_response"] = urgent
                    st.error(urgent)
                    st.stop()
                try:
                    with st.spinner("Generating answer..."):
                        result = medical_answer(transcript, lang)
                    store.save_interaction(user["id"], transcript, result, kind="voice")
                    st.session_state["last_voice_response"] = result
                    st.success("Answer saved in your history.")
                except (ValueError, OllamaUnavailable) as exc:
                    st.error(str(exc))
    if st.session_state.get("last_voice_response"):
        st.markdown("### 🩺 AI response" if lang == "en" else "### 🩺 AI का जवाब")
        st.markdown(st.session_state.last_voice_response)
        speech_button(st.session_state.last_voice_response, lang, key="voice_tts")
    advisory(lang)


def history(user, lang):
    section(t("history", lang), "Review and manage your saved AI conversations and voice questions." if lang == "en" else
            "पिछली बातचीत देखें और हटा सकते हैं।", "PRIVATE TIMELINE")
    interactions = store.list_interactions(user["id"], limit=100)
    if not interactions:
        st.info(t("nothing", lang))
        return
    options = {"All" if lang == "en" else "सभी": "all", "Medical chat": "medical", "Voice": "voice"}
    selection = st.selectbox("Type", list(options))
    for item in interactions:
        if options[selection] != "all" and item["kind"] != options[selection]:
            continue
        with st.expander(f"{'🎙' if item['kind']=='voice' else '💬'} {item['question'][:100]} · {when(item['created_at'])}"):
            st.markdown("**Your question**")
            st.write(item["question"])
            st.markdown("**AI answer**")
            st.markdown(item["response"])
            if st.button("🗑 Delete", key=f"delete_chat_{item['id']}"):
                store.delete_interaction(user["id"], item["id"])
                st.rerun()


def insights(user, lang):
    section(t("insights", lang), "View trends in your parsed report findings. This is not a clinical dashboard." if lang == "en" else
            "अपनी सहेजी रिपोर्ट के नतीजों को चार्ट में देखें।", "HEALTH DATA VISUALIZATION")
    reports = store.list_reports(user["id"], limit=100)
    if not reports:
        st.info("Upload a report to unlock health insights." if lang == "en" else "स्वास्थ्य जानकारी देखने के लिए पहले रिपोर्ट अपलोड करें।")
        return
    all_labs = [lab for report in reports for lab in report["labs"]]
    values = Counter(lab["status"] for lab in all_labs)
    cols = st.columns(3)
    with cols[0]: metric("Saved Reports", len(reports), "📄")
    with cols[1]: metric("Parsed Test Results", len(all_labs), "🔬")
    with cols[2]: metric("Out-of-range Flags", values["Low"]+values["High"], "⚑")
    if not all_labs:
        st.info("No structured lab values available for charts.")
        return
    a,b = st.columns(2)
    with a:
        fig=go.Figure(go.Pie(labels=list(values.keys()),values=list(values.values()),hole=.68,
                             marker={"colors":[{"High":"#ffad66","Low":"#f079ab","Within stated range":"#24dac0","Not evaluated":"#6798ba"}.get(k,"#6798ba") for k in values.keys()]}))
        fig.update_layout(title="Parsed range comparisons",height=360,margin=dict(l=10,r=10,t=55,b=10),
                          paper_bgcolor="rgba(0,0,0,0)",font_color="#b9dae6",showlegend=True,
                          legend=dict(orientation="h",y=-.10))
        st.plotly_chart(fig,use_container_width=True)
    with b:
        common=Counter(lab["name"] for lab in all_labs).most_common(9)
        fig=go.Figure(go.Bar(x=[v for _,v in common],y=[k for k,_ in common],orientation="h",
                             marker={"color":"#2ccfdf"}))
        fig.update_layout(title="Most frequently parsed tests",height=360,margin=dict(l=10,r=10,t=55,b=10),
                          paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#b9dae6",
                          xaxis_title="Number of results",yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig,use_container_width=True)
    st.warning("These labels compare extracted values to ranges printed on each report; they do not constitute a diagnosis. Please verify every result with the original report and a clinician.")


def profile(user, lang):
    section(t("profile", lang), "Manage your account and your stored medical records.", "ACCOUNT & PRIVACY")
    st.markdown("### Account details")
    st.write(f"**Username:** {user['username']} · **Email:** {user['email']}")
    with st.form("profile_edit"):
        name=st.text_input("Display name",value=user["full_name"],max_chars=120)
        selection=st.selectbox("Preferred language",["English","हिंदी"], index=0 if user["language"]=="en" else 1)
        if st.form_submit_button("Save profile"):
            if len(name.strip()) < 2:
                st.error("Name needs at least 2 characters.")
            else:
                code="en" if selection=="English" else "hi"
                store.update_user_profile(user["id"],name.strip(),code)
                st.session_state.language=code
                st.success("Updated.")
                st.rerun()
    with st.expander("🔐 Change password"):
        with st.form("change_pw"):
            old=st.text_input("Current password",type="password")
            new=st.text_input("New password (10+ characters, letters and numbers)",type="password")
            if st.form_submit_button("Change password"):
                try:
                    if change_password(user["id"],old,new):
                        st.success("Password changed.")
                    else:
                        st.error("Current password incorrect.")
                except AuthError as exc:
                    st.error(str(exc))
    with st.expander("🗑 Delete my account and stored health data"):
        st.warning("Irreversible: removes your profile, medical conversations, extracted report text and summaries. Minimal audit-event metadata may remain.")
        with st.form("delete_my_account"):
            confirm=st.text_input("Type DELETE to confirm")
            password=st.text_input("Your password",type="password")
            if st.form_submit_button("Permanently delete my account"):
                if confirm == "DELETE" and confirm_password(user["id"],password):
                    store.delete_account(user["id"])
                    st.session_state.clear()
                    st.rerun()
                else:
                    st.error("Confirmation text or password incorrect.")
    advisory(lang)
