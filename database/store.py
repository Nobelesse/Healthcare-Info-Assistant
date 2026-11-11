"""Data-access boundaries. Every user query is scoped by user ID."""
import json
from contextlib import contextmanager
from datetime import datetime, timezone
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import sessionmaker

from config.settings import DB_PATH, database_url
from database.models import Base, User, Interaction, Report, AuditEvent

ENGINE = create_engine(database_url(), connect_args={"check_same_thread": False}, future=True)
Session = sessionmaker(bind=ENGINE, expire_on_commit=False)


@event.listens_for(ENGINE, "connect")
def _sqlite_options(conn, record):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(ENGINE)


@contextmanager
def session_scope():
    with Session() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


def public_user(user: User) -> dict:
    return {"id": user.id, "username": user.username, "full_name": user.full_name,
            "email": user.email, "role": user.role, "consented": user.consented,
            "is_active": user.is_active, "language": user.language,
            "created_at": user.created_at, "last_login_at": user.last_login_at}


def get_user(user_id: int) -> dict | None:
    with session_scope() as s:
        user = s.get(User, user_id)
        return public_user(user) if user else None


def list_users(search: str = "") -> list[dict]:
    with session_scope() as s:
        users = s.scalars(select(User).where(User.role == "user").order_by(User.created_at.desc())).all()
        if search:
            needle = search.casefold()
            users = [u for u in users if needle in u.username.casefold() or needle in u.full_name.casefold() or needle in u.email.casefold()]
        return [public_user(u) for u in users]


def save_interaction(user_id: int, question: str, response: str, kind="medical") -> int:
    with session_scope() as s:
        item = Interaction(user_id=user_id, question=question, response=response, kind=kind)
        s.add(item)
        s.flush()
        return item.id


def list_interactions(user_id: int | None = None, limit: int = 100) -> list[dict]:
    with session_scope() as s:
        q = select(Interaction).order_by(Interaction.created_at.desc()).limit(limit)
        if user_id is not None:
            q = q.where(Interaction.user_id == user_id)
        return [{"id": x.id, "user_id": x.user_id, "kind": x.kind, "question": x.question,
                 "response": x.response, "created_at": x.created_at} for x in s.scalars(q)]


def delete_interaction(user_id: int, interaction_id: int) -> bool:
    with session_scope() as s:
        x = s.scalar(select(Interaction).where(Interaction.id == interaction_id, Interaction.user_id == user_id))
        if x is None:
            return False
        s.delete(x)
        return True


def save_report(user_id: int, filename: str, page_count: int, extracted_text: str, labs: list[dict], ai_summary: str) -> int:
    with session_scope() as s:
        report = Report(user_id=user_id, filename=filename[:180], page_count=page_count,
                        extracted_text=extracted_text, labs_json=json.dumps(labs, ensure_ascii=False), ai_summary=ai_summary)
        s.add(report)
        s.flush()
        return report.id


def _report_dict(r: Report, include_raw: bool) -> dict:
    obj = {"id": r.id, "user_id": r.user_id, "filename": r.filename,
           "page_count": r.page_count, "labs": json.loads(r.labs_json),
           "ai_summary": r.ai_summary, "created_at": r.created_at}
    if include_raw:
        obj["extracted_text"] = r.extracted_text
    return obj


def list_reports(user_id: int | None = None, limit: int = 100) -> list[dict]:
    with session_scope() as s:
        q = select(Report).order_by(Report.created_at.desc()).limit(limit)
        if user_id is not None:
            q = q.where(Report.user_id == user_id)
        return [_report_dict(r, include_raw=False) for r in s.scalars(q)]


def get_report(report_id: int, requesting_user_id: int, *, admin=False) -> dict | None:
    if admin:
        # Backward-compatible admin call; make it consent-gated and automatically audited.
        return admin_open_report(requesting_user_id, report_id)
    with session_scope() as s:
        r = s.scalar(select(Report).where(Report.id == report_id,
                                          Report.user_id == requesting_user_id))
        return _report_dict(r, include_raw=True) if r else None



def delete_report(user_id: int, report_id: int) -> bool:
    with session_scope() as s:
        r = s.scalar(select(Report).where(Report.id == report_id, Report.user_id == user_id))
        if r is None:
            return False
        s.delete(r)
        return True


def counts(user_id: int | None = None) -> dict:
    with session_scope() as s:
        iq = select(func.count(Interaction.id))
        rq = select(func.count(Report.id))
        vq = select(func.count(Interaction.id)).where(Interaction.kind == "voice")
        if user_id is not None:
            iq = iq.where(Interaction.user_id == user_id)
            rq = rq.where(Report.user_id == user_id)
            vq = vq.where(Interaction.user_id == user_id)
        return {"questions": s.scalar(iq), "reports": s.scalar(rq), "voice": s.scalar(vq),
                "users": s.scalar(select(func.count(User.id)).where(User.role == "user"))}


