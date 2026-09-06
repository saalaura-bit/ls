"""
test_03_links.py - Tests de links.
Proyecto: 001-portfolio-web
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from checks import check_links

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent


def get_html_files():
    return list(PROJECT_DIR.glob("*.html"))


class TestLinks:
    def test_all_internal_links_valid(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_links(html_content=content, base_path=PROJECT_DIR, filename=f.name)
            broken = [i for i in issues if i["severity"] == "error"]
            assert len(broken) == 0, f"{f.name}: {broken}"

    def test_links_have_aria_label(self):
        import re
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            links = re.findall(r'<a\s[^>]*href="([^"]*)"[^>]*>', content, re.IGNORECASE)
            for link in links:
                if link.startswith("#") or link.startswith("mailto:") or link.startswith("tel:"):
                    continue
                if link.startswith("http"):
                    continue
                link_line = content[content.index(link):content.index(link)+200]
                assert 'aria-label="' in link_line or 'title="' in link_line, \
                    f"{f.name}: Link {link} missing aria-label/title"

    def test_no_javascript_links(self):
        import re
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            js_links = re.findall(r'href="javascript:', content, re.IGNORECASE)
            assert len(js_links) == 0, f"{f.name}: javascript: links found"
