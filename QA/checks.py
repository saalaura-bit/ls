"""
checks.py - Funciones de validación estática para proyectos web.
Proyecto: 001-portfolio-web
"""
import os
import re
from pathlib import Path
from html.parser import HTMLParser


class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.warnings = []
        self.tags = []
        self.has_doctype = False
        self.has_charset = False
        self.has_viewport = False
        self.has_lang = False
        self.lang_value = ""
        self.title = ""
        self.meta_description = ""
        self.meta_tags = {}
        self.links = []
        self.images = []
        self.scripts = []
        self.inline_styles = []
        self.current_tag = None
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.tag_stack.append(tag)

        if tag == "!doctype":
            self.has_doctype = True
        elif tag == "html":
            if "lang" in attrs_dict:
                self.has_lang = True
                self.lang_value = attrs_dict["lang"]
            else:
                self.errors.append("HTML tag missing lang attribute")
        elif tag == "meta":
            if attrs_dict.get("charset") or attrs_dict.get("http-equiv") == "Content-Type":
                self.has_charset = True
            if attrs_dict.get("name") == "viewport":
                self.has_viewport = True
                content = attrs_dict.get("content", "")
                if "width=device-width" not in content:
                    self.warnings.append("Viewport meta missing width=device-width")
            if attrs_dict.get("name") == "description":
                self.meta_description = attrs_dict.get("content", "")
            self.meta_tags[attrs_dict.get("name", attrs_dict.get("property", ""))] = attrs_dict.get("content", "")
        elif tag == "title":
            self.current_tag = "title"
        elif tag == "a":
            href = attrs_dict.get("href", "")
            self.links.append(href)
            if not attrs_dict.get("aria-label") and not attrs_dict.get("title"):
                text = self.get_text_context()
                if not text or len(text) < 3:
                    self.warnings.append(f"Link without aria-label or title: {href}")
        elif tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            self.images.append({"src": src, "alt": alt})
            if not alt:
                self.errors.append(f"Image without alt attribute: {src}")
        elif tag == "script":
            src = attrs_dict.get("src", "")
            if src:
                self.scripts.append(src)
        elif tag == "style":
            self.current_tag = "style"
        elif tag in ["div", "span", "p", "section", "article", "nav", "header", "footer", "main", "aside"]:
            if "role" in attrs_dict:
                pass  # Good accessibility
        elif tag == "input" or tag == "textarea" or tag == "select":
            if not attrs_dict.get("aria-label") and not attrs_dict.get("aria-labelledby"):
                self.warnings.append(f"Form element without aria-label: {tag}")

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        if tag == "title":
            self.current_tag = None

    def handle_data(self, data):
        if self.current_tag == "title":
            self.title += data.strip()

    def get_text_context(self):
        return ""

    def validate(self, html_content):
        self.feed(html_content)
        results = {
            "doctype": self.has_doctype,
            "charset": self.has_charset,
            "viewport": self.has_viewport,
            "lang": self.has_lang,
            "lang_value": self.lang_value,
            "title": self.title,
            "meta_description": self.meta_description,
            "meta_tags": self.meta_tags,
            "links": self.links,
            "images": self.images,
            "scripts": self.scripts,
            "errors": self.errors,
            "warnings": self.warnings,
        }
        return results


def check_html_structure(html_content, filename=""):
    """Valida la estructura HTML básica."""
    issues = []

    if "<!DOCTYPE" not in html_content.upper():
        issues.append({"severity": "error", "message": "Missing DOCTYPE declaration", "file": filename})

    if 'charset="UTF-8"' not in html_content and "charset=utf-8" not in html_content.lower():
        issues.append({"severity": "warning", "message": "Missing or non-standard charset declaration", "file": filename})

    if 'name="viewport"' not in html_content:
        issues.append({"severity": "error", "message": "Missing viewport meta tag", "file": filename})

    if 'lang="' not in html_content:
        issues.append({"severity": "error", "message": "Missing lang attribute on html tag", "file": filename})

    title_match = re.search(r"<title>(.*?)</title>", html_content, re.DOTALL | re.IGNORECASE)
    if not title_match:
        issues.append({"severity": "error", "message": "Missing <title> tag", "file": filename})
    elif not title_match.group(1).strip():
        issues.append({"severity": "warning", "message": "Empty <title> tag", "file": filename})

    unclosed_tags = re.findall(r"<(br|hr|img|input|meta|link)\b[^>]*>(?<!/>)", html_content, re.IGNORECASE)
    if unclosed_tags:
        issues.append({"severity": "info", "message": f"Self-closing tags found: {len(unclosed_tags)}", "file": filename})

    return issues


