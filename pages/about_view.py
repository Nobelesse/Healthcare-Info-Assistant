"""Project-only About page; deliberately no college, institute or academic references."""
import streamlit as st
from ui.components import hero, section, feature_card, advisory


def about_page(lang="en"):
    hero(language=lang,landing=True)
    st.write("")
    if lang == "hi":
        section("प्रोजेक्ट के बारे में", "आपका बुद्धिमान स्वास्थ्य जानकारी साथी — आसान भाषा में स्वास्थ्य जानकारी।", "OUR PURPOSE")
        st.markdown('''Healthcare Info Assistant एक स्थानीय AI आधारित डिजिटल स्वास्थ्य सूचना प्रणाली है। यह
        सामान्य स्वास्थ्य सवालों, बीमारियों, पोषक तत्वों की कमी और लैब रिपोर्ट को समझने में मदद करता है।
        उपयोगकर्ता हिंदी या अंग्रेज़ी में सवाल पूछ सकते हैं, PDF लैब रिपोर्ट का सार समझ सकते हैं और आवाज़ से बातचीत कर सकते हैं।''')
    else:
        section("About Healthcare Info Assistant", "Your Intelligent Healthcare Information Companion.", "OUR PURPOSE")
        st.markdown('''Healthcare Info Assistant is a privacy-conscious, local-AI-powered health education platform designed
        to make complex medical information easier to understand. It supports everyday questions about diseases, symptoms,
        nutritional deficiencies and lab reports in **English and Hindi**. It is not a clinical diagnostic device.''')
    cols=st.columns(3)
    cards=[("AI Medical Chat", "Medical and everyday explanations, nutrition education and when to seek care.", "🧠"),
           ("Lab Report Intelligence", "Extracts text and compares lab values with explicitly reported reference ranges.", "📊"),
           ("Voice + Multilingual", "Whisper speech recognition, Ollama responses and browser-generated speech.", "🎙")]
    for col,(title,desc,icon) in zip(cols,cards):
        with col: feature_card(title,desc,icon)
    st.write("")
    section("How it works" if lang == "en" else "यह कैसे काम करता है", "A local-first architecture built around transparency and accessibility.", "BEHIND THE EXPERIENCE")
    st.markdown('''<div class="glass-panel"><div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-around;text-align:center;font-weight:700;font-size:14px">
     <div>🖥 Streamlit Interface</div><div>➜</div><div>🧠 Local Ollama AI</div><div>➜</div><div>🗣 Clear Explanations</div>
     </div><hr style="margin:15px 0"><div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-around;text-align:center;font-size:13px">
     <div>📄 PyMuPDF + Optional OCR</div><div>◈</div><div>🔐 Argon2 + SQLite</div><div>◈</div><div>🎤 Whisper + Browser Voice</div>
     </div></div>''',unsafe_allow_html=True)
    section("Privacy and boundaries" if lang == "en" else "गोपनीयता और सीमाएँ", "Know exactly what the app does and does not do.", "TRUST BY DESIGN")
    st.markdown('''- **Your data:** Stored conversations, extracted report text and summaries remain in the local SQLite database.
    - **Administrator access:** The permanent administrator, **Mr. Doc**, can view stored user information and medical content. This is disclosed during registration, and sensitive accesses are logged.
    - **Original PDFs:** Files are read in memory and not permanently saved. Scanned documents require optional Tesseract OCR.
    - **AI processing:** Ollama runs on your computer; the app does not send prompts to Gemini or another paid AI API.
    - **No diagnosis:** AI output can be incomplete or incorrect. Report range comparisons are only a first-pass aid and require checking against the original laboratory report.
    - **Deployment:** This is a local, educational demonstration, not a certified medical product or internet-hosted patient portal.
    ''')
    st.markdown("#### Useful independent medical resources")
    st.markdown("[WHO](https://www.who.int/health-topics) · [MedlinePlus](https://medlineplus.gov/) · [NHS](https://www.nhs.uk/conditions/) · [NIH Office of Dietary Supplements](https://ods.od.nih.gov/)")
    advisory(lang)
