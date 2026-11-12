"""Security and full-page offline localization regression tests for v1.8."""
import ast
from pathlib import Path

import pytest
from sqlalchemy import select

from auth.service import register_user, bootstrap_admin, login
from database import store
from database.models import User
from scripts import translate_ui
from ui import strings

ROOT = Path(__file__).resolve().parents[1]
ADMIN_PASSWORD = "AdminSecret456789"


def setup_admin_and_records():
    patient = register_user('patient','Demo Patient','demo@example.org','PatientSecret123',True)
    cid = store.save_interaction(patient['id'],'Private question', 'Private medical answer')
    rid = store.save_report(patient['id'],'demo.pdf',1,'Lab reading',[], 'Private summary')
    bootstrap_admin(ADMIN_PASSWORD)
    admin = login('Mr. Doc',ADMIN_PASSWORD,role='admin')
    return patient, admin, cid, rid


def test_admin_must_reauthenticate_for_every_private_conversation_read(sandbox_db):
    patient, admin, cid, rid=setup_admin_and_records()
    assert store.admin_open_conversation(admin['id'],cid) is None
    assert store.admin_open_conversation(admin['id'],cid,'wrong-secret') is None
    result = store.admin_open_conversation(admin['id'],cid,ADMIN_PASSWORD)
    assert result['response'] == 'Private medical answer'
    # Every NEW call, even in same logged-in session, must supply the secret again.
    assert store.admin_open_conversation(admin['id'],cid) is None
    events=store.audit_log()
    assert any(e['action']=='admin_read_conversation' for e in events)
    assert any(e['action']=='admin_read_conversation_denied' for e in events)
    assert all(ADMIN_PASSWORD not in repr(e) for e in events)
    assert all('Private medical answer' not in repr(e) for e in events)


def test_report_legacy_admin_read_and_profiles_must_reauthenticate(sandbox_db):
    patient,admin,cid,rid=setup_admin_and_records()
    for pw in (None,'incorrect','PatientSecret123'):
        assert store.get_report(rid,admin['id'],admin=True,reauth_password=pw) is None
        assert store.admin_open_report(admin['id'],rid,pw) is None
        assert store.admin_open_user_profile(admin['id'],patient['id'],pw) is None
    assert store.admin_open_report(admin['id'],rid,ADMIN_PASSWORD)['ai_summary']=='Private summary'
    assert store.admin_open_user_profile(admin['id'],patient['id'],ADMIN_PASSWORD)['email']=='demo@example.org'


def test_patient_cannot_bypass_with_actual_admin_password(sandbox_db):
    patient,admin,cid,rid=setup_admin_and_records()
    assert store.admin_open_report(patient['id'],rid,ADMIN_PASSWORD) is None
    assert store.admin_open_conversation(patient['id'],cid,ADMIN_PASSWORD) is None
    assert store.admin_open_user_profile(patient['id'],patient['id'],ADMIN_PASSWORD) is None


def test_old_admin_password_fails_after_hash_changes(sandbox_db):
    patient,admin,cid,rid=setup_admin_and_records()
    from auth.service import hash_password
    with store.session_scope() as s:
        s.get(User,admin['id']).password_hash=hash_password('NewStrongAdminPassword123')
    assert store.admin_open_conversation(admin['id'],cid,ADMIN_PASSWORD) is None
    assert store.admin_open_conversation(admin['id'],cid,'NewStrongAdminPassword123') is not None


def test_no_admin_access_without_patient_consent(sandbox_db):
    patient,admin,cid,rid=setup_admin_and_records()
    with store.session_scope() as s:
        s.get(User,patient['id']).consented=False
    assert store.admin_open_conversation(admin['id'],cid,ADMIN_PASSWORD) is None
    assert store.admin_open_report(admin['id'],rid,ADMIN_PASSWORD) is None
    assert store.admin_open_user_profile(admin['id'],patient['id'],ADMIN_PASSWORD) is None


def test_private_listing_requires_explicit_owner_id(sandbox_db):
    with pytest.raises(ValueError):
        store.list_interactions(None)
    with pytest.raises(ValueError):
        store.list_reports(None)


def test_admin_view_never_caches_password_or_private_content_in_session_state():
    src=(ROOT/'views/admin_views.py').read_text(encoding='utf-8')
    tree=ast.parse(src)
    assert 'with st.form(form_id, clear_on_submit=True)' in src
    assert "type='password'" in src
    assert 'store.admin_open_conversation(admin[\'id\'],cid,password)' in src
    assert 'store.admin_open_report(admin[\'id\'],rid,password)' in src
    assert 'store.admin_open_user_profile(admin[\'id\'], uid, password)' in src
    assert 'admin_open_chat_' not in src  # no persisted private content
    assert 'admin_open_report_' not in src  # no persisted private content
    assert 'st.session_state' not in src


def test_full_language_pack_can_be_generated_with_no_fallback(monkeypatch,tmp_path):
    # Fake translations: no connection to Ollama and no real patient data used.
    monkeypatch.setattr(translate_ui,'CACHE',tmp_path/'instance/locale_overrides.json')
    monkeypatch.setattr(strings,'ROOT',tmp_path)
    strings.reload_locale_cache()
    calls=[]
    def fake_translate(lang, batch):
        calls.extend(batch)
        return {key: ('[日本語] '+strings.C[key][0]) for key in batch}
    monkeypatch.setattr(translate_ui,'translate_batch',fake_translate)
    assert strings.locale_coverage('ja')[0] < len(strings.C)
    complete,total=translate_ui.prepare_language_pack('ja', batch_size=10)
    assert complete==total==len(strings.C)
    strings.reload_locale_cache()
    assert strings.locale_coverage('ja')==(total,total)
    assert 'ja' in strings.complete_locales()
    assert len(set(calls)) == total-len(strings.EXTRA_TEXT['ja'])
    assert strings.t('admin_audit_title','ja').startswith('[日本語]')
    assert 'Healthcare Info Assistant' in strings.t('about_title','ja')
    # Package comes from only authored UI strings, never questions or lab data.
    assert 'Private medical answer' not in repr(calls)
    strings.reload_locale_cache()


def test_bad_or_partial_translation_never_counts_as_completed(monkeypatch,tmp_path):
    monkeypatch.setattr(translate_ui,'CACHE',tmp_path/'instance/locale_overrides.json')
    monkeypatch.setattr(strings,'ROOT',tmp_path)
    strings.reload_locale_cache()
    monkeypatch.setattr(translate_ui,'translate_batch',lambda lang,batch: {})
    done,total=translate_ui.prepare_language_pack('fr',rounds=2)
    assert done<total
    assert 'fr' not in strings.complete_locales()
    strings.reload_locale_cache()


def test_all_app_pages_use_localized_labels_and_guard_partial_locale():
    app=(ROOT/'app.py').read_text('utf8')
    admin=(ROOT/'views/admin_views.py').read_text('utf8')
    user=(ROOT/'views/user_views.py').read_text('utf8')
    assert 'if not _ensure_locale_ready(lang):' in app
    assert 'show_locale_preparation(lang)' in app
    assert 'prepare_language_pack(wanted,progress=on_progress)' not in app  # no blocking UI
    assert 'complete_locales()' in app
    assert 'complete_locales()' in user  # profile cannot choose a partial pack
    assert 't(\'admin_reauth_prompt\',lang)' in admin
    assert all(strings.t('admin_reauth_prompt',language) for language in strings.LANGUAGES)
