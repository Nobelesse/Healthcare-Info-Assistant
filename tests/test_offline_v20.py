"""V2 regression: local grounding, conservative comparisons, streaming and privacy."""
import io
import json
import sqlite3
from pathlib import Path
import pytest
from services.knowledge_service import search_knowledge, for_lab_names, catalog, grounding_message
from services.comparison_service import compare_reports
from services.secure_backup import encrypt_database, decrypt_database, restore_as_new_file
from services.offline_status import is_loopback_base
from ui.v2_strings import v2t, KEYS, LANG_CODES


def test_curated_knowledge_is_bundled_with_traceable_source():
    assert len(catalog()) >= 8
    items=search_knowledge('What does high LDL cholesterol mean?')
    assert items and items[0]['id']=='cholesterol'
    assert items[0]['source_url'].startswith('https://medlineplus.gov/')
    assert not search_knowledge('Explain the legal statute of a trademark.')
    assert search_knowledge('मुझे विटामिन डी के बारे में बताओ')[0]['id']=='vitamin_d'
    assert '[1]' in grounding_message(items)


def test_lab_grounding_never_includes_unmatched_data():
    items=for_lab_names([{'name':'Vitamin B12'}, {'name':'TSH'}, {'name':'Unknown chemical'}])
    assert {x['id'] for x in items} == {'b12','thyroid'}


def test_comparison_rejects_mixed_units_and_duplicate_results():
    a={'id':1,'labs':[{'name':'LDL Cholesterol','unit':'mg/dL','value':166,'status':'High','reference':'0-100'},
                      {'name':'Glucose','unit':'mmol/L','value':5.3,'status':'Within stated range'},
                      {'name':'Hemoglobin','unit':'g/dL','value':14.1},
                      {'name':'Hemoglobin','unit':'g/dL','value':13.9}]}
    b={'id':2,'labs':[{'name':'LDL Cholesterol','unit':'mg/dL','value':152,'status':'High','reference':'0-100'},
                      {'name':'Glucose','unit':'mg/dL','value':97},
                      {'name':'Hemoglobin','unit':'g/dL','value':14.0}]}
    rows=compare_reports(a,b)
    assert len(rows)==1
    assert rows[0]['name']=='LDL Cholesterol' and rows[0]['change']==-14
    with pytest.raises(ValueError):
        compare_reports(a,a)


def test_comparison_rejects_unknown_or_nonfinite_values():
    a={'id':1,'labs':[{'name':'TSH','value':float('nan'),'unit':'mIU/L'},
                       {'name':'A1c','value':5.9,'unit':'unit not found'}]}
    b={'id':2,'labs':[{'name':'TSH','value':4.0,'unit':'mIU/L'},
                       {'name':'A1c','value':6.0,'unit':'unit not found'}]}
    assert compare_reports(a,b)==[]


def test_backup_is_aes_encrypted_and_restore_is_non_destructive(tmp_path):
    src=tmp_path/'original.sqlite'
    with sqlite3.connect(src) as con:
        con.execute('CREATE TABLE records (note TEXT)')
        con.execute('INSERT INTO records VALUES (?)',('sensitive fictitious record',))
    payload=encrypt_database('LongPrivatePassphrase!42',src)
    assert payload.startswith(b'HIA-SECURE-BACKUP')
    assert b'sensitive fictitious record' not in payload
    with pytest.raises(ValueError):
        decrypt_database(payload,'IncorrectPassphrase42')
    with pytest.raises(ValueError):
        decrypt_database(payload[:-20]+b'0'*20,'LongPrivatePassphrase!42')
    out=tmp_path/'new-restored.sqlite'
    restore_as_new_file(payload,'LongPrivatePassphrase!42',out)
    with sqlite3.connect(out) as con:
        assert con.execute('SELECT note FROM records').fetchone()[0]=='sensitive fictitious record'
    with pytest.raises(FileExistsError):
        restore_as_new_file(payload,'LongPrivatePassphrase!42',out)
    assert src.exists()


def test_locale_keys_all_languages():
    assert len(LANG_CODES)==14
    assert all(len(v)==len(LANG_CODES) for v in KEYS.values())
    for lang in LANG_CODES:
        for key in KEYS:
            assert v2t(key,lang).strip()
        assert v2t('offline_heading',lang)
        assert v2t('test',lang)


def test_no_cloud_required_for_offline_status():
    assert is_loopback_base('http://127.0.0.1:11434')
    assert is_loopback_base('http://localhost:11434')
    assert not is_loopback_base('https://my-cloud-llm.example')
    assert not is_loopback_base('file:///etc/passwd')


def test_ollama_stream_receives_chunks_without_saving_global_history(monkeypatch):
    import services.ollama_service as ollama
    calls={}
    class MockResponse:
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def raise_for_status(self): return None
        def iter_lines(self):
            return iter([json.dumps({'message':{'content':'नमस्ते'}}),
                         json.dumps({'message':{'content':' दोस्त'}}),
                         json.dumps({'done':True})])
    def fake_stream(*a,**kw):
        calls.update(kw)
        return MockResponse()
    monkeypatch.setattr(ollama.httpx,'stream',fake_stream)
    result=''.join(ollama.medical_answer('What is anemia?',stream=True))
    assert result=='नमस्ते दोस्त'
    assert calls['json']['stream'] is True
    assert 'iron deficiency' in calls['json']['messages'][0]['content'].lower()


def test_local_image_ocr_requires_opt_in(monkeypatch):
    from services import report_service
    monkeypatch.setattr(report_service,'ENABLE_OCR',False)
    with pytest.raises(report_service.ReportError,match='optional'):
        report_service.extract_image(b'fake PNG')


def test_current_admin_privacy_and_navigation_code_present():
    root=Path(__file__).resolve().parents[1]
    app=(root/'app.py').read_text(encoding='utf-8')
    admin=(root/'views'/'admin_views.py').read_text(encoding='utf-8')
    assert 'user_views.offline_readiness' in app
    assert "confirm_password(admin['id'],verify)" in admin
    assert "type='password'" in admin
    assert (root/'data'/'medical_knowledge.json').exists()
