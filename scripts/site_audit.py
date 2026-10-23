#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlsplit
import json
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
records = {}
for record_path in sorted((root / "data" / "articles").glob("*.json")):
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
        records[record.get("slug", "")] = record
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{record_path.relative_to(root)} invalid article record: {error}")

for page in sorted(root.rglob("*.html")):
    text = page.read_text(encoding="utf-8")
    # Google verification HTML files intentionally contain one exact plaintext token line.
    if page.parent == root and page.name.startswith("google") and text.strip() == f"google-site-verification: {page.name}":
        continue
    for tag in ("<html", "<title>", '<meta name="viewport"', "</html>"):
        if tag not in text:
            errors.append(f"{page.relative_to(root)} missing {tag}")
    if page.parts[-2:-1] == ("artikel",):
        slug = page.stem
        record = records.get(slug, {})
        published = record.get("approved") is True and record.get("publicationState") == "PUBLISHED"
        has_noindex = bool(re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', text, re.I))
        if published and has_noindex:
            errors.append(f"{page.relative_to(root)} published page still has noindex")
        if not published and not has_noindex:
            errors.append(f"{page.relative_to(root)} draft missing noindex")
    for link in re.findall(r'href=["\']([^"\']+)["\']', text):
        if link.startswith(("https:", "http:", "mailto:", "tel:", "javascript:", "#")):
            continue
        path_part = urlsplit(link).path
        if not path_part:
            continue
        target = ((root / path_part.lstrip("/")) if path_part.startswith("/") else (page.parent / path_part)).resolve()
        if not target.is_relative_to(root) or not target.exists():
            errors.append(f"{page.relative_to(root)} broken local link: {link}")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("SITE AUDIT PASS")
