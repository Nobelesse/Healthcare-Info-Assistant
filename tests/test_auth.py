import pytest
from auth.service import AuthError, bootstrap_admin, register_user, login, verify_password
from database import store
from database.models import User


def register(name="person", email="person@example.org"):
    return register_user(name,"Demo Person",email,"StrongPass123",True,"hi")


def test_registration_and_login(sandbox_db):
    u=register()
    assert u["role"]=="user" and u["language"]=="hi"
    assert login("PERSON", "StrongPass123")["id"] == u["id"]
    assert login("person", "BadPassword1") is None
    with store.session_scope() as s:
        row=s.get(User,u["id"])
        assert row.password_hash != "StrongPass123"
        assert verify_password(row.password_hash,"StrongPass123")
    assert all("password" not in k for k in u)


def test_consent_and_name_reserved(sandbox_db):
    with pytest.raises(AuthError, match="Consent"):
        register_user("bob","Bob Sample","bob@example.org","StrongPass123",False)
    with pytest.raises(AuthError, match="reserved"):
        register_user("mr. doc","Some Person","two@example.org","StrongPass123",True)
    with pytest.raises(AuthError, match="Password"):
        register_user("bob","Bob Sample","bob@example.org","weak",True)


def test_case_insensitive_duplicate(sandbox_db):
    register()
    with pytest.raises(AuthError, match="already registered"):
        register_user("Person","Another Person","another@example.org","StrongPass123",True)
    with pytest.raises(AuthError, match="already registered"):
        register_user("other","Another Person","PERSON@example.org","StrongPass123",True)


def test_permanent_admin_bootstrap(sandbox_db):
    assert bootstrap_admin("AdminSecret456789") == "created"
    assert bootstrap_admin("DifferentStrong789") == "ready"  # never silently replace the password
    assert login("Mr. Doc", "AdminSecret456789",role="admin")["role"]=="admin"
    assert login("Mr. Doc", "DifferentStrong789",role="admin") is None
    assert login("Mr. Doc", "AdminSecret456789",role="user") is None
    assert store.set_user_active(1,False) is False


def test_account_deletion_scope(sandbox_db):
    user=register()
    item=store.save_interaction(user["id"],"What is HbA1c?","Explanation")
    report=store.save_report(user["id"],"report.pdf",1,"HbA1c 6.4 % 4-5.6",[],"Summary")
    assert store.delete_account(user["id"])
    assert store.get_user(user["id"]) is None
    assert store.list_interactions(user["id"]) == []
    assert store.list_reports(user["id"]) == []
