"""Original dashboard components. All user-controlled HTML content is escaped."""
import base64
from functools import lru_cache
from html import escape
import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from config.settings import ROOT
from ui.strings import t


@lru_cache(maxsize=1)
def _heart_data():
    return base64.b64encode((ROOT / "assets" / "heart.webp").read_bytes()).decode("ascii")


def inject_css(theme="dark"):
    css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    if theme == "light":
        st.markdown('<span id="theme-light-marker" style="display:none"></span>', unsafe_allow_html=True)


def brand():
    st.markdown('''<div class="brand"><div class="brand-icon">♡</div><div>
    <div class="brand-title">Healthcare<br>Info Assistant</div><div class="brand-subtitle">AI • MEDTECH</div></div></div>
    <div class="brand-line"></div>''', unsafe_allow_html=True)


def hero(name="", language="en", landing=False):
    title = ("आपका डिजिटल स्वास्थ्य साथी" if language == "hi" else "Intelligent Healthcare, <span class='gradient-text'>Simply Explained.</span>")
    subtitle = ("बीमारियों, कमियों और लैब रिपोर्ट को आसान हिंदी में समझें।" if language == "hi" else
                "Understand health conditions, nutrition and medical reports with local AI — private, bilingual and designed for clarity.")
    eyebrow = "AI-POWERED HEALTH INSIGHTS" if language == "en" else "AI आधारित स्वास्थ्य जानकारी"
    if name and not landing:
        eyebrow = (f"WELCOME BACK, {escape(name.upper())}" if language == "en" else f"स्वागत है, {escape(name)}")
    img = _heart_data()
    html = f'''<section class="hero"><div class="hero-copy"><div class="eyebrow">✦ {eyebrow}</div>
       <h1>{title}</h1><p>{subtitle}</p>
       <span class="hero-chip">✧ {"Bilingual AI" if language == "en" else "हिंदी + English"}</span>
       <span class="hero-chip">◈ Offline AI · Ollama</span>
       <span class="hero-chip">♡ Medical education</span></div>
       <img class="hero-img" src="data:image/webp;base64,{img}" alt="Decorative futuristic 3D holographic heart" /></section>'''
    st.markdown(html, unsafe_allow_html=True)


def section(title, caption="", overline="EXPERIENCE"):
    st.markdown(f'<div class="section-overline">{escape(overline)}</div><div class="section-heading">{escape(title)}</div>'
                f'<p class="section-caption">{escape(caption)}</p>', unsafe_allow_html=True)


def metric(label: str, value: str, icon="✧", tint="#19cde4"):
    st.markdown(f'''<div class="metric-card" style="--tint:{escape(tint)}"><div class="symbol">{escape(icon)}</div>
    <div class="value">{escape(str(value))}</div><div class="hint">{escape(label)}</div></div>''', unsafe_allow_html=True)


def feature_card(title, desc, icon):
    st.markdown(f'''<div class="feature-card"><div class="feature-icon">{escape(icon)}</div>
    <h3>{escape(title)}</h3><p>{escape(desc)}</p></div>''', unsafe_allow_html=True)


def advisory(lang="en"):
    st.markdown(f'<div class="notice">⚕ {escape(t("caution",lang))} '
                + ("For urgent symptoms, seek emergency services immediately." if lang == "en" else
                   "गंभीर लक्षण होने पर तुरंत आपातकालीन चिकित्सा सहायता लें।") + '</div>', unsafe_allow_html=True)


def speech_button(text: str, lang="en", key="speech"):
    """Local browser TTS after a direct user click; no network services or paid voices."""
    text = text[:2200]
    serialized = json.dumps(text, ensure_ascii=True).replace("<", "\\u003c")
    langtag = "hi-IN" if lang == "hi" else "en-IN"
    components.html(f'''<!doctype html><html><head><style>
      body{{margin:0;background:transparent;font-family:system-ui;}}
      button{{padding:10px 17px;border:1px solid #38dddc;border-radius:12px;background:linear-gradient(135deg,#0b5868,#0b2a4b);color:#c8ffff;cursor:pointer;font-weight:650}}
      button:hover{{box-shadow:0 0 20px #0c8790;}}</style></head>
      <body><button id="speak">🔊 {"सुनें / रोकें" if lang == "hi" else "Read aloud / Stop"}</button>
      <script>const text={serialized};const lang={json.dumps(langtag)};
      document.getElementById('speak').addEventListener('click',()=>{{
      if(!('speechSynthesis' in window)){{alert('Speech playback not supported by this browser.');return;}}
      if(speechSynthesis.speaking){{speechSynthesis.cancel();return;}}
      let u=new SpeechSynthesisUtterance(text);u.lang=lang;u.rate=.92;
      let voices=speechSynthesis.getVoices();let v=voices.find(x=>x.lang.toLowerCase().startsWith(lang.slice(0,2).toLowerCase()));
      if(v)u.voice=v;speechSynthesis.speak(u);
      }});</script></body></html>''', height=58, scrolling=False)


def sidebar_user(user, lang="en"):
    safe_name = escape(user["full_name"])
    st.markdown(f'<div class="profile-glass"><b>◉ {safe_name}</b><small>● SECURE USER ACCOUNT</small></div>', unsafe_allow_html=True)


def footer():
    st.markdown('<div class="footer-note">HEALTHCARE INFO ASSISTANT • LOCAL AI · PRIVACY-FIRST DEMONSTRATION<br>'
                'Educational information, not medical advice or diagnosis. Always verify report readings with your laboratory and clinician.</div>',
                unsafe_allow_html=True)
