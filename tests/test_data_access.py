from auth.service import register_user, bootstrap_admin, login
from database import store


def test_user_cannot_read_or_delete_someone_elses_report(sandbox_db):
    a=register_user("alpha","Alpha User","a@example.org","StrongPass123",True)
    b=register_user("bravo","Bravo User","b@example.org","StrongPass123",True)
    rid=store.save_report(a["id"],"report.pdf",1,"Vitamin D 15 ng/mL 30-100",[],"Low vitamin D")
    assert store.get_report(rid,a["id"])["extracted_text"]=="Vitamin D 15 ng/mL 30-100"
    assert store.get_report(rid,b["id"]) is None
    assert not store.delete_report(b["id"],rid)
    assert store.get_report(rid,b["id"],admin=True) is None  # user cannot claim admin access
    bootstrap_admin("AdminSecret456789")
    administrator = login("Mr. Doc", "AdminSecret456789", role="admin")
    assert store.get_report(rid, administrator["id"], admin=True)["extracted_text"].startswith("Vitamin D")


def test_user_cannot_delete_other_users_conversation(sandbox_db):
    a=register_user("alpha","Alpha User","a@example.org","StrongPass123",True)
    b=register_user("bravo","Bravo User","b@example.org","StrongPass123",True)
    turn=store.save_interaction(a["id"],"Question","Answer")
    assert not store.delete_interaction(b["id"],turn)
    assert len(store.list_interactions(a["id"]))==1
    assert store.delete_interaction(a["id"],turn)
    assert store.list_interactions(a["id"])==[]


def test_admin_audit_metadata(sandbox_db):
    store.record_audit(1,"admin_read_report",2,3)
    records=store.audit_log()
    assert records[0]["actor_id"]==1
    assert records[0]["target_id"]==3
    assert "medical_text" not in str(records[0])
