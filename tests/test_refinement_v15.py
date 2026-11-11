"""Regression coverage for the v1.5 usability changes (no private data read)."""
import ast
from pathlib import Path

import pytest

from services.session_flow import active_chat, claim_recording
from ui.strings import t, LANGUAGES

ROOT = Path(__file__).resolve().parents[1]


def test_new_login_starts_clean_and_account_switch_is_isolated():
    state = {}
    first = active_chat(state, 101)
    assert first == []
    first.append({'question': 'hello', 'response': 'hi'})
    assert active_chat(state, 101) == [{'question': 'hello', 'response': 'hi'}]
    assert active_chat(state, 202) == []
    assert active_chat(state, 101) == []  # never reuse other account's chat
    state.clear()  # logout
    assert active_chat(state, 101) == []  # login again


def test_claim_recording_only_once_across_any_number_of_reruns():
    state = {}
    assert not claim_recording(state, '')
    assert claim_recording(state, 'clip-a')
    for _ in range(8):
        assert not claim_recording(state, 'clip-a')
    assert claim_recording(state, 'clip-b')
    assert not claim_recording(state, 'clip-b')
    assert claim_recording({}, 'clip-b')  # brand-new session


def test_chat_is_session_only_while_saved_history_is_separate():
    view = (ROOT / 'views/user_views.py').read_text(encoding='utf-8')
    tree = ast.parse(view)
    chat_node = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'chat')
    snippet = ast.get_source_segment(view, chat_node)
    assert 'active_chat(st.session_state,user[\'id\'])' in snippet
    assert 'store.list_interactions' not in snippet
    assert 'store.save_interaction' in snippet  # history still permanently saved
    assert 'medical_answer(prompt,lang,medical' in snippet
    history_node = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'history')
    assert 'store.list_interactions' in ast.get_source_segment(view, history_node)


def test_logout_and_login_clear_current_chat_but_preserve_database():
    src = (ROOT / 'app.py').read_text(encoding='utf-8')
    assert 'st.session_state.clear()' in src
    assert 'st.session_state["active_chat_messages"] = []' in src
    assert 'st.session_state["active_chat_user_id"] = user["id"]' in src
    assert 'store.delete_interaction' not in src


def test_voice_autosubmits_once_after_successful_recognition():
    view = (ROOT / 'views/user_views.py').read_text(encoding='utf-8')
    tree = ast.parse(view)
    voice = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'voice_assistant')
    snippet = ast.get_source_segment(view, voice)
    assert 'recording=st.audio_input(' in snippet
    assert 'claim_recording(st.session_state,digest)' in snippet
    assert 'transcribe_audio_with_language(audio,None if detect else lang)' in snippet
    assert '_send_voice_query(user,lang,transcript,answer_lang=reply_lang)' in snippet
    assert 'st.session_state[\'voice_transcript\']=transcript.strip()' in snippet
    assert '_send_voice_query(user,lang,corrected,' in snippet  # manual only if corrected
    assert 'corrected.strip()!=st.session_state.get(' in snippet
    assert 'if transcript.strip():' in snippet


def test_playback_speed_choices_and_fast_default():
    src = (ROOT / 'ui/components.py').read_text(encoding='utf-8')
    assert '<option value="1">1×</option>' in src
    assert '<option value="1.25" selected>1.25×</option>' in src
    assert '<option value="1.5">1.5×</option>' in src
    assert '<option value="0.85">' not in src
    assert '<option value="1.15">' not in src
    assert 'Number(document.getElementById(\'speed\').value)' in src


def test_heart_repositioned_without_turning_off_heartbeat():
    css = (ROOT / 'assets/style.css').read_text(encoding='utf-8')
    assert '.stApp .hero.hero-auth .hero-visual' in css
    assert 'top:-45px !important' in css
    assert '.hero .hero-copy::before' in css
    assert '.stApp:has(#theme-light-marker) [data-testid="stMain"] .hero .hero-copy::before' in css
    assert 'animation:cardiac-beat 1.37s' in css
    assert '@media(prefers-reduced-motion:reduce)' in css


@pytest.mark.parametrize('language', list(LANGUAGES))
def test_voice_help_no_longer_claims_manual_click_is_required(language):
    hint = t('voice_review_note', language).lower()
    assert hint
    assert not any(x in hint for x in ('nothing is sent', 'no se envía nada', 'जब तक', 'दाबेपर्यंत'))
