"""Safe UI components and browser playback with consistent localization."""
import base64
from functools import lru_cache
from html import escape
import json
from pathlib import Path
import re
import streamlit as st
import streamlit.components.v1 as components
from config.settings import ROOT
from ui.strings import t, VOICE_LOCALES


@lru_cache(maxsize=1)
def _heart_data():
    return base64.b64encode((ROOT / 'assets' / 'heart.webp').read_bytes()).decode('ascii')


def inject_css(theme='dark'):
    css = (ROOT / 'assets' / 'style.css').read_text(encoding='utf-8')
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    if theme == 'light':
        st.markdown('<span id="theme-light-marker" hidden></span>', unsafe_allow_html=True)


def brand(lang='en'):
    # Project name remains in English for all locales by explicit user request.
    st.markdown(f'''<div class="brand"><div class="brand-icon">♡</div><div>
      <div class="brand-title">Healthcare<br>Info Assistant</div>
      <div class="brand-subtitle">{escape(t('brand_specialty',lang))} <span class="release-tag">V1.6</span></div>
      </div></div><div class="brand-line"></div>''', unsafe_allow_html=True)


def hero(name='', language='en', landing=False):
    title = f'{escape(t("hero_title_1",language))} <span class="gradient-text">{escape(t("hero_title_2",language))}</span>'
    eyebrow = (t('hero_welcome', language, name=name) if name and not landing
               else t('hero_eyebrow', language))
    img = _heart_data()
    chips = ''.join(f'<span class="hero-chip">{symbol} {escape(t(k,language))}</span>' for symbol,k in
                    [('✧','hero_chip_1'),('◈','hero_chip_2'),('♡','hero_chip_3')])
    st.markdown(f'''<section class="hero{' hero-auth' if landing else ''}">
      <div class="hero-copy"><div class="eyebrow">✦ {escape(eyebrow)}</div>
      <h1>{title}</h1><p>{escape(t('hero_desc',language))}</p>{chips}</div>
      <div class="hero-visual"><div class="hero-orbit hero-orbit-outer"></div>
      <div class="hero-orbit hero-orbit-inner"></div><div class="hero-scanner"></div>
      <div class="heart-float"><div class="heart-pulse-shell" role="img"
      aria-label="Animated anatomical heart illustration"><img class="hero-img"
      src="data:image/webp;base64,{img}" alt="" aria-hidden="true"/></div></div></div>
      <div class="hero-corner-label">{escape(t('hero_stamp', language))}</div></section>''',
                unsafe_allow_html=True)


def section(title, caption='', overline=''):
    st.markdown(f'<div class="section-overline">{escape(overline)}</div>'
                f'<div class="section-heading">{escape(title)}</div>'
                f'<p class="section-caption">{escape(caption)}</p>', unsafe_allow_html=True)


def metric(label: str, value, icon='✧', tint='rgba(45,195,181,.14)'):
    st.markdown(f'''<div class="metric-card" style="--tint:{escape(tint)}">
        <div class="symbol">{escape(icon)}</div><div class="value">{escape(str(value))}</div>
        <div class="hint">{escape(label)}</div></div>''', unsafe_allow_html=True)


def feature_card(title, desc, icon):
    st.markdown(f'''<div class="feature-card"><div class="feature-icon">{escape(icon)}</div>
        <h3>{escape(title)}</h3><p>{escape(desc)}</p></div>''', unsafe_allow_html=True)


def advisory(lang='en'):
    st.markdown(f'<div class="notice">⚕ {escape(t("caution", lang))} {escape(t("emergency",lang))}</div>',
                unsafe_allow_html=True)


