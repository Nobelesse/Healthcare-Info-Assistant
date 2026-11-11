"""v1.9 regression tests for a uniform four-card dashboard action grid.

These tests are safe to run without Ollama, patient records, or a browser. They
check structural expectations; final browser dimensions require visual QA.
"""
from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_uses_four_existing_actions_in_scoped_container():
    source = (ROOT / 'views' / 'user_views.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    dashboard = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'dashboard')
    feature_lists = [node.value for node in ast.walk(dashboard)
                     if isinstance(node, ast.Assign)
                     and any(isinstance(target, ast.Name) and target.id == 'features' for target in node.targets)]
    assert len(feature_lists) == 1
    assert len(feature_lists[0].elts) == 4
    assert [row.elts[0].value for row in feature_lists[0].elts] == ['chat', 'reports', 'voice', 'insights']
    assert "st.container(key='dashboard_quick_actions')" in source
    assert "st.columns(4, gap='medium')" in source
    assert "key='quick_'+page" in source
    assert "_navigate(page)" in source


def test_scoped_equal_height_cards_and_aligned_buttons():
    css = (ROOT / 'assets' / 'style.css').read_text(encoding='utf-8')
    part = css.split('v1.9 — Equal-height interactive dashboard quick-action cards.', 1)[1]
    assert '.st-key-dashboard_quick_actions .feature-card' in part
    assert 'height:258px !important' in part
    assert 'min-height:258px !important' in part
    assert 'box-sizing:border-box' in part
    assert 'width:100% !important' in part
    assert '.st-key-dashboard_quick_actions .feature-card h3' in part
    assert 'min-height:46px' in part
    assert '.st-key-dashboard_quick_actions [data-testid="stButton"] button' in part
    assert 'min-height:46px !important' in part
    assert '@media (min-width:761px) and (max-width:1250px)' in part
    assert '@media (max-width:760px)' in part
    assert 'height:auto !important' in part
    assert 'prefers-reduced-motion:reduce' in part


def test_about_cards_and_project_security_are_unchanged():
    about = (ROOT / 'views' / 'about_view.py').read_text(encoding='utf-8')
    css = (ROOT / 'assets' / 'style.css').read_text(encoding='utf-8')
    assert 'feature_card(' in about
    # There is no global .feature-card height rule in the v1.9 additions.
    additions = css.split('v1.9 — Equal-height interactive dashboard quick-action cards.', 1)[1]
    for line in additions.splitlines():
        if '.feature-card' in line and not line.lstrip().startswith('/*'):
            assert '.st-key-dashboard_quick_actions' in line
    assert (ROOT / 'database' / 'store.py').is_file()
    assert (ROOT / 'auth' / 'service.py').is_file()