def check_seo(html_content, filename=""):
    """Valida elementos SEO."""
    issues = []

    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html_content, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta\s+content="([^"]*)"\s+name="description"', html_content, re.IGNORECASE)

    if not desc_match:
        issues.append({"severity": "error", "message": "Missing meta description", "file": filename})
    else:
        desc = desc_match.group(1)
        if len(desc) < 50:
            issues.append({"severity": "warning", "message": f"Meta description too short ({len(desc)} chars, min 50)", "file": filename})
        if len(desc) > 160:
            issues.append({"severity": "warning", "message": f"Meta description too long ({len(desc)} chars, max 160)", "file": filename})

    og_tags = ["og:title", "og:description", "og:image", "og:url", "og:type"]
    for tag in og_tags:
        if tag not in html_content:
            issues.append({"severity": "warning", "message": f"Missing Open Graph tag: {tag}", "file": filename})

    if "canonical" not in html_content.lower():
        issues.append({"severity": "info", "message": "No canonical link tag found", "file": filename})

    h1_count = len(re.findall(r"<h1\b", html_content, re.IGNORECASE))
    if h1_count == 0:
        issues.append({"severity": "error", "message": "No H1 tag found", "file": filename})
    elif h1_count > 1:
        issues.append({"severity": "warning", "message": f"Multiple H1 tags found ({h1_count})", "file": filename})

    return issues


def check_links(html_content, base_path, filename=""):
    """Valida links internos y externos."""
    issues = []
    link_pattern = re.compile(r'href="([^"]*)"', re.IGNORECASE)
    links = link_pattern.findall(html_content)

    for link in links:
        if link.startswith("#") or link.startswith("mailto:") or link.startswith("tel:"):
            continue
        if link.startswith("http://") or link.startswith("https://"):
            continue
        if link.startswith("javascript:"):
            continue

        link_path = base_path / link
        if not link_path.exists():
            issues.append({"severity": "error", "message": f"Broken internal link: {link}", "file": filename})

    return issues


def check_accessibility(html_content, filename=""):
    """Valida elementos de accesibilidad."""
    issues = []

    img_pattern = re.compile(r"<img\s[^>]*?>", re.IGNORECASE)
    images = img_pattern.findall(html_content)
    for img in images:
        if 'alt="' not in img.lower():
            src_match = re.search(r'src="([^"]*)"', img, re.IGNORECASE)
            src = src_match.group(1) if src_match else "unknown"
            issues.append({"severity": "error", "message": f"Image without alt text: {src}", "file": filename})

    if "<nav" in html_content.lower():
        nav_links = re.findall(r"<nav[^>]*>.*?</nav>", html_content, re.DOTALL | re.IGNORECASE)
        for nav in nav_links:
            if 'aria-label' not in nav.lower():
                issues.append({"severity": "warning", "message": "Navigation without aria-label", "file": filename})

    form_elements = re.findall(r"<(input|textarea|select)\b[^>]*>", html_content, re.IGNORECASE)
    for elem in form_elements:
        if 'aria-label' not in elem.lower() and 'aria-labelledby' not in elem.lower():
            issues.append({"severity": "warning", "message": f"Form element without label: {elem[:50]}...", "file": filename})

    return issues


def check_consistency(html_files, base_path):
    """Valida consistencia entre páginas."""
    issues = []
    nav_contents = []
    footer_contents = []

    for html_file in html_files:
        filepath = base_path / html_file
        if not filepath.exists():
            continue

        content = filepath.read_text(encoding="utf-8", errors="ignore")

        nav_match = re.search(r"<nav[^>]*>(.*?)</nav>", content, re.DOTALL | re.IGNORECASE)
        if nav_match:
            nav_text = re.sub(r"<[^>]+>", "", nav_match.group(1))
            nav_text = re.sub(r"\s+", " ", nav_text).strip()
            nav_contents.append((html_file, nav_text))

        footer_match = re.search(r"<footer[^>]*>(.*?)</footer>", content, re.DOTALL | re.IGNORECASE)
        if footer_match:
            footer_text = re.sub(r"<[^>]+>", "", footer_match.group(1))
            footer_text = re.sub(r"\s+", " ", footer_text).strip()
            footer_contents.append((html_file, footer_text))

    if nav_contents:
        first_nav = nav_contents[0][1]
        for fname, nav in nav_contents[1:]:
            if nav != first_nav:
                issues.append({"severity": "warning", "message": f"Navigation differs from other pages", "file": fname})

    if footer_contents:
        first_footer = footer_contents[0][1]
        for fname, footer in footer_contents[1:]:
            if footer != first_footer:
                issues.append({"severity": "info", "message": f"Footer content differs from other pages", "file": fname})

    return issues


