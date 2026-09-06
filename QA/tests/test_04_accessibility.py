"""
test_04_accessibility.py - Tests de accesibilidad.
Proyecto: 001-portfolio-web
"""
import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from checks import check_accessibility

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent


def get_html_files():
    return list(PROJECT_DIR.glob("*.html"))


class TestAccessibility:
    def test_images_have_alt(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_accessibility(content, f.name)
            alt_issues = [i for i in issues if "alt" in i["message"].lower() and i["severity"] == "error"]
            assert len(alt_issues) == 0, f"{f.name}: {alt_issues}"

    def test_nav_has_aria_label(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            navs = re.findall(r"<nav[^>]*>.*?</nav>", content, re.DOTALL | re.IGNORECASE)
            for nav in navs:
                assert 'aria-label' in nav.lower(), f"{f.name}: Nav without aria-label"

    def test_semantic_html(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            assert "<nav" in content.lower(), f"{f.name}: No <nav> element"
            assert "<footer" in content.lower(), f"{f.name}: No <footer> element"
            assert "<header" in content.lower() or "<section" in content.lower(), \
                f"{f.name}: No <header> or <section> element"

    def test_svg_have_title(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            svgs = re.findall(r"<svg[^>]*>.*?</svg>", content, re.DOTALL | re.IGNORECASE)
            for svg in svgs:
                has_aria = 'aria-label' in svg.lower() or 'aria-hidden' in svg.lower() or '<title' in svg.lower()
                assert has_aria, f"{f.name}: SVG without accessibility attributes"

    def test_lang_attribute_value(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r'<html\s+lang="([^"]*)"', content, re.IGNORECASE)
            assert match, f"{f.name}: No lang attribute"
            lang = match.group(1)
            assert lang in ["en", "es"], f"{f.name}: Invalid lang value: {lang}"
