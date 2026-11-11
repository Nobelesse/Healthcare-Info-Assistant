"""Functional v1.6 regressions: safe cached translations and Hindi voice routing."""
from pathlib import Path
from types import SimpleNamespace
import ast
import pytest
from services.translation_service import (
    display_in_language, preferred_voice_language, voice_display_language,
)
from services import voice_service, ollama_service
from ui.strings import LANGUAGES, t, VOICE_LOCALES

ROOT = Path(__file__).resolve().parents[1]


def test_medical_text_translation_happens_once_per_session_and_locale():
    calls=[]
    def fake_translate(text, lang):
        calls.append((text,lang))
        return '## चिकित्सीय अर्थ\nयह मूल उत्तर का अनुवाद है।'
    state={}
    original='## Medical meaning\nThis is a factual answer, not a diagnosis.'
    translated, success=display_in_language(state,original,'hi','en',7,fake_translate)
    assert translated.startswith('## चिकित्सीय') and success
    assert original not in translated
    for _ in range(4):
        assert display_in_language(state,original,'hi','en',7,fake_translate)[0] == translated
    assert calls == [(original,'hi')]
    assert display_in_language(state,original,'en','en',7,fake_translate) == (original,True)
    assert original not in repr(list(state['_translation_cache']))  # hashed cache keys


def test_translation_cache_does_not_leak_between_users_and_clears_on_logout():
    state={}
    calls=[]
    def fake(text,lang):
        calls.append(lang)
        return f'{lang}: translated'
    assert display_in_language(state,'test','hi','en',1,fake)[0]=='hi: translated'
    assert display_in_language(state,'test','hi','en',2,fake)[0]=='hi: translated'
    assert len(calls)==2
    state.clear()  # app logout/login resets Streamlit session state
    assert display_in_language(state,'test','hi','en',2,fake)[0]=='hi: translated'
    assert len(calls)==3


def test_offline_translation_keeps_original_and_does_not_claim_success():
    def fail(text,lang):
        raise ollama_service.OllamaUnavailable('offline')
    original='Sensitive medical report text, saved unchanged.'
    result=display_in_language({},original,'fr','en',9,fail)
    assert result==(original,False)


def test_language_routing_from_whisper_for_all_configured_languages():
    for code in LANGUAGES:
        assert preferred_voice_language('en',code,True,LANGUAGES) == code
        assert code in VOICE_LOCALES
    assert preferred_voice_language('en','hi-IN',True,LANGUAGES)=='hi'
    assert preferred_voice_language('en','hi',False,LANGUAGES)=='en'
    assert preferred_voice_language('en','zz',True,LANGUAGES)=='en'


def test_spoken_language_before_and_selected_language_after_manual_switch():
    assert voice_display_language('en','hi',2,2)=='hi'
    assert voice_display_language('ja','hi',3,2)=='ja'
    assert voice_display_language('hi','hi',3,2)=='hi'


def test_voice_transcribes_in_original_language_and_preserves_metadata(monkeypatch):
    class FakeWhisper:
        def transcribe(self,path,*,beam_size,language,task,vad_filter):
            assert task=='transcribe'  # NEVER 'translate' to English
            assert language is None
            return [SimpleNamespace(text='मुझे विटामिन डी के बारे में बताओ')], SimpleNamespace(language='hi')
    monkeypatch.setattr(voice_service,'_whisper_model',lambda: FakeWhisper())
    text,lang=voice_service.transcribe_audio_with_language(b'RIFF valid bytes',None)
    assert lang=='hi' and 'विटामिन' in text


def test_translation_prompt_preserves_medical_units_and_warnings(monkeypatch):
    captured={}
    def fake_send(messages,max_tokens=1050):
        captured.update(messages=messages,max_tokens=max_tokens)
        return 'परीक्षण मान 160 mg/dL है।'
    monkeypatch.setattr(ollama_service,'_send',fake_send)
    assert 'mg/dL' in ollama_service.translate_answer('Test result is 160 mg/dL.','hi')
    system=captured['messages'][0]['content']
    assert 'STRICT TRANSLATOR' in system
    assert 'medical facts' in system and 'units' in system
    assert captured['max_tokens']>1050


def test_user_chat_and_voice_page_translate_existing_answer():
    view=(ROOT/'views/user_views.py').read_text(encoding='utf-8')
    src=ast.parse(view)
    chat=next(n for n in src.body if isinstance(n,ast.FunctionDef) and n.name=='chat')
    voice=next(n for n in src.body if isinstance(n,ast.FunctionDef) and n.name=='voice_assistant')
    for node in (chat,voice):
        snippet=ast.get_source_segment(view,node)
        assert 'display_in_language(' in snippet
        assert 'speech_button(' in snippet
    voice_text=ast.get_source_segment(view,voice)
    assert "preferred_voice_language(lang, spoken_code, detect, LANGUAGES)" in voice_text
    assert 'transcribe_audio_with_language' in voice_text
    assert 'voice_display_language(' in voice_text


def test_premium_mic_and_contained_hero_have_reduced_motion_guards():
    css=(ROOT/'assets/style.css').read_text(encoding='utf-8')
    view=(ROOT/'views/user_views.py').read_text(encoding='utf-8')
    assert 'voice-mic-icon' in css and '<svg class="voice-mic-icon"' in view
    assert 'right:3% !important' in css
    assert '.hero-orbit-outer{width:69% !important' in css
    assert 'prefers-reduced-motion:reduce' in css
    assert t('translation_unavailable','hi')
    assert t('voice_detected_language','en',locale='Hindi')=='Detected speaking language: Hindi'


def test_history_only_translates_selected_saved_answer_and_report_tracks_creation_lang():
    view=(ROOT/'views/user_views.py').read_text(encoding='utf-8')
    tree=ast.parse(view)
    history=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='history')
    content=ast.get_source_segment(view,history)
    assert 'current=st.selectbox(' in content
    assert 'item=visible[current]' in content
    report=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='report_analyzer')
    report_text=ast.get_source_segment(view,report)
    assert "st.session_state.setdefault('report_original_languages',{})[report_id]=lang" in report_text
    assert 'display_in_language(' in report_text