def check_i18n(html_content, filename=""):
    """Valida sincronización EN/ES."""
    issues = []

    en_elements = re.findall(r'class="en"[^>]*>(.*?)</', html_content, re.DOTALL | re.IGNORECASE)
    es_elements = re.findall(r'class="es"[^>]*>(.*?)</', html_content, re.DOTALL | re.IGNORECASE)

    if len(en_elements) != len(es_elements):
        issues.append({
            "severity": "warning",
            "message": f"Mismatch EN/ES count: {len(en_elements)} EN vs {len(es_elements)} ES",
            "file": filename
        })

    en_texts = set()
    es_texts = set()
    for text in en_elements:
        clean = re.sub(r"<[^>]+>", "", text).strip()
        if clean:
            en_texts.add(clean)
    for text in es_elements:
        clean = re.sub(r"<[^>]+>", "", text).strip()
        if clean:
            es_texts.add(clean)

    for text in en_texts:
        if text in es_texts:
            issues.append({"severity": "warning", "message": f"Text identical in EN and ES: '{text[:50]}...'", "file": filename})

    return issues


def check_performance(html_content, filename=""):
    """Valida indicadores de performance."""
    issues = []

    if len(html_content) > 100000:
        issues.append({"severity": "warning", "message": f"Large HTML file ({len(html_content)} bytes)", "file": filename})

    inline_styles = re.findall(r'style="[^"]*"', html_content)
    if len(inline_styles) > 5:
        issues.append({"severity": "info", "message": f"Many inline styles found ({len(inline_styles)})", "file": filename})

    external_css = re.findall(r'<link[^>]*href="([^"]*\.css[^"]*)"', html_content, re.IGNORECASE)
    if len(external_css) > 3:
        issues.append({"severity": "info", "message": f"Many external CSS files ({len(external_css)})", "file": filename})

    external_js = re.findall(r'<script[^>]*src="([^"]*)"', html_content, re.IGNORECASE)
    if len(external_js) > 5:
        issues.append({"severity": "info", "message": f"Many external JS files ({len(external_js)})", "file": filename})

    return issues


def run_all_checks(project_path):
    """Ejecuta todos los checks contra un proyecto."""
    project_path = Path(project_path)
    all_issues = []

    html_files = list(project_path.glob("*.html"))
    if not html_files:
        return [{"severity": "error", "message": "No HTML files found in project", "file": ""}]

    for html_file in html_files:
        fname = html_file.name
        content = html_file.read_text(encoding="utf-8", errors="ignore")

        all_issues.extend(check_html_structure(content, fname))
        all_issues.extend(check_seo(content, fname))
        all_issues.extend(check_links(html_content=content, base_path=project_path, filename=fname))
        all_issues.extend(check_accessibility(content, fname))
        all_issues.extend(check_i18n(content, fname))
        all_issues.extend(check_performance(content, fname))

    all_issues.extend(check_consistency([f.name for f in html_files], project_path))

    return all_issues


def generate_summary(issues):
    """Genera un resumen de los issues encontrados."""
    summary = {
        "total": len(issues),
        "errors": len([i for i in issues if i["severity"] == "error"]),
        "warnings": len([i for i in issues if i["severity"] == "warning"]),
        "info": len([i for i in issues if i["severity"] == "info"]),
        "by_file": {},
        "by_category": {},
    }

    for issue in issues:
        fname = issue.get("file", "unknown")
        if fname not in summary["by_file"]:
            summary["by_file"][fname] = {"error": 0, "warning": 0, "info": 0}
        summary["by_file"][fname][issue["severity"]] += 1

    return summary
