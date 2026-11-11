"""Healthcare Info Assistant — one Streamlit entrypoint with role-aware in-app navigation.

Important: reusable views deliberately live in ``views/``, not Streamlit's reserved
``pages/`` folder. Only app.py is an executable route. The internal view modules
must never be exposed as separate (blank, unguarded) browser pages.
"""
from html import escape
import streamlit as st
from auth.service import AuthError, register_user, login, bootstrap_admin
from config.settings import ADMIN_USERNAME
from database.store import initialize_database, get_user
from database import store
from ui.components import inject_css, brand, sidebar_user, footer, hero, section, advisory
from ui.strings import t, LANGUAGES, supported, locale_coverage, complete_locales, reload_locale_cache
from views import user_views, admin_views
from views.about_view import about_page
from ui.v2_strings import v2t

st.set_page_config(
    page_title="Healthcare Info Assistant | Medical AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)
initialize_database()
try:
    ADMIN_SETUP = bootstrap_admin()
except AuthError as e:
    ADMIN_SETUP = "invalid_config"
    ADMIN_ERROR = str(e)


# These are *application states*, not separate Streamlit pages. This is also why
# there is no public administrator registration route.
GUEST_PAGES = {"user_login", "register", "admin_login", "about"}


def _avoid_partial_legacy_locale(lang):
    """Old user profiles may contain an unfinished 1.4–1.7 locale selection."""
    done,total=locale_coverage(lang)
    if done < total:
        st.session_state['legacy_locale_pending']=lang
        st.session_state['language']='en'
        return 'en'
    return lang


def _session_start(user, *, preserve_selected_language=False):
    # Preserve deliberate language/theme choices while discarding account-specific state.
    theme = st.session_state.get("theme", "dark")
    current = st.session_state.get("language")
    chosen = supported(current) if preserve_selected_language and current else supported(user["language"])
    if preserve_selected_language and user["role"] == "user" and chosen != user["language"]:
        store.update_user_profile(user["id"], user["full_name"], chosen)
    st.session_state.clear()
    st.session_state["theme"] = theme
    st.session_state["identity"] = {"user_id": user["id"], "role": user["role"]}
    # Fresh, private active chat at every login; saved history stays in SQLite.
    st.session_state["active_chat_user_id"] = user["id"]
    st.session_state["active_chat_messages"] = []
    st.session_state["language"] = chosen
    st.session_state["page"] = "overview" if user["role"] == "admin" else "home"
    st.rerun()


def _logout():
    st.session_state.clear()
    st.rerun()


def _sidebar_heading(title, description=""):
    """Accessible, visually separated navigation heading with a short explanation."""
    st.markdown(
        f'<div class="sidebar-group"><div class="sidebar-group-title">{escape(title)}</div>'
        f'<p class="sidebar-group-description">{escape(description)}</p></div>',
        unsafe_allow_html=True,
    )


def _nav_button(page, icon, label, *, guest=False):
    state_key = "guest_page" if guest else "page"
    if st.button(
        f"{icon}   {label}",
        key=f"{'guest' if guest else 'auth'}_nav_{page}",
        type="primary" if st.session_state.get(state_key) == page else "secondary",
        width="stretch",
    ):
        st.session_state[state_key] = page
        st.rerun()


def _sidebar_preferences(lang, *, guest=False, user=None, admin=False):
    _sidebar_heading(t("sidebar_preferences", lang), t("sidebar_preferences_help", lang))
    options=list(LANGUAGES)
    selected = st.selectbox(
        t("sidebar_language_label", lang),
        options=options,
        index=options.index(supported(lang)),
        format_func=LANGUAGES.get,
        key="guest_language_select" if guest else "member_language_select",
        accept_new_options=False,
        width="stretch",
    )
    wanted=selected
    if wanted != lang:
        complete,total = locale_coverage(wanted)
        if complete < total:
            # A partial language must not silently show English labels across
            # admin, chat, report and profile pages. Build its *entire* UI
            # catalog via local Ollama, then switch only if 100% is validated.
            if st.session_state.get('locale_preparation_failed') == wanted:
                st.warning(t('locale_prepare_failed',lang))
                if st.button('↻ '+t('locale_preparing',lang,language=LANGUAGES[wanted]),
                             key='retry_locale_pack'):
                    st.session_state.pop('locale_preparation_failed',None)
                    st.rerun()
                return
            from scripts.translate_ui import prepare_language_pack, TranslationPreparationError
            with st.status(t('locale_preparing',lang,language=LANGUAGES[wanted]), expanded=True) as status:
                bar=st.progress(complete/total)
                label=st.empty()
                def on_progress(done,count):
                    bar.progress(done/count)
                    label.caption(t('locale_progress',lang,complete=done,total=count))
                try:
                    complete,total=prepare_language_pack(wanted,progress=on_progress)
                except TranslationPreparationError:
                    status.update(state='error')
                    st.session_state['locale_preparation_failed']=wanted
                    st.error(t('locale_prepare_failed',lang))
                    return
                reload_locale_cache()
                if complete != total:
                    status.update(state='error')
                    st.session_state['locale_preparation_failed']=wanted
                    st.warning(t('locale_prepare_failed',lang))
                    return
                status.update(state='complete',expanded=False)
        # Switch only to a fully translated UI locale.
        st.session_state.pop('locale_preparation_failed',None)
        st.session_state["language_revision"] = st.session_state.get("language_revision", 0) + 1
        st.session_state["language"] = wanted
        if not guest and not admin and user:
            store.update_user_profile(user["id"], user["full_name"], wanted)
        st.rerun()
    if st.session_state.pop('legacy_locale_pending',None):
        st.info(t('locale_previous',lang))
    translated,total=locale_coverage(lang)
    if translated < total:
        # Legacy profiles from old releases can still hold a partial locale.
        st.warning(t('locale_prepare_failed','en'))
        st.caption(t('locale_progress','en',complete=translated,total=total))
    theme_now = st.toggle(
        t("sidebar_light_theme", lang),
        value=st.session_state.get("theme", "dark") == "light",
        key="guest_theme_toggle" if guest else "member_theme_toggle",
    )
    want_theme = "light" if theme_now else "dark"
    if st.session_state.get("theme", "dark") != want_theme:
        st.session_state["theme"] = want_theme
        st.rerun()


def guest_sidebar(lang):
    """Unauthenticated users see only purposeful, functioning navigation choices."""
    with st.sidebar:
        brand(lang)
        _sidebar_heading(t("sidebar_user_portal", lang), t("sidebar_user_portal_help", lang))
        _nav_button("user_login", "👤", t("guest_user_login", lang), guest=True)
        _nav_button("register", "✚", t("guest_register", lang), guest=True)

        _sidebar_heading(t("sidebar_admin_portal", lang), t("sidebar_admin_portal_help", lang))
        _nav_button("admin_login", "🛡", t("guest_admin_login", lang), guest=True)

        _sidebar_heading(t("sidebar_project", lang), t("sidebar_project_help", lang))
        _nav_button("about", "ⓘ", t("about", lang), guest=True)

        _sidebar_preferences(lang, guest=True)
        st.markdown(
            '<div class="sidebar-trust"><span class="sidebar-trust-mark">✚</span>'
            f'<div><b>Healthcare Info Assistant</b><small>{escape(t("sidebar_trust",lang))}</small></div></div>',
            unsafe_allow_html=True,
        )
    inject_css(st.session_state.get("theme", "dark"))


def _centered_submit(label):
    """Compact primary action centered inside a Streamlit form (desktop/mobile)."""
    _left, middle, _right = st.columns([0.8, 1.1, 0.8], gap="small")
    with middle:
        return st.form_submit_button(label, type="primary", width="stretch")


def _user_login(lang):
    with st.form("user_login_form"):
        username = st.text_input(t("field_username", lang), key="login_user_name", max_chars=80)
        password = st.text_input(t("field_password", lang), type="password")
        if _centered_submit(t("action_sign_in", lang)):
            account = login(username, password, role="user")
            if account:
                _session_start(account, preserve_selected_language=True)
            else:
                st.error(t("error_login", lang))


def _user_register(lang):
    st.caption(t("consent_intro", lang))
    with st.form("user_register_form"):
        n = st.text_input(t("field_full_name", lang), max_chars=120)
        u = st.text_input(t("field_choose_username", lang), max_chars=30)
        e = st.text_input(t("field_email", lang), max_chars=254)
        pw = st.text_input(t("field_new_password", lang), type="password")
        pw2 = st.text_input(t("field_confirm_password", lang), type="password")
        l = st.selectbox(t("field_preferred_language", lang), complete_locales(),
                         index=complete_locales().index(supported(lang)) if supported(lang) in complete_locales() else 0,
                         format_func=LANGUAGES.get, accept_new_options=False)
        consent = st.checkbox(t("field_consent", lang))
        if _centered_submit(t("action_create_account", lang)):
            if pw != pw2:
                st.error(t("error_password_mismatch", lang))
            else:
                try:
                    account = register_user(u, n, e, pw, consent, l)
                    _session_start(account)
                except AuthError as exc:
                    st.error(t("auth_error",lang))


def _admin_login(lang):
    st.info(t("admin_login_intro", lang).format(username=ADMIN_USERNAME))
    if ADMIN_SETUP == "needs_password":
        st.warning(t("admin_setup_warning",lang))
    elif ADMIN_SETUP == "invalid_config":
        st.error(t("admin_setup_invalid",lang) + ": " + ADMIN_ERROR)
    with st.form("admin_login_form"):
        admin_pw = st.text_input(t("field_admin_password", lang), type="password")
        if _centered_submit(t("action_admin_login", lang)):
            account = login(ADMIN_USERNAME, admin_pw, role="admin")
            if account:
                _session_start(account, preserve_selected_language=True)
            else:
                st.error(t("error_admin_login", lang))


def landing():
    lang = st.session_state.get("language", "en")
    lang = supported(lang)
    st.session_state.setdefault("guest_page", "user_login")
    if st.session_state["guest_page"] not in GUEST_PAGES:
        st.session_state["guest_page"] = "user_login"
    lang = _avoid_partial_legacy_locale(lang)
    guest_sidebar(lang)
    choice = st.session_state["guest_page"]
    if choice == "about":
        about_page(lang)
        footer(lang)
        return

    left, right = st.columns([1.15, 1], gap="large", vertical_alignment="top")
    with left:
        hero(language=lang, landing=True)
        st.markdown(
            f'<div class="auth-welcome"><span class="auth-heart">♡</span>'
            f'<div><b>{escape(t("guest_welcome_line", lang))}</b>'
            f'<p>{escape(t("guest_welcome_desc", lang))}</p></div></div>',
            unsafe_allow_html=True,
        )
    with right:
        if choice == "user_login":
            section(t("guest_user_login", lang), t("guest_user_login_desc", lang), t("sidebar_user_portal", lang))
            _user_login(lang)
        elif choice == "register":
            section(t("guest_register", lang), t("guest_register_desc", lang), t("sidebar_user_portal", lang))
            _user_register(lang)
        elif choice == "admin_login":
            section(t("guest_admin_login", lang), t("guest_admin_login_desc", lang), t("sidebar_admin_portal", lang))
            _admin_login(lang)
    st.markdown('<div class="auth-bottom-space"></div>', unsafe_allow_html=True)
    advisory(lang)
    footer(lang)


def sidebar(user, lang, admin=False):
    with st.sidebar:
        brand(lang)
        if admin:
            groups = [
                ("sidebar_admin_dashboard", "sidebar_admin_dashboard_help", [("overview", "◈")]),
                ("sidebar_management", "sidebar_management_help", [("users", "♧"), ("admin_reports", "▤"), ("conversations", "☰")]),
                ("sidebar_privacy", "sidebar_privacy_help", [("audit", "⌁")]),
            ]
        else:
            groups = [
                ("sidebar_workspace", "sidebar_workspace_help", [("home", "⌂")]),
                ("sidebar_assistance", "sidebar_assistance_help", [("chat", "◎"), ("reports", "▤"), ("voice", "♬")]),
                ("sidebar_your_health", "sidebar_your_health_help", [("history", "◷"), ("insights", "▥"), ("offline", "◉"), ("profile", "♙")]),
            ]
        for title_key, desc_key, options in groups:
            _sidebar_heading(t(title_key, lang), t(desc_key, lang))
            for page, icon in options:
                _nav_button(page, icon, v2t('offline_heading',lang) if page=='offline' else t(page, lang))
        _sidebar_heading(t("sidebar_project", lang), t("sidebar_project_help", lang))
        _nav_button("about", "ⓘ", t("about", lang))
        _sidebar_preferences(lang, guest=False, user=user, admin=admin)
        sidebar_user(user, lang)
        st.markdown('<div class="sidebar-logout-gap" aria-hidden="true"></div>',
                    unsafe_allow_html=True)
        _left, logout_center, _right = st.columns([0.26, 0.48, 0.26], gap="small")
        with logout_center:
            if st.button("⏻   " + t("logout", lang), key="logout", width="stretch"):
                _logout()
    inject_css(st.session_state.get("theme", "dark"))


def authenticated():
    identity = st.session_state.get("identity")
    if not identity:
        landing()
        return
    user = get_user(identity["user_id"])
    if not user or not user["is_active"] or user["role"] != identity["role"]:
        st.session_state.pop("identity", None)
        st.warning(t("session_expired",st.session_state.get("language","en")))
        landing()
        return
    admin = user["role"] == "admin"
    lang = st.session_state.get("language", user["language"])
    lang = supported(lang)
    lang = _avoid_partial_legacy_locale(lang)
    sidebar(user, lang, admin=admin)
    page = st.session_state.get("page", "overview" if admin else "home")
    if admin:
        actions = {
            "overview": admin_views.overview, "users": admin_views.users,
            "admin_reports": admin_views.reports, "conversations": admin_views.conversations,
            "audit": admin_views.audit,
        }
    else:
        actions = {
            "home": user_views.dashboard, "chat": user_views.chat,
            "reports": user_views.report_analyzer, "voice": user_views.voice_assistant,
            "history": user_views.history, "insights": user_views.insights,
            "offline": user_views.offline_readiness, "profile": user_views.profile,
        }
    if page == "about":
        about_page(lang)
    elif page in actions:
        actions[page](user, lang)
    else:
        st.session_state["page"] = "overview" if admin else "home"
        st.rerun()
    footer(lang)


if __name__ == "__main__":
    authenticated()
