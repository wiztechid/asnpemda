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
    "404.html", "koreksi.html", "favicon.svg", "favicon.ico", "robots.txt", "sitemap.xml",
    "assets/site.css", "assets/author-suiza-ixan.webp", "google3aabce049d4a051c.html",
}
actual = {p.relative_to(dist).as_posix() for p in dist.rglob("*") if p.is_file()}
missing = required - actual
if missing:
    raise SystemExit("missing public files: " + ", ".join(sorted(missing)))
verification_file = dist / "google3aabce049d4a051c.html"
if verification_file.read_text(encoding="utf-8") != "google-site-verification: google3aabce049d4a051c.html":
    raise SystemExit("Google Search Console verification file missing or altered in public build")
blocked = [p for p in actual if p.startswith(("docs/", "research/", "data/", "scripts/", "schemas/"))]
if blocked:
    raise SystemExit("internal/source files leaked into dist: " + ", ".join(sorted(blocked)))
if "artikel/gaji-asn-melalui-koperasi.html" in actual:
    raise SystemExit("unapproved draft article leaked into dist")
published_path = "artikel/pppk-paruh-waktu-penuh-waktu-2027.html"
if published_path not in actual:
    raise SystemExit("approved PPPK article missing from public build")
published_html = (dist / published_path).read_text(encoding="utf-8")
if '<meta name="robots" content="index,follow">' not in published_html:
    raise SystemExit("published PPPK article is not indexable")
if "/assets/hero-pppk-paruh-waktu-2027.webp" not in published_html:
    raise SystemExit("published PPPK article hero reference missing")
if "assets/hero-pppk-paruh-waktu-2027.webp" not in actual:
    raise SystemExit("published PPPK article hero missing from public build")
if "/artikel/pppk-paruh-waktu-penuh-waktu-2027.html" not in (dist / "index.html").read_text(encoding="utf-8"):
    raise SystemExit("homepage does not link to the published PPPK article")
for page in ("index.html", "about.html", "editorial.html", "privacy.html", "disclaimer.html", "koreksi.html", "404.html"):
    html = (dist / page).read_text(encoding="utf-8")
    if '<img class="brand-icon" src="/favicon.svg?v=' not in html:
        raise SystemExit(f"{page} brand mark does not reuse the favicon")
index = (dist / "index.html").read_text(encoding="utf-8")
if "/artikel/gaji-asn-melalui-koperasi.html" in index:
    raise SystemExit("homepage links to an unapproved draft article")
tree = ET.parse(dist / "sitemap.xml")
locations = [node.text or "" for node in tree.findall(".//{*}loc")]
if len(locations) != len(set(locations)):
    raise SystemExit("sitemap contains duplicate URLs")
site_url = "https://asnpemda.pages.dev"
robots = (dist / "robots.txt").read_text(encoding="utf-8")
if f"Sitemap: {site_url}/sitemap.xml" not in robots.splitlines():
    raise SystemExit("robots.txt sitemap URL does not match the configured public origin")
for url in locations:
    relative = url.removeprefix(site_url + "/")
    if url == site_url + "/":
        relative = "index.html"
    page_path = dist / relative
    if not page_path.is_file() or page_path.suffix.lower() != ".html":
        raise SystemExit(f"sitemap URL does not resolve to a public HTML page: {url}")
    page_html = page_path.read_text(encoding="utf-8")
    canonicals = re.findall(r'<link\\b(?=[^>]*\\brel=["\\']canonical["\\'])(?=[^>]*\\bhref=["\\']([^"\\']+)["\\'])[^>]*>', page_html, re.I)
    if len(canonicals) != 1 or canonicals[0] != url:
        raise SystemExit(f"canonical does not match sitemap URL: {url}")
    if re.search(r'<meta\\b(?=[^>]*\\bname=["\\']robots["\\'])(?=[^>]*\\bcontent=["\\'][^"\\']*noindex)[^>]*>', page_html, re.I):
        raise SystemExit(f"noindex page leaked into sitemap: {url}")
if any("gaji-asn-melalui-koperasi" in url for url in locations):
    raise SystemExit("unapproved draft article leaked into sitemap")
if "https://asnpemda.pages.dev/koreksi.html" not in locations:
    raise SystemExit("public correction page missing from sitemap")
if "https://asnpemda.pages.dev/artikel/pppk-paruh-waktu-penuh-waktu-2027.html" not in locations:
    raise SystemExit("published PPPK article missing from sitemap")
print("PUBLIC BUILD PASS: allowlist, draft exclusion, and sitemap verified")

smoke_record = root / "data" / "articles" / "ci-hero-smoke.json"
smoke_page = root / "artikel" / "ci-hero-smoke.html"
smoke_image = root / "assets" / "ci-hero-smoke.webp"
if smoke_record.exists() or smoke_page.exists() or smoke_image.exists():
    raise SystemExit("CI hero smoke fixture path already exists")
try:
    smoke_image.write_bytes((root / "assets" / "author-suiza-ixan.webp").read_bytes())
    smoke_page.write_text('<!doctype html><html><head><link rel="canonical" href="https://asnpemda.pages.dev/artikel/ci-hero-smoke.html"></head><body><main class="article-page"><nav class="breadcrumbs"></nav><article class="article-content"><header class="article-header"><h1>CI smoke</h1></header><figure class="article-hero"></figure><aside class="status-card"></aside><section class="quick-answer"></section><nav class="toc"></nav><div class="article-body"></div><section class="related-posts"></section><section class="reader-engagement"></section><section class="share-panel"></section></article></main><footer class="site-footer"><div class="footer-grid"></div></footer><script src="../assets/article-engagement.js"></script></body></html>', encoding="utf-8")
    smoke_record.write_text('{"approved":true,"publicationState":"PUBLISHED","slug":"ci-hero-smoke","dateModified":"2026-10-20","heroImage":"assets/ci-hero-smoke.webp"}', encoding="utf-8")
    subprocess.run([sys.executable, str(root / "scripts" / "build_site.py")], check=True)
    if not (dist / "artikel" / "ci-hero-smoke.html").is_file():
        raise SystemExit("approved article fixture was not copied")
    if not (dist / "assets" / "ci-hero-smoke.webp").is_file():
        raise SystemExit("approved article hero was not copied")
    tree = ET.parse(dist / "sitemap.xml")
    locations = [node.text or "" for node in tree.findall(".//{*}loc")]
    if "https://asnpemda.pages.dev/artikel/ci-hero-smoke.html" not in locations:
        raise SystemExit("approved article fixture missing from sitemap")
finally:
    smoke_record.unlink(missing_ok=True)
    smoke_page.unlink(missing_ok=True)
    smoke_image.unlink(missing_ok=True)
subprocess.run([sys.executable, str(root / "scripts" / "build_site.py")], check=True)
print("ARTICLE HERO BUILD PASS: approved article and WebP asset copied together")

