"""Tiny, framework-independent session guards for private active conversations.

The database is the user's saved *history*, not the open AI chat transcript.
Session-only data is intentionally reset when a login starts a new Streamlit session.
"""
from collections.abc import MutableMapping
from typing import Any


def active_chat(state: MutableMapping[str, Any], user_id: int) -> list[dict]:
    """Return only the chat created in this login session for this user.

    Any account switch, even without a conventional logout, drops the in-memory
    chat rather than showing another account's in-session messages.
    """
    if state.get("active_chat_user_id") != user_id:
        state["active_chat_user_id"] = user_id
        state["active_chat_messages"] = []
    return state["active_chat_messages"]


def claim_recording(state: MutableMapping[str, Any], digest: str) -> bool:
    """Claim a completed recording once; Streamlit widget reruns cannot resend it.

    Claim before transcription/AI inference so even an error does not create an
    uncontrolled retry loop. To try again, record a new clip, or use correction.
    """
    if not digest or state.get("voice_attempt_digest") == digest:
        return False
    state["voice_attempt_digest"] = digest
    return True