def record_audit(actor_id: int | None, action: str, target_user_id: int | None = None, target_id: int | None = None):
    with session_scope() as s:
        s.add(AuditEvent(actor_id=actor_id, action=action, target_user_id=target_user_id, target_id=target_id))


def audit_log(limit=150) -> list[dict]:
    with session_scope() as s:
        return [{"id": x.id, "actor_id": x.actor_id, "action": x.action,
                 "target_user_id": x.target_user_id, "target_id": x.target_id,
                 "created_at": x.created_at} for x in s.scalars(select(AuditEvent).order_by(AuditEvent.id.desc()).limit(limit))]


def set_user_active(user_id: int, new_state: bool) -> bool:
    with session_scope() as s:
        user = s.get(User, user_id)
        if not user or user.role != "user":
            return False
        user.is_active = new_state
        return True


def update_user_profile(user_id: int, name: str, language: str) -> bool:
    with session_scope() as s:
        user = s.get(User, user_id)
        if not user or user.role != "user":
            return False
        user.full_name = name
        user.language = language
        return True


def delete_account(user_id: int) -> bool:
    with session_scope() as s:
        u = s.get(User, user_id)
        if not u or u.role != "user":
            return False
        for r in s.scalars(select(Report).where(Report.user_id == user_id)):
            s.delete(r)
        for x in s.scalars(select(Interaction).where(Interaction.user_id == user_id)):
            s.delete(x)
        # Retain minimal admin-access audit records, which do not include medical content.
        s.delete(u)
        return True


def _authorized_admin(session, actor_id: int) -> bool:
    actor = session.get(User, actor_id)
    return bool(actor and actor.role == "admin" and actor.is_active)


def admin_report_headers(actor_id: int, limit=200) -> list[dict]:
    """Return non-medical metadata only; no names/text or lab results before audited access."""
    with session_scope() as s:
        if not _authorized_admin(s, actor_id):
            return []
        rows = s.execute(
            select(Report.id, Report.user_id, Report.created_at, Report.page_count)
            .join(User, User.id == Report.user_id)
            .where(User.consented.is_(True))
            .order_by(Report.id.desc()).limit(min(limit, 200))
        ).all()
        return [{"id": r.id, "user_id": r.user_id, "created_at": r.created_at,
                 "page_count": r.page_count} for r in rows]


def admin_open_report(actor_id: int, report_id: int) -> dict | None:
    """Consent-gated report read plus audit event in the same DB transaction."""
    with session_scope() as s:
        if not _authorized_admin(s, actor_id):
            return None
        r = s.scalar(select(Report).join(User, User.id == Report.user_id)
                     .where(Report.id == report_id, User.consented.is_(True)))
        if not r:
            return None
        s.add(AuditEvent(actor_id=actor_id, action="admin_read_report",
                         target_user_id=r.user_id, target_id=r.id))
        return _report_dict(r, include_raw=True)


def admin_conversation_headers(actor_id: int, limit=150) -> list[dict]:
    with session_scope() as s:
        if not _authorized_admin(s, actor_id):
            return []
        rows = s.execute(
            select(Interaction.id, Interaction.user_id, Interaction.created_at, Interaction.kind)
            .join(User, User.id == Interaction.user_id)
            .where(User.consented.is_(True))
            .order_by(Interaction.id.desc()).limit(min(limit, 200))
        ).all()
        return [{"id": r.id, "user_id": r.user_id, "created_at": r.created_at,
                 "kind": r.kind} for r in rows]


def admin_open_conversation(actor_id: int, interaction_id: int) -> dict | None:
    with session_scope() as s:
        if not _authorized_admin(s, actor_id):
            return None
        row = s.scalar(select(Interaction).join(User, User.id == Interaction.user_id)
                       .where(Interaction.id == interaction_id, User.consented.is_(True)))
        if not row:
            return None
        s.add(AuditEvent(actor_id=actor_id, action="admin_read_conversation",
                         target_user_id=row.user_id, target_id=row.id))
        return {"id": row.id, "user_id": row.user_id, "kind": row.kind,
                "question": row.question, "response": row.response, "created_at": row.created_at}


def admin_user_insights(actor_id: int) -> dict:
    """Counts without disclosing medical content."""
    with session_scope() as s:
        if not _authorized_admin(s, actor_id):
            return {}
        active = s.scalar(select(func.count(User.id)).where(User.role == "user", User.is_active.is_(True)))
        inactive = s.scalar(select(func.count(User.id)).where(User.role == "user", User.is_active.is_(False)))
        consented = s.scalar(select(func.count(User.id)).where(User.role == "user", User.consented.is_(True)))
        return {"active": active, "inactive": inactive, "consented": consented}
