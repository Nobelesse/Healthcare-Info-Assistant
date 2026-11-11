"""Permanent administrator: user directory, report access, conversations, audit trail."""
from datetime import datetime
import streamlit as st
from database import store
from ui.components import section, metric, advisory
from pages.user_views import when, _labs_dataframe


def overview(admin, lang):
    section("Control Center" if lang == "en" else "प्रशासन डैशबोर्ड", "Authorized, auditable access to user accounts and saved health information.", "MR. DOC · ADMINISTRATION")
    numbers = store.counts()
    cols = st.columns(4)
    for col, (label, value, icon) in zip(cols, [
        ("Registered Users", numbers["users"], "👥"), ("AI Conversations", numbers["questions"], "💬"),
        ("Analyzed Reports", numbers["reports"], "📄"), ("Voice Sessions", numbers["voice"], "🎙")]):
        with col: metric(label, str(value), icon)
    st.markdown('''<div class="glass-panel"><b>🛡 PRIVACY & ADMINISTRATOR ACCESS</b><p style="color:#a5d0dc;font-size:14px;line-height:1.8">
    Users must acknowledge administrator access to stored medical report text and AI conversation history at signup. Opening a user's private report or conversation is logged. Passwords cannot be viewed. Original PDF files are not stored.</p></div>''', unsafe_allow_html=True)
    st.markdown("### Recent account registrations")
    users = store.list_users()[:10]
    if users:
        st.dataframe([{"ID":u["id"], "Username":u["username"], "Full name":u["full_name"],
                       "Active":u["is_active"], "Joined":when(u["created_at"])} for u in users],
                     hide_index=True,use_container_width=True)
    else:
        st.info("No registered users yet.")


def users(admin, lang):
    section("User Directory", "Find registered users, view profile details and manage account access.", "IDENTITY MANAGEMENT")
    search = st.text_input("Search username, name or email", placeholder="Type a search term...")
    all_users = store.list_users(search)
    st.caption(f"{len(all_users)} users found. Password hashes and credentials are never displayed.")
    for u in all_users[:80]:
        label=f"{'🟢' if u['is_active'] else '🔴'} {u['full_name']} · @{u['username']} · User #{u['id']}"
        with st.expander(label):
            left,right=st.columns(2)
            with left:
                st.write(f"**Email:** {u['email']}")
                st.write(f"**Preferred language:** {u['language'].upper()}")
                st.write(f"**Consent acknowledged:** {'Yes' if u['consented'] else 'No'}")
            with right:
                st.write(f"**Joined:** {when(u['created_at'])}")
                st.write(f"**Last login:** {when(u['last_login_at'])}")
                st.write(f"**Account:** {'Active' if u['is_active'] else 'Disabled'}")
            button_label="Deactivate user" if u["is_active"] else "Reactivate user"
            if st.button(button_label, key=f"status_u_{u['id']}"):
                store.set_user_active(u["id"], not u["is_active"])
                store.record_audit(admin["id"], "admin_user_status_change", u["id"])
                st.rerun()


def reports(admin, lang):
    section("All Medical Reports", "Access stored extracted text, interpreted labs and saved AI reports. All reads are audited.", "SENSITIVE REPORT ACCESS")
    all_reports = store.list_reports(limit=200)
    if not all_reports:
        st.info("No uploaded reports yet.")
        return
    users_by_id = {u["id"]:u for u in store.list_users()}
    st.caption("Original uploaded PDF bytes are not retained. Only extracted report text, values and AI summaries are stored.")
    for r in all_reports:
        owner=users_by_id.get(r["user_id"],{}).get("username","Unknown")
        with st.expander(f"📄 {r['filename']} · @{owner} · {when(r['created_at'])}"):
            st.write(f"**User ID:** {r['user_id']} | **Pages:** {r['page_count']}")
            st.write(f"**Parsed tests:** {len(r['labs'])}")
            if st.button("🔒 Open private report (audited)",key=f"admin_read_r_{r['id']}"):
                # Authenticated admin is the only caller of this privileged path.
                details = store.get_report(r["id"], admin["id"], admin=True)
                if details:
                    store.record_audit(admin["id"], "admin_read_report", r["user_id"], r["id"])
                    st.markdown("#### Structured lab results")
                    _labs_dataframe(details["labs"])
                    st.markdown("#### AI explanation")
                    st.markdown(details["ai_summary"])
                    st.markdown("#### Original extracted text")
                    st.text(details["extracted_text"])
                else:
                    st.error("Report not found.")


def conversations(admin, lang):
    section("Conversation Access", "View user questions and stored AI responses with access logging.", "SENSITIVE CHAT ACCESS")
    all_items=store.list_interactions(limit=150)
    users_by_id={u["id"]:u for u in store.list_users()}
    if not all_items:
        st.info("No conversations yet.")
        return
    for item in all_items:
        owner=users_by_id.get(item["user_id"],{}).get("username","Unknown")
        with st.expander(f"{'🎙' if item['kind']=='voice' else '💬'} @{owner} · {when(item['created_at'])} · {item['question'][:75]}"):
            st.write(f"**User ID:** {item['user_id']} · **Type:** {item['kind']}")
            if st.button("🔒 Open private conversation (audited)",key=f"admin_open_chat_{item['id']}"):
                store.record_audit(admin["id"], "admin_read_conversation", item["user_id"], item["id"])
                st.markdown("**User's question**")
                st.write(item["question"])
                st.markdown("**AI answer**")
                st.markdown(item["response"])


def audit(admin, lang):
    section("Access Audit Trail", "Read-only log of account creation, logins, and sensitive administrator actions.", "ACCOUNTABILITY")
    rows=store.audit_log(limit=150)
    if not rows:
        st.info("No audit events yet.")
        return
    st.dataframe([{"Time":when(item["created_at"]),"Actor ID":item["actor_id"],"Action":item["action"],
                   "User ID":item["target_user_id"],"Record ID":item["target_id"]} for item in rows],
                 hide_index=True,use_container_width=True)
    st.caption("Audit records contain event metadata only, not passwords or medical report content.")
