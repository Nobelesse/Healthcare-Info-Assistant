"""Argon2 password handling, non-public permanent admin creation, account policies."""
import re
from datetime import datetime, timezone
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from config.settings import ADMIN_USERNAME, ADMIN_INITIAL_PASSWORD
from ui.strings import LANGUAGES
from database.models import User
from database.store import session_scope, public_user, record_audit

PASSWORDS = PasswordHasher(time_cost=2, memory_cost=32768, parallelism=2)
USERNAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{2,29}$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")


class AuthError(ValueError):
    pass


def validate_password(password: str, *, admin=False):
    min_length = 12 if admin else 10
    if len(password) < min_length or len(password) > 128:
        raise AuthError(f"Password must have {min_length}–128 characters.")
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        raise AuthError("Password must contain at least one letter and one number.")


def hash_password(password: str) -> str:
    return PASSWORDS.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return PASSWORDS.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, ValueError):
        return False


def register_user(username: str, full_name: str, email: str, password: str, consent: bool, language="en") -> dict:
    username, full_name, email = username.strip(), full_name.strip(), email.strip()
    if username.casefold() == ADMIN_USERNAME.casefold():
        raise AuthError("This username is reserved.")
    if not USERNAME_RE.fullmatch(username):
        raise AuthError("Username must be 3–30 characters, start with a letter, and use letters/numbers/._- only.")
    if not (2 <= len(full_name) <= 120):
        raise AuthError("Enter a name between 2 and 120 characters.")
    if not EMAIL_RE.fullmatch(email) or len(email) > 254:
        raise AuthError("Please enter a valid email address.")
    if not consent:
        raise AuthError("Consent is required because the administrator can access stored medical information.")
    validate_password(password)
    if language not in LANGUAGES:
        raise AuthError("Unsupported language.")
    try:
        with session_scope() as s:
            user = User(username=username, username_key=username.casefold(), full_name=full_name,
                        email=email, email_key=email.casefold(), role="user", is_active=True,
                        consented=True, language=language, password_hash=hash_password(password))
            s.add(user)
            s.flush()
            result = public_user(user)
    except IntegrityError as exc:
        raise AuthError("Username or email is already registered.") from exc
    record_audit(result["id"], "user_registered", result["id"])
    return result


def login(username: str, password: str, *, role="user") -> dict | None:
    if role not in {"user", "admin"}:
        return None
    if role == "admin" and username.casefold() != ADMIN_USERNAME.casefold():
        return None
    with session_scope() as s:
        user = s.scalar(select(User).where(User.username_key == username.strip().casefold(), User.role == role))
        if not user or not user.is_active or not verify_password(user.password_hash, password):
            return None
        user.last_login_at = datetime.now(timezone.utc)
        info = public_user(user)
    record_audit(info["id"], "admin_login" if role == "admin" else "user_login", info["id"])
    return info


def admin_exists() -> bool:
    with session_scope() as s:
        return s.scalar(select(User.id).where(User.role == "admin", User.username_key == ADMIN_USERNAME.casefold())) is not None


def bootstrap_admin(initial_password: str | None = None) -> str:
    """Create the sole admin once. Never reset admin password on later app launches."""
    if admin_exists():
        return "ready"
    password = ADMIN_INITIAL_PASSWORD if initial_password is None else initial_password
    if not password:
        return "needs_password"
    validate_password(password, admin=True)
    try:
        with session_scope() as s:
            s.add(User(username=ADMIN_USERNAME, username_key=ADMIN_USERNAME.casefold(),
                       full_name=ADMIN_USERNAME, email="", email_key=None,
                       role="admin", consented=True, is_active=True, language="en",
                       password_hash=hash_password(password)))
    except IntegrityError:
        return "ready" if admin_exists() else "failed"
    return "created"


def change_password(user_id: int, old_password: str, new_password: str) -> bool:
    validate_password(new_password)
    with session_scope() as s:
        u = s.get(User, user_id)
        if not u or u.role != "user" or not verify_password(u.password_hash, old_password):
            return False
        u.password_hash = hash_password(new_password)
        return True


def confirm_password(user_id: int, candidate: str) -> bool:
    with session_scope() as s:
        u = s.get(User, user_id)
        return bool(u and verify_password(u.password_hash, candidate))
