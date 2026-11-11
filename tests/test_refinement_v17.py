"""v1.7 regression tests for UI alignment and realistic local-LLM speed tuning."""
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_larger_beating_heart_and_no_grid_overlay():
    css = (ROOT / 'assets/style.css').read_text(encoding='utf8')
    new = css.split('v1.7 — clear hero typography', 1)[1]
    assert '.hero::before' in new and 'display:none !important' in new
    assert 'width:59% !important' in new
    assert 'max-height:398px !important' in new
    assert 'width:72% !important' in new  # bounded orbital circle
    assert 'z-index:1 !important' in new
    assert 'max-width:77% !important' in new
    assert 'rgba(8,39,57,.98)' in new  # heading readability veil
    assert 'prefers-reduced-motion:reduce' in css  # preserved
    assert 'animation:cardiac-beat 1.37s' in css


def test_compact_centered_auth_controls_and_sidebar_logout():
    src = (ROOT / 'app.py').read_text(encoding='utf8')
    assert 'def _centered_submit(label):' in src
    assert 'st.columns([0.8, 1.1, 0.8], gap="small")' in src
    for action in ('action_sign_in', 'action_admin_login', 'action_create_account'):
        assert f'_centered_submit(t("{action}", lang))' in src
    assert 'sidebar-logout-gap' in src
    assert 'st.columns([0.26, 0.48, 0.26], gap="small")' in src
    assert 'if st.button("⏻   " + t("logout", lang)' in src


def test_english_tts_faster_default_and_other_locales_preserved():
    # Runtime Streamlit dependencies are intentionally optional for the fast
    # backend test suite; inspect the real UI component source offline.
    src = (ROOT / 'ui/components.py').read_text(encoding='utf8')
    assert "if lang == 'en' else" in src
    assert '<option value="1.75" selected>1.75×</option>' in src
    assert '<option value="2">2×</option>' in src
    assert '<option value="1.25" selected>1.25×</option>' in src
    assert "replace('__SPEED_OPTIONS__',speed_options)" in src
    assert "Number(document.getElementById('speed').value)" in src


def test_small_chat_uses_lower_memory_budget_and_warm_model(monkeypatch):
    from services import ollama_service as api
    captured = []

    class R:
        status_code = 200
        def raise_for_status(self): pass
        def json(self): return {'message': {'content': 'Educational reply.'}}

    def fake_post(url, *, json, timeout):
        captured.append(json)
        return R()

    monkeypatch.setattr(api.httpx, 'post', fake_post)
    api.medical_answer('Explain anemia', 'en', detail='standard')
    assert captured[-1]['options']['num_predict'] == 780
    assert captured[-1]['options']['num_ctx'] == 3072
    assert captured[-1]['keep_alive'] == '12m'
    api.medical_answer('Explain anemia', 'en', detail='short')
    assert captured[-1]['options']['num_predict'] == 430
    api.medical_answer('Explain anemia', 'en', detail='detailed')
    assert captured[-1]['options']['num_predict'] == 1050


def test_translation_stays_strict_and_preserves_long_response_budget(monkeypatch):
    from services import ollama_service as api
    captured=[]

    def fake_send(messages,max_tokens=1050):
        captured.append((messages,max_tokens))
        return 'ठीक है।'

    monkeypatch.setattr(api, '_send', fake_send)
    assert api.translate_answer('Hemoglobin is 14 g/dL.','hi') == 'ठीक है।'
    messages,budget=captured[-1]
    assert budget >= 1200
    assert 'STRICT TRANSLATOR' in messages[0]['content']
    assert 'medical facts' in messages[0]['content']
    assert 'warnings' in messages[0]['content']
    assert 'units' in messages[0]['content']
    assert messages[1]['content'] == 'Hemoglobin is 14 g/dL.'
    api.translate_answer('This is medically important. ' * 300,'fr')
    assert captured[-1][1] == 2300


def test_readme_and_previous_privacy_guards_remain():
    readme = (ROOT / 'README.md').read_text(encoding='utf8')
    assert 'Refinement v1.7' in readme
    assert 'No AI-generated replacement image is needed' in readme
    src=(ROOT / 'app.py').read_text(encoding='utf8')
    assert 'st.session_state.clear()' in src
    assert 'st.session_state["active_chat_messages"] = []' in src
