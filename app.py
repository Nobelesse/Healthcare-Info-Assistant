"""Healthcare Info Assistant entrypoint: local-first, bilingual, premium Streamlit UI."""
from html import escape
import streamlit as st
from auth.service import AuthError, register_user, login, bootstrap_admin
from config.settings import APP_NAME, ADMIN_USERNAME
from database.store import initialize_database, get_user
from database import store
from ui.components import inject_css, brand, sidebar_user, footer, hero, section, advisory
from ui.strings import t
from pages import user_views, admin_views
from pages.about_view import about_page

st.set_page_config(page_title="Healthcare Info Assistant | Medical AI", page_icon="🩺", layout="wide", initial_sidebar_state="expanded")
initialize_database()
try:
    ADMIN_SETUP = bootstrap_admin()
except AuthError as e:
    ADMIN_SETUP = "invalid_config"
    ADMIN_ERROR = str(e)


def _session_start(user):
    st.session_state["identity"] = {"user_id":user["id"],"role":user["role"]}
    st.session_state["language"] = user["language"]
    st.session_state["page"] = "overview" if user["role"] == "admin" else "home"
    st.rerun()


def _logout():
    st.session_state.clear()
    st.rerun()


def landing():
    inject_css(st.session_state.get("theme","dark"))
    st.markdown("<div style='height:3px'></div>", unsafe_allow_html=True)
    hero(landing=True)
    st.write("")
    section("Secure access to your healthspace", "Create a user account, sign in, or access the permanent administrator console.", "WELCOME TO THE FUTURE")
    a,b,c=st.tabs(["👤 User Login","✦ Create User Account","🛡️ Admin Login"])
    with a:
        with st.form("user_login_form"):
            username=st.text_input("Username",key="login_user_name",max_chars=80)
            password=st.text_input("Password",type="password")
            if st.form_submit_button("Sign in",type="primary",use_container_width=True):
                account=login(username,password,role="user")
                if account:
                    _session_start(account)
                else:
                    st.error("Invalid credentials or disabled user account.")
    with b:
        st.caption("Your administrator can access stored reports and conversations. Please read the consent checkbox carefully.")
        with st.form("user_register_form"):
            n=st.text_input("Full name",max_chars=120)
            u=st.text_input("Choose username",max_chars=30)
            e=st.text_input("Email address",max_chars=254)
            pw=st.text_input("Password (10+ characters, letters and numbers)",type="password")
            pw2=st.text_input("Confirm password",type="password")
            l=st.selectbox("Preferred language",["English","हिंदी"])
            consent=st.checkbox("I understand and consent that the permanent administrator 'Mr. Doc' can access my account details, stored medical report text, AI responses and conversation history. The app is for educational use, not confidential clinical care.")
            if st.form_submit_button("Create my account",type="primary",use_container_width=True):
                if pw != pw2:
                    st.error("Passwords do not match.")
                else:
                    try:
                        account=register_user(u,n,e,pw,consent,lang_to_code(l))
                        _session_start(account)
                    except AuthError as exc:
                        st.error(str(exc))
    with c:
        st.markdown(f"**Permanent administrator:** `{ADMIN_USERNAME}` — no public admin registration.")
        if ADMIN_SETUP == "needs_password":
            st.warning("Admin not initialized. Set ADMIN_INITIAL_PASSWORD in .env and run `python -m scripts.init_admin`, then restart Streamlit.")
        elif ADMIN_SETUP == "invalid_config":
            st.error(f"Invalid admin setup: {ADMIN_ERROR}")
        with st.form("admin_login_form"):
            admin_pw=st.text_input("Admin password",type="password")
            if st.form_submit_button("Open admin console",type="primary",use_container_width=True):
                account=login(ADMIN_USERNAME,admin_pw,role="admin")
                if account:
                    _session_start(account)
                else:
                    st.error("Incorrect admin password or administrator not initialized.")
    st.write("")
    advisory("en")
    footer()


def lang_to_code(choice):
    return "hi" if choice=="हिंदी" else "en"


def sidebar(user, lang, admin=False):
    with st.sidebar:
        brand()
        if admin:
            options=[("overview","◈"),("users","♧"),("admin_reports","▤"),("conversations","☰"),("audit","⌁"),("about","ⓘ")]
        else:
            options=[("home","⌂"),("chat","◎"),("reports","▤"),("voice","♬"),("history","◷"),
                     ("insights","▥"),("profile","♙"),("about","ⓘ")]
        st.caption("ADMIN CONSOLE" if admin else "NAVIGATION")
        for name, icon in options:
            label = f"{icon}   {t(name,lang)}"
            if st.button(label,key=f"nav_{name}",use_container_width=True,
                         type="primary" if st.session_state.get("page")==name else "secondary"):
                st.session_state["page"]=name
                st.rerun()
        st.divider()
        selected=st.selectbox("Language / भाषा",["English","हिंदी"],index=0 if lang=="en" else 1,key="ui_language")
        wanted=lang_to_code(selected)
        if wanted!=lang:
            st.session_state["language"]=wanted
            if not admin:
                store.update_user_profile(user["id"],user["full_name"],wanted)
            st.rerun()
        theme_now=st.toggle("☼ Light theme",value=st.session_state.get("theme","dark")=="light",key="theme_control")
        want_theme="light" if theme_now else "dark"
        if st.session_state.get("theme","dark") != want_theme:
            st.session_state["theme"]=want_theme
            st.rerun()
        sidebar_user(user,lang)
        if st.button("⏻  "+t("logout",lang),key="logout",use_container_width=True):
            _logout()
    inject_css(st.session_state.get("theme","dark"))


def authenticated():
    identity=st.session_state.get("identity")
    if not identity:
        landing()
        return
    user=get_user(identity["user_id"])
    if not user or not user["is_active"] or user["role"]!=identity["role"]:
        st.session_state.pop("identity",None)
        st.warning("Your session has ended, or your account has been disabled. Please log in again.")
        landing()
        return
    admin = user["role"]=="admin"
    lang=st.session_state.get("language",user["language"])
    if lang not in {"en","hi"}:lang="en"
    sidebar(user,lang,admin=admin)
    page=st.session_state.get("page","overview" if admin else "home")
    if admin:
        actions={"overview":admin_views.overview,"users":admin_views.users,"admin_reports":admin_views.reports,
                 "conversations":admin_views.conversations,"audit":admin_views.audit}
    else:
        actions={"home":user_views.dashboard,"chat":user_views.chat,"reports":user_views.report_analyzer,
                 "voice":user_views.voice_assistant,"history":user_views.history,
                 "insights":user_views.insights,"profile":user_views.profile}
    if page=="about":
        about_page(lang)
    elif page in actions:
        actions[page](user,lang)
    else:
        st.session_state["page"]="overview" if admin else "home"
        st.rerun()
    footer()


if __name__=="__main__":
    authenticated()
