#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlsplit
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
for page in sorted(root.rglob("*.html")):
    text = page.read_text(encoding="utf-8")
    for tag in ("<html", "<title>", '<meta name="viewport"', "</html>"):
        if tag not in text:
            errors.append(f"{page.relative_to(root)} missing {tag}")
    if page.parts[-2:-1] == ("artikel",) and "noindex" not in text:
        errors.append(f"{page.relative_to(root)} draft missing noindex")
    for link in re.findall(r'href=["\']([^"\']+)["\']', text):
        if link.startswith(("https:", "http:", "mailto:", "tel:", "javascript:", "#")):
            continue
        path = urlsplit(link).path
        if not path:
            continue
        target = ((root / path.lstrip("/")) if path.startswith("/") else (page.parent / path)).resolve()
        if not target.is_relative_to(root) or not target.exists():
            errors.append(f"{page.relative_to(root)} broken local link: {link}")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("SITE AUDIT PASS")
