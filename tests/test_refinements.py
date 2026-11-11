"""Regression tests added in patch 1.1; all work with isolated in-memory data."""
from auth.service import register_user, bootstrap_admin, login
from database import store
from services.report_service import analyze_labs
from services.ollama_service import emergency_notice


def test_extra_lab_tests_and_original_reference_only():
    samples = """ALT (SGPT) 55 U/L 0-40
Uric Acid 8.5 mg/dL 3.5 - 7.2
MCHC 33 g/dL 32 - 36
eGFR 66 mL/min/1.73m2 >60
CRP 18 mg/L
"""
    found = {x["name"]: x for x in analyze_labs(samples)}
    assert found["ALT"]["status"] == "High"
    assert found["Uric Acid"]["status"] == "High"
    assert found["MCHC"]["status"] == "Within stated range"
    assert found["eGFR"]["status"] == "Within stated range"
    assert found["CRP"]["status"] == "Not evaluated"


def test_medical_information_question_is_not_blocked_as_live_emergency():
    assert emergency_notice("What is severe chest pain?", "en") == ""
    assert emergency_notice("Explain severe chest pain", "en") == ""
    assert "Emergency" in emergency_notice("I have severe chest pain", "en")
    assert "आपात" in emergency_notice("मुझे सीने में तेज दर्द है", "hi")


def test_admin_headers_hide_medical_content_until_audited_open(sandbox_db):
    owner = register_user("patient", "Demo Patient", "patient@example.org", "StrongPass123", True)
    report_id = store.save_report(owner["id"], "private-test.pdf", 1,
                                  "CRP 18 mg/L", [], "Sensitive summary")
    chat_id = store.save_interaction(owner["id"], "Private symptom text", "Private AI answer")
    bootstrap_admin("AdminSecret456789")
    admin = login("Mr. Doc", "AdminSecret456789", role="admin")
    headers = store.admin_report_headers(admin["id"])
    chat_headers = store.admin_conversation_headers(admin["id"])
    assert headers[0]["id"] == report_id
    assert "extracted_text" not in str(headers)
    assert "filename" not in str(headers)
    assert "Private symptom" not in str(chat_headers)
    assert store.admin_open_report(owner["id"], report_id) is None
    assert store.admin_open_conversation(owner["id"], chat_id) is None
    assert store.admin_open_report(admin["id"], report_id)["ai_summary"] == "Sensitive summary"
    assert store.admin_open_conversation(admin["id"], chat_id)["question"] == "Private symptom text"
    events = store.audit_log()
    assert [e["action"] for e in events[:2]] == ["admin_read_conversation", "admin_read_report"]


def test_admin_requires_user_consent_on_sensitive_access(sandbox_db):
    owner = register_user("patient", "Demo Patient", "patient@example.org", "StrongPass123", True)
    report_id = store.save_report(owner["id"], "lab.pdf", 1, "CRP 18 mg/L", [], "Demo summary")
    bootstrap_admin("AdminSecret456789")
    admin = login("Mr. Doc", "AdminSecret456789", role="admin")
    # Simulate consent no longer being present in a legacy database record.
    from database.models import User
    with store.session_scope() as session:
        session.get(User, owner["id"]).consented = False
    assert store.admin_open_report(admin["id"], report_id) is None
    assert store.admin_report_headers(admin["id"]) == []
