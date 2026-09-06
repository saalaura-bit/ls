"""
test_06_i18n.py - Tests de sincronización EN/ES.
Proyecto: 001-portfolio-web
"""
import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from checks import check_i18n

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent


def get_html_files():
    return list(PROJECT_DIR.glob("*.html"))


class TestI18n:
    def test_en_es_count_match(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_i18n(content, f.name)
            count_issues = [i for i in issues if "Mismatch" in i["message"]]
            assert len(count_issues) == 0, f"{f.name}: {count_issues}"

    def test_no_untranslated_text(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_i18n(content, f.name)
            identical_issues = [i for i in issues if "identical" in i["message"].lower()]
            assert len(identical_issues) == 0, f"{f.name}: {identical_issues}"

    def test_language_toggle_button(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            assert 'id="langBtn"' in content or "langBtn" in content, \
                f"{f.name}: Missing language toggle button"
            assert "toggleLang" in content, f"{f.name}: Missing toggleLang function"

    def test_css_classes_en_es(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            en_count = len(re.findall(r'class="en"', content, re.IGNORECASE))
            es_count = len(re.findall(r'class="es"', content, re.IGNORECASE))
            assert en_count > 0, f"{f.name}: No .en elements"
            assert es_count > 0, f"{f.name}: No .es elements"

    def test_both_languages_have_content(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            en_elements = re.findall(r'class="en"[^>]*>(.*?)</', content, re.DOTALL | re.IGNORECASE)
            es_elements = re.findall(r'class="es"[^>]*>(.*?)</', content, re.DOTALL | re.IGNORECASE)
            assert len(en_elements) > 0, f"{f.name}: No EN content"
            assert len(es_elements) > 0, f"{f.name}: No ES content"
