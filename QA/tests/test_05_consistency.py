"""
test_05_consistency.py - Tests de consistencia entre páginas.
Proyecto: 001-portfolio-web
"""
import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from checks import check_consistency

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent


def get_html_files():
    return [f.name for f in PROJECT_DIR.glob("*.html")]


class TestConsistency:
    def test_navigation_identical(self):
        files = get_html_files()
        nav_contents = []
        for fname in files:
            content = (PROJECT_DIR / fname).read_text(encoding="utf-8", errors="ignore")
            nav_match = re.search(r"<nav[^>]*>(.*?)</nav>", content, re.DOTALL | re.IGNORECASE)
            if nav_match:
                nav_text = re.sub(r"<[^>]+>", "", nav_match.group(1))
                nav_text = re.sub(r"\s+", " ", nav_text).strip()
                nav_contents.append((fname, nav_text))

        if nav_contents:
            first_nav = nav_contents[0][1]
            for fname, nav in nav_contents[1:]:
                assert nav == first_nav, f"{fname}: Navigation differs from other pages"

    def test_footer_branding(self):
        files = get_html_files()
        for fname in files:
            content = (PROJECT_DIR / fname).read_text(encoding="utf-8", errors="ignore")
            assert "Maria Laura Saavedra" in content, f"{fname}: Missing name in footer"
            assert "Montevideo, Uruguay" in content, f"{fname}: Missing location in footer"

    def test_logo_links_to_index(self):
        files = get_html_files()
        for fname in files:
            content = (PROJECT_DIR / fname).read_text(encoding="utf-8", errors="ignore")
            logo_match = re.search(r'class="logo"[^>]*href="([^"]*)"', content)
            if logo_match:
                assert logo_match.group(1) == "index.html", \
                    f"{fname}: Logo doesn't link to index.html"

    def test_contact_links(self):
        files = get_html_files()
        for fname in files:
            content = (PROJECT_DIR / fname).read_text(encoding="utf-8", errors="ignore")
            assert "saalaura@gmail.com" in content, f"{fname}: Missing email"
            assert "+59897496335" in content or "598 97 496 335" in content, \
                f"{fname}: Missing phone"
            assert "linkedin.com/in/maria-laura-saavedra" in content, \
                f"{fname}: Missing LinkedIn"

    def test_privacy_link_exists(self):
        files = get_html_files()
        for fname in files:
            content = (PROJECT_DIR / fname).read_text(encoding="utf-8", errors="ignore")
            assert "privacy.html" in content, f"{fname}: Missing privacy link"

    def test_float_nav_exists(self):
        files = get_html_files()
        for fname in files:
            content = (PROJECT_DIR / fname).read_text(encoding="utf-8", errors="ignore")
            assert 'class="float-nav"' in content, f"{fname}: Missing float nav"
            assert 'class="float-toggle"' in content, f"{fname}: Missing float toggle"
