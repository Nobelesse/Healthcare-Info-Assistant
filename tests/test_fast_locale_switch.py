"""v2.0 offline localization: no old-language UI, blocking select, or private data access."""
from concurrent.futures import Future
from pathlib import Path

import pytest

from ui.locale_wait_labels import message
from ui.strings import LANGUAGES, C
from services import locale_service as svc

ROOT = Path(__file__).resolve().parents[1]


def test_all_fourteen_have_first_run_text_in_own_language():
    for code in LANGUAGES:
        fields = ['select','title','detail','hint','progress','error','retry']
        assert all(message(code, field).strip() for field in fields)
        assert message(code, 'progress').format(done=30,total=len(C))
        if code != 'en':
            assert message(code,'title') != message('en','title')


def test_main_pages_wait_for_full_pack_and_no_previous_locale_fallback():
    app=(ROOT/'app.py').read_text('utf8')
    assert app.count('if not _ensure_locale_ready(lang):') == 2
    assert 'show_locale_preparation(lang)' in app
    assert 'st.session_state["language"] = wanted' in app
    assert '_avoid_partial_legacy_locale' not in app
    assert "t('locale_preparing',lang,language=" not in app
    assert 'prepare_language_pack(wanted' not in app
    waiter=(ROOT/'ui/locale_wait.py').read_text('utf8')
    assert 'st.fragment(run_every=' in waiter
    assert 'st.session_state[\'language\'] = selected' in waiter
    assert '_pending_locale_last' in waiter
    assert 'reload_locale_cache()' in waiter


def test_background_worker_uses_only_static_catalog_and_one_thread():
    code=(ROOT/'services/locale_service.py').read_text('utf8')
    assert 'max_workers=1' in code
    assert 'prepare_language_pack' in code
    assert not any(word in code for word in ('user_id', 'medical_text', 'patient', 'password', 'database'))


def test_job_status_is_nonblocking_and_retry_only_when_needed(monkeypatch):
    class FakeExecutor:
        def __init__(self):
            self.calls=[]
            self.future=Future()
        def submit(self, method, *args, **kwargs):
            self.calls.append((method,args,kwargs))
            return self.future
    fake=FakeExecutor()
    monkeypatch.setattr(svc, '_EXECUTOR', fake)
    monkeypatch.setattr(svc, '_JOBS', {})
    monkeypatch.setattr(svc, 'locale_coverage',lambda code: (78,324))

    assert svc.ensure_job('ja') == 'working'
    assert svc.ensure_job('ja') == 'working'
    assert len(fake.calls)==1
    assert fake.calls[0][1] == ('ja',)
    assert svc.job_status('ja') == 'working'
    assert svc.retry_job('ja') == 'working'
    assert len(fake.calls)==1

    fake.future.set_result((324,324))
    assert svc.job_status('ja') == 'ready'
    svc.retry_job('ja')
    assert len(fake.calls)==2


def test_job_failure_reports_retry_not_infinite_requeue(monkeypatch):
    class FakeExecutor:
        def __init__(self): self.calls=0
        def submit(self, fn, *args, **kwargs):
            self.calls+=1
            f=Future();f.set_exception(RuntimeError('offline'))
            return f
    fake=FakeExecutor()
    monkeypatch.setattr(svc,'_EXECUTOR',fake)
    monkeypatch.setattr(svc,'_JOBS',{})
    monkeypatch.setattr(svc,'locale_coverage',lambda code:(78,324))
    assert svc.ensure_job('ja') == 'working'
    assert svc.job_status('ja') == 'failed'
    assert svc.ensure_job('ja') == 'failed'
    assert fake.calls == 1
    assert svc.retry_job('ja') == 'working'
    assert fake.calls == 2


def test_translation_requests_keep_model_warm_without_cloud():
    source=(ROOT/'scripts/translate_ui.py').read_text('utf8')
    assert "'keep_alive': '12m'" in source
    assert '/api/generate' in source
    assert 'OLLAMA_BASE_URL' in source
    assert 'save_cache(data)' in source
