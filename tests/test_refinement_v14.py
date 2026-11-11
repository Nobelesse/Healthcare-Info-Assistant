"""Regression tests for medical-pearl UI, local language packs, and user privacy."""
import ast
from pathlib import Path
import pytest
from ui.strings import LANGUAGES, C, t, supported, VOICE_LOCALES, locale_coverage
from services.ollama_service import _lang_instruction, emergency_notice
from scripts.translate_ui import valid_translation, placeholders

ROOT = Path(__file__).resolve().parents[1]


def test_dropdown_constraints_and_language_options():
    app=(ROOT/'app.py').read_text(encoding='utf-8')
    assert 'selected = st.selectbox(' in app
    assert 'accept_new_options=False' in app
    assert 'l = st.selectbox(' in app
    for lang in ('de','fr','ja','zh','pt','ru','ar','bn','ta','te'):
        assert lang in LANGUAGES
        assert lang in VOICE_LOCALES
    assert len(LANGUAGES) >= 14


def test_legacy_complete_translations_untouched():
    for code in ('hi','mr','es'):
        assert locale_coverage(code) == (len(C),len(C))
        assert t('field_consent',code) != t('field_consent','en')
        assert t('emergency',code) != t('emergency','en')
    assert all(len(row)==len(LANGUAGES) for row in C.values())
    assert len(C) >= 300


@pytest.mark.parametrize('code',['fr','de','ja','zh','pt','ru','ar','bn','ta','te'])
def test_extra_locales_curated_core_and_ai_instruction(code):
    assert supported(code) == code
    assert t('guest_user_login',code) != t('guest_user_login','en')
    assert t('field_username',code) != t('field_username','en')
    assert t('emergency',code) != t('emergency','en')
    assert _lang_instruction(code) != _lang_instruction('en')
    assert 'Healthcare Info Assistant' in t('about_title',code)
    assert 'Mr. Doc' in t('field_consent',code)
    assert locale_coverage(code)[0] < len(C)  # Do not falsely claim completeness


def test_heart_beats_without_video_and_reduced_motion():
    view=(ROOT/'ui/components.py').read_text(encoding='utf-8')
    css=(ROOT/'assets/style.css').read_text(encoding='utf-8')
    assert 'heart-pulse-shell' in view
    assert '@keyframes cardiac-beat' in css
    assert 'animation:cardiac-beat 1.37s' in css
    assert '@media(prefers-reduced-motion:reduce)' in css
    assert '.stApp .heart-pulse-shell,.stApp .heart-pulse-shell::before' in css


def test_light_hero_colors_and_sidebar_picker_are_readable():
    css=(ROOT/'assets/style.css').read_text(encoding='utf-8')
    assert '.stApp:has(#theme-light-marker) [data-testid="stMain"] .hero .hero-copy h1' in css
    assert 'background-image:linear-gradient(99deg,#078879,#3972b5)' in css
    assert '#f9fefa' in css and '#f6fcff' in css
    assert 'stSelectbox' in css
    assert 'accept_new_options=True' not in (ROOT/'app.py').read_text(encoding='utf-8')


def test_optional_translation_pack_input_validation():
    assert placeholders('Hello {username}, {count}') == ['count','username']
    assert valid_translation('Hello {username}', 'Bonjour {username}')
    assert not valid_translation('Hello {username}', 'Bonjour')
    assert not valid_translation('Healthcare Info Assistant', 'Something Else')
    assert not valid_translation('Mr. Doc', 'Admin')


def test_patch_changes_do_not_require_private_files():
    from config.settings import ROOT as ROOT_CONFIG
    assert ROOT_CONFIG == ROOT
    assert (ROOT/'scripts/translate_ui.py').exists()
    assert not (ROOT/'pages').exists()
