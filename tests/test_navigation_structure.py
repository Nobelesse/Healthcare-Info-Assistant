"""Regression checks: internal view modules must not be browser-routable pages."""
import ast
from pathlib import Path
from ui.strings import t

ROOT = Path(__file__).resolve().parents[1]


def test_internal_views_not_auto_registered_as_streamlit_pages():
    assert not list((ROOT / "pages").glob("*.py"))
    for name in ("user_views", "admin_views", "about_view"):
        assert (ROOT / "views" / f"{name}.py").is_file()


def test_app_uses_explicit_guest_sidebar_and_role_aware_dispatch():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    tree = ast.parse(app)
    assert any(isinstance(n, ast.ImportFrom) and n.module == "views" for n in tree.body)
    assert not any(isinstance(n, ast.ImportFrom) and n.module == "pages" for n in tree.body)
    functions = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert {"guest_sidebar", "sidebar", "_user_login", "_user_register", "_admin_login", "authenticated"} <= functions
    assert "GUEST_PAGES" in app
    assert "st.tabs(" not in app  # Guest account choices have moved into the sidebar.


def test_guest_navigation_labels_exist_in_both_languages():
    for language in ("en", "hi"):
        for key in (
            "sidebar_user_portal", "sidebar_user_portal_help",
            "sidebar_admin_portal", "sidebar_admin_portal_help",
            "sidebar_project", "sidebar_project_help",
            "guest_user_login", "guest_register", "guest_admin_login",
            "field_consent", "field_admin_password",
        ):
            assert t(key, language) != key


def test_single_page_client_navigation_configuration():
    content = (ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8")
    assert "showSidebarNavigation = false" in content
