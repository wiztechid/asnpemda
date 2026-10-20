#!/usr/bin/env python3
"""Smoke-test the allowlisted public Cloudflare Pages artifact."""
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root / "scripts" / "build_site.py")], check=True)
dist = root / "dist"
required = {
    "index.html", "about.html", "editorial.html", "privacy.html", "disclaimer.html",
    "404.html", "favicon.svg", "favicon.ico", "robots.txt", "sitemap.xml",
    "assets/site.css", "assets/author-suiza-ixan.webp",
}
actual = {p.relative_to(dist).as_posix() for p in dist.rglob("*") if p.is_file()}
missing = required - actual
if missing:
    raise SystemExit("missing public files: " + ", ".join(sorted(missing)))
blocked = [p for p in actual if p.startswith(("docs/", "research/", "data/", "scripts/", "schemas/"))]
if blocked:
    raise SystemExit("internal/source files leaked into dist: " + ", ".join(sorted(blocked)))
if "artikel/gaji-asn-melalui-koperasi.html" in actual:
    raise SystemExit("unapproved draft article leaked into dist")
for page in ("index.html", "about.html", "editorial.html", "privacy.html", "disclaimer.html", "404.html"):
    html = (dist / page).read_text(encoding="utf-8")
    if '<img class="brand-icon" src="/favicon.svg?v=' not in html:
        raise SystemExit(f"{page} brand mark does not reuse the favicon")
index = (dist / "index.html").read_text(encoding="utf-8")
if "/artikel/gaji-asn-melalui-koperasi.html" in index:
    raise SystemExit("homepage links to an unapproved draft article")
tree = ET.parse(dist / "sitemap.xml")
locations = [node.text or "" for node in tree.findall(".//{*}loc")]
if any("gaji-asn-melalui-koperasi" in url for url in locations):
    raise SystemExit("unapproved draft article leaked into sitemap")
print("PUBLIC BUILD PASS: allowlist, draft exclusion, and sitemap verified")
