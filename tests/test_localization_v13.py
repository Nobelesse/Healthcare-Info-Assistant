"""v1.3 multilingual UI, privacy and theme regression checks."""
import ast
from pathlib import Path
import pytest
from auth.service import register_user
from services.ollama_service import _lang_instruction
from ui.strings import C, LANGUAGES, t, supported, local_status

ROOT=Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('lang', list(LANGUAGES))
def test_complete_locales_and_hero(lang):
    assert t('hero_title_1',lang)
    assert t('field_consent',lang)
    assert t('about_privacy_5',lang)
    assert t('admin_sensitive_reports',lang)
    assert t('profile_delete_warning',lang)
    assert t('speech_speaking',lang)
    assert 'Healthcare Info Assistant' in t('about_title',lang)
    assert 'Mr. Doc' in t('field_consent',lang)


def test_every_locale_has_all_translation_keys():
    assert len(LANGUAGES)>=4
    assert len(C)>=250
    assert all(isinstance(row,tuple) and len(row)==len(LANGUAGES) and
               all(isinstance(v,str) and v.strip() for v in row)
               for row in C.values())


def test_no_missing_literal_keys_in_application():
    used=set()
    for path in [ROOT/'app.py',*list((ROOT/'views').glob('*.py')),
                 ROOT/'ui/components.py']:
        tree=ast.parse(path.read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='t':
                if node.args and isinstance(node.args[0],ast.Constant):
                    used.add(node.args[0].value)
    assert used-set(C)==set()
    assert all(k in C for k in ('lab_col_name','lab_col_result','lab_col_unit','lab_col_range',
         'lab_col_comparison','detail_short','detail_standard','detail_detailed',
         'history_all','history_medical','history_voice',
         *(f'about_privacy_{i}' for i in range(1,7))))


def test_fixed_selection_language_controls_no_open_input():
    app=(ROOT/'app.py').read_text(encoding='utf-8')
    member=(ROOT/'views/user_views.py').read_text(encoding='utf-8')
    assert 'st.selectbox(' in app and 'st.selectbox(' in member
    assert 'lang_to_code' not in app
    assert 'accept_new_options=False' in app
    assert 'accept_new_options=True' not in app+member
    assert 'st.text_input("Language' not in app+member


@pytest.mark.parametrize('lang',['hi','mr','es'])
def test_non_english_prompts_and_status(lang):
    assert _lang_instruction(lang)!=_lang_instruction('en')
    assert local_status('High',lang)!=local_status('High','en')
    assert local_status('Within stated range',lang)!=local_status('Within stated range','en')


def test_new_locale_user_registration_and_restrictions(sandbox_db):
    for lang in ('mr','es'):
        account=register_user(f'person_{lang}','Sample Demo',f'{lang}@test.example',
                              'StrongPass123',True,language=lang)
        assert account['language']==lang
    with pytest.raises(ValueError):
        register_user('person_unknown','Sample Demo','no@test.example',
                      'StrongPass123',True,language='unknown')


def test_theme_css_contrast_rules_and_user_data_exclusions():
    css=(ROOT/'assets/style.css').read_text(encoding='utf-8')
    assert '.stApp:has(#theme-light-marker) .hero h1' in css
    assert 'background:linear-gradient(175deg,#103847' in css
    assert '.sidebar-group' in css
    assert '#ffffff !important' in css
    ignored=(ROOT/'.gitignore').read_text(encoding='utf-8')
    assert '.env' in ignored
    assert '.venv' in ignored
    assert 'instance' in ignored
    assert not list((ROOT/'pages').glob('*.py'))


def test_multilingual_emergency_precautions():
    from services.ollama_service import emergency_notice
    assert 'emergencia' in emergency_notice('tengo dolor fuerte en el pecho', 'es').lower()
    assert 'आपत्कालीन' in emergency_notice('मला छातीत तीव्र वेदना आहेत', 'mr')
    assert emergency_notice('qué es dolor fuerte en el pecho', 'es') == ''