def speech_button(text: str, lang='en', key='speech'):
    """Browser TTS: support depends on installed voices. Labels fully localized."""
    cleaned = re.sub(r'[\`*_#>\[\]]', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()[:5000]
    words = {k: t(k,lang) for k in (
        'play','stop','speed','speech_stopped','speech_unavailable','speech_speaking',
        'speech_finished','speech_voice_missing','speech_audio_error')}
    payload = json.dumps(cleaned, ensure_ascii=True).replace('<','\\u003c')
    strings = json.dumps(words,ensure_ascii=True).replace('<','\\u003c')
    locale = VOICE_LOCALES.get(lang, 'en-IN')
    # Requested rate is not standardized across browser/system voices. Make the
    # English starting rate faster and give users more headroom, while leaving
    # existing non-English voice settings unchanged.
    speed_options = (
        '<option value="1.25">1.25×</option><option value="1.5">1.5×</option>'
        '<option value="1.75" selected>1.75×</option><option value="2">2×</option>'
        if lang == 'en' else
        '<option value="1">1×</option><option value="1.25" selected>1.25×</option>'
        '<option value="1.5">1.5×</option>'
    )
    frame = r'''<!doctype html><html><head><meta charset="UTF-8"/><style>
      html,body{margin:0;background:transparent;color:#d9faf5;font:13px system-ui,sans-serif}
      .controls{display:flex;gap:9px;align-items:center;flex-wrap:wrap}
      button,select{border:1px solid #38998e;border-radius:11px;background:#123b49;color:#efffff;padding:9px 13px;cursor:pointer}
      button:hover{background:#196475} label{color:#d9f9f5} #hint{color:#b5dedb;font-size:12px}
      </style></head><body><div class="controls">
      <button id="play"></button><button id="stop" type="button"></button>
      <label for="speed" id="speed-label"></label>
      <select id="speed">__SPEED_OPTIONS__</select><span id="hint"></span></div>
      <script>
      const full=__TEXT__,locale=__LOCALE__,msg=__WORDS__;
      document.getElementById('play').textContent='🔊 '+msg.play;
      document.getElementById('stop').textContent='■ '+msg.stop;
      document.getElementById('speed-label').textContent=msg.speed;
      const hint=document.getElementById('hint');
      function cancel(){if('speechSynthesis' in window) speechSynthesis.cancel();}
      document.getElementById('stop').onclick=()=>{cancel();hint.textContent=msg.speech_stopped;};
      window.addEventListener('pagehide',cancel);
      document.getElementById('play').onclick=()=>{
        if(!('speechSynthesis' in window)){hint.textContent=msg.speech_unavailable;return;}
        cancel();const voices=speechSynthesis.getVoices();
        const langBase=locale.split('-')[0].toLowerCase();
        const voice=voices.find(v=>v.lang.toLowerCase()===locale.toLowerCase()) ||
          voices.find(v=>v.lang.toLowerCase().split('-')[0]===langBase);
        if(!voice){hint.textContent=msg.speech_voice_missing;return;}
        const chunks=full.match(/[\s\S]{1,160}/g)||[full];let index=0;
        hint.textContent=msg.speech_speaking;
        function next(){if(index>=chunks.length){hint.textContent=msg.speech_finished;return;}
          const utter=new SpeechSynthesisUtterance(chunks[index++]);utter.lang=locale;
          utter.rate=Number(document.getElementById('speed').value);if(voice) utter.voice=voice;
          utter.onend=next;utter.onerror=()=>{hint.textContent=msg.speech_audio_error;};
          speechSynthesis.speak(utter);
        }next();
      };
      </script></body></html>'''
    frame = (frame.replace('__TEXT__',payload).replace('__LOCALE__',json.dumps(locale))
             .replace('__WORDS__',strings).replace('__SPEED_OPTIONS__',speed_options))
    components.html(frame,height=88,scrolling=False)


def sidebar_user(user, lang='en'):
    st.markdown(f'<div class="profile-glass"><b>◉ {escape(user["full_name"])}</b>'
                f'<small>● {escape(t("sidebar_account_secure", lang))}</small></div>', unsafe_allow_html=True)


def footer(lang='en'):
    st.markdown(f'<div class="footer-note"><b>Healthcare Info Assistant</b> · {escape(t("footer",lang))}</div>',
                unsafe_allow_html=True)
