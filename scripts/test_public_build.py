#!/usr/bin/env python3
"""Smoke-test the allowlisted public Cloudflare Pages artifact."""
import subprocess
import sys
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root / "scripts" / "build_site.py")], check=True)
dist = root / "dist"
required = {
    "index.html", "about.html", "editorial.html", "privacy.html", "disclaimer.html",
    "404.html", "koreksi.html", "favicon.svg", "favicon.ico", "robots.txt", "sitemap.xml",
    "assets/site.css", "assets/home-topic-filters.js", "assets/article-template.css", "assets/article-insights.css", "assets/author-suiza-ixan.webp", "google3aabce049d4a051c.html",
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
# Public calculators must match the frozen article navigation/footer shell while
# retaining their own calculation modules and print-friendly standalone UI.
for name, image in (
    ("kalkulator-spm-sp2d.html", "hero-kalkulator-potongan-spj-2026.webp"),
    ("kalkulator-pajak-ekatalog.html", "hero-pajak-ekatalog-penyedia-2026.webp"),
):
    page = (dist / name).read_text(encoding="utf-8")
    for marker in (
        '<header class="site-header">', '<footer class="site-footer">',
        'class="brand-icon"', 'class="shell footer-grid"', 'class="shell footer-bottom"',
        'class="skip-link"', 'class="breadcrumbs shell tool-breadcrumbs"',
        'class="shell tool-editorial"', 'href="/assets/article-template.css',
        '"@type":"WebApplication"',
        'name="twitter:card" content="summary_large_image"',
    ):
        if marker not in page:
            raise SystemExit(f"calculator site-shell missing {marker}: {name}")
    for slug in (
        "about", "editorial", "privacy", "disclaimer", "koreksi",
        "kalkulator-spm-sp2d", "kalkulator-pajak-ekatalog",
    ):
        # The public builder rewrites source .html links to clean Cloudflare URLs.
        if f'href="/{slug}"' not in page and f'href="/{slug}.html"' not in page:
            raise SystemExit(f"calculator site-shell missing link to {slug}: {name}")
    if page.count('<header class="site-header">') != 1 or page.count('<footer class="site-footer">') != 1:
        raise SystemExit("duplicate site shell in calculator: " + name)
    if 'og:image' not in page or image not in page or ("assets/" + image) not in actual:
        raise SystemExit("calculator hero/social image missing: " + name)
    if 'name="viewport"' not in page or 'rel="canonical"' not in page:
        raise SystemExit("calculator mobile/SEO metadata missing: " + name)
    if name == "kalkulator-spm-sp2d.html" and (
        'value="unknown">— Pilih sesuai invoice/dokumen —' not in page
        or 'Otomatis berdasar ambang umum' in page
    ):
        raise SystemExit("SPM calculator must require a document-confirmed PPN collector")
    if name == "kalkulator-pajak-ekatalog.html" and (
        'id="lsVatCollectorWrap"' not in page
        or 'Pemungut PPN pada invoice/dokumen LS' not in page
    ):
        raise SystemExit("E-Katalog LS calculator must ask who collects PPN")
print("CALCULATOR SHELL PASS: navigation, identity, policies, and footer match articles")

pension_page = (dist / "artikel" / "cara-menghitung-gaji-pensiun-pns.html").read_text(encoding="utf-8")
if '<a class="blogroll-card" href="sertifikasi-pbj-level-1-ppk-tipe-c-2026"><img src="../assets/hero-sertifikasi-pbj-lkpp-2026.svg"' not in pension_page:
    raise SystemExit("related PBJ article card does not use its matching hero image")
insights_css = (dist / "assets" / "article-insights.css").read_text(encoding="utf-8")
for token in (".article-page .article-body > h2", ".article-page .article-body > section[id]:not(.pension-calculator) > h2", "counter(article-section", "@media(max-width:650px)"):
    if token not in insights_css:
        raise SystemExit("frozen article heading template missing required feature: " + token)
if "POIN PENTING" in insights_css or "INFO PENTING" in insights_css:
    raise SystemExit("repeated heading label is not allowed in the frozen article template")
if ".article-page .article-body h2{" in insights_css:
    raise SystemExit("article widget headings must not inherit the numbered section style")
insights_link = '<link rel="stylesheet" href="../assets/article-insights.css?v=20261023-2">'
for article_file in sorted(path for path in actual if path.startswith("artikel/") and path.endswith(".html")):
    built_article = (dist / article_file).read_text(encoding="utf-8")
    source_article = (root / article_file).read_text(encoding="utf-8")
    if insights_link not in built_article:
        raise SystemExit("article is missing the heading highlights stylesheet: " + article_file)
    if built_article.count('href="../assets/article-template.css?v=20261023-1"') != 1 or re.search(r"<style\b", built_article, re.I):
        raise SystemExit("article does not use exactly one shared frozen stylesheet: " + article_file)
    if "class=\"fact-grid\"" in built_article:
        raise SystemExit("article uses the legacy fact-grid summary: " + article_file)
    if len(re.findall(r"""<section\b[^>]*class=["'][^"']*quick-answer[^"']*["']""", built_article, re.I)) != 1:
        raise SystemExit("article quick answer must use one semantic section: " + article_file)
    attrs = list(re.finditer(r"""class=["']([^"']*)["']""", built_article))
    classes = [(match.group(1).split(), match.start()) for match in attrs]
    module_order = ("article-page", "breadcrumbs", "article-content", "article-header", "article-hero", "status-card", "quick-answer", "takeaways", "toc", "article-body", "related-posts", "reader-engagement", "share-panel", "site-footer", "footer-grid")
    module_positions = []
    for module in module_order:
        matches = [position for names, position in classes if module in names]
        if len(matches) != 1:
            raise SystemExit("article must contain exactly one frozen module " + module + ": " + article_file)
        module_positions.append(matches[0])
    if module_positions != sorted(module_positions):
        raise SystemExit("article modules do not follow the frozen master order: " + article_file)
    ids = re.findall(r"""\bid=["']([^"']+)["']""", built_article, re.I)
    if len(ids) != len(set(ids)):
        raise SystemExit("article contains duplicate ids: " + article_file)
    toc = re.search(r"""<nav\b[^>]*class=["'][^"']*toc[^"']*["'][^>]*>([\s\S]*?)</nav>""", built_article, re.I)
    if not toc or any(target not in ids for target in re.findall(r"""href=["']#([^"']+)["']""", toc.group(1), re.I)):
        raise SystemExit("article table of contents contains a broken section link: " + article_file)
    takeaways = re.search(r"""<div\b[^>]*class=["'][^"']*takeaways[^"']*["'][^>]*>([\s\S]*?)</div>\s*<nav\b[^>]*class=["'][^"']*toc""", built_article, re.I)
    if not takeaways or len(re.findall(r"<div\b[^>]*>\s*<strong\b", takeaways.group(1), re.I)) != 3:
        raise SystemExit("article must have exactly three takeaway cards before the TOC: " + article_file)
    if len(re.findall(r"<h2\b", built_article, re.I)) != len(re.findall(r"<h2\b", source_article, re.I)):
        raise SystemExit("public build changed frozen article subheading count: " + article_file)
if "/artikel/pppk-paruh-waktu-penuh-waktu-2027" not in (dist / "index.html").read_text(encoding="utf-8"):
    raise SystemExit("homepage does not link to the published PPPK article")
home_html = (dist / "index.html").read_text(encoding="utf-8")
if 'property="og:image"' not in home_html or 'name="twitter:card" content="summary_large_image"' not in home_html:
    raise SystemExit("homepage social preview metadata missing")
if "assets/hero-aturan-wfh-asn-pemda-2026.webp" not in actual:
    raise SystemExit("homepage social preview image is not in the public build")
if 'data-topic-filter-grid' not in home_html or 'article-grid-count-' not in home_html:
    raise SystemExit("homepage topic filter grid metadata missing")
if 'assets/home-topic-filters.js' not in home_html:
    raise SystemExit("homepage topic filter script is not linked")
site_css = (dist / "assets" / "site.css").read_text(encoding="utf-8")
if "@media(max-width:600px){.site-header .brand small{display:none}}" not in site_css:
    raise SystemExit("mobile site header must hide the long brand tagline")
if 'Semua</button>' not in home_html or 'Pensiun & kesejahteraan' not in home_html:
    raise SystemExit("homepage topic filter controls missing or incomplete")
home_cards = re.findall(r'<article class="article-card"[^>]*data-topic="([^"]+)"', home_html)
if len(home_cards) != len(set(re.findall(r'href="/artikel/([a-z0-9-]+)"', home_html))):
    raise SystemExit("homepage card count does not match linked published article count")
pension_card = re.search(r'<article class="article-card"[^>]*data-topic="pensiun"[\s\S]*?</article>', home_html)
if not pension_card or "menit baca" not in pension_card.group(0) or "article-card-label" not in pension_card.group(0):
    raise SystemExit("generated pension card is missing its reading time or category label")
if not re.search(r'<span>\d{1,2} [A-Z][a-z]+ 2026</span>', pension_card.group(0)):
    raise SystemExit("generated pension card date is not localized")

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
if any(url.endswith(".html") for url in locations):
    raise SystemExit("sitemap contains Cloudflare Pages URLs that redirect from .html")
site_url = "https://asnpemda.pages.dev"
robots = (dist / "robots.txt").read_text(encoding="utf-8")
if f"Sitemap: {site_url}/sitemap.xml" not in robots.splitlines():
    raise SystemExit("robots.txt sitemap URL does not match the configured public origin")
for url in locations:
    relative = url.removeprefix(site_url + "/")
    if url == site_url + "/":
        relative = "index.html"
    page_path = dist / relative
    if not page_path.is_file() and (dist / (relative + ".html")).is_file():
        page_path = dist / (relative + ".html")
    if not page_path.is_file() or page_path.suffix.lower() != ".html":
        raise SystemExit(f"sitemap URL does not resolve to a public HTML page: {url}")
    page_html = page_path.read_text(encoding="utf-8")
    canonicals = re.findall(r'<link\b(?=[^>]*\brel=["\']canonical["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>', page_html, re.I)
    if len(canonicals) != 1 or canonicals[0] != url:
        raise SystemExit(f"canonical does not match sitemap URL: {url}")
    og_urls = re.findall(r'<meta\b(?=[^>]*\bproperty=["\']og:url["\'])(?=[^>]*\bcontent=["\']([^"\']+)["\'])[^>]*>', page_html, re.I)
    if len(og_urls) != 1 or og_urls[0] != url:
        raise SystemExit(f"Open Graph URL does not match sitemap URL: {url}")
    if relative.startswith("artikel/"):
        jsonld = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>', page_html, re.I)
        article_schemas = []
        for payload in jsonld:
            try:
                schema = json.loads(payload)
            except json.JSONDecodeError as error:
                raise SystemExit(f"invalid JSON-LD on {url}: {error}") from error
            if schema.get("@type") == "Article":
                article_schemas.append(schema)
        if len(article_schemas) != 1:
            raise SystemExit(f"expected one Article JSON-LD object: {url}")
        main_entity = article_schemas[0].get("mainEntityOfPage")
        if isinstance(main_entity, dict):
            main_entity = main_entity.get("@id") or main_entity.get("url")
        if main_entity != url or (article_schemas[0].get("url") and article_schemas[0]["url"] != url):
            raise SystemExit(f"Article JSON-LD URL does not match sitemap URL: {url}")
    if re.search(r'<meta\b(?=[^>]*\bname=["\']robots["\'])(?=[^>]*\bcontent=["\'][^"\']*noindex)[^>]*>', page_html, re.I):
        raise SystemExit(f"noindex page leaked into sitemap: {url}")
if any("gaji-asn-melalui-koperasi" in url for url in locations):
    raise SystemExit("unapproved draft article leaked into sitemap")
if "https://asnpemda.pages.dev/koreksi" not in locations:
    raise SystemExit("public correction page missing from sitemap")
if "https://asnpemda.pages.dev/artikel/pppk-paruh-waktu-penuh-waktu-2027" not in locations:
    raise SystemExit("published PPPK article missing from sitemap")
print("PUBLIC BUILD PASS: allowlist, draft exclusion, and sitemap verified")

smoke_record = root / "data" / "articles" / "ci-hero-smoke.json"
smoke_page = root / "artikel" / "ci-hero-smoke.html"
smoke_image = root / "assets" / "ci-hero-smoke.webp"
if smoke_record.exists() or smoke_page.exists() or smoke_image.exists():
    raise SystemExit("CI hero smoke fixture path already exists")
try:
    smoke_image.write_bytes((root / "assets" / "author-suiza-ixan.webp").read_bytes())
    smoke_page.write_text('<!doctype html><html><head><link rel="canonical" href="https://asnpemda.pages.dev/artikel/ci-hero-smoke"><link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/article-template.css"></head><body><main class="article-page"><nav class="breadcrumbs"></nav><article class="article-content"><header class="article-header"><h1>CI smoke</h1></header><figure class="article-hero"></figure><aside class="status-card"></aside><section class="quick-answer"><h2>Jawaban singkat</h2></section><div class="takeaways"><div><strong>Satu</strong><p>Ringkas</p></div><div><strong>Dua</strong><p>Ringkas</p></div><div><strong>Tiga</strong><p>Ringkas</p></div></div><nav class="toc"></nav><div class="article-body"></div><section class="related-posts"></section><section class="reader-engagement"></section><section class="share-panel"></section></article></main><footer class="site-footer"><div class="footer-grid"></div></footer><script src="../assets/article-engagement.js"></script></body></html>', encoding="utf-8")
    smoke_record.write_text('{"approved":true,"publicationState":"PUBLISHED","slug":"ci-hero-smoke","dateModified":"2026-10-20","heroImage":"assets/ci-hero-smoke.webp"}', encoding="utf-8")
    subprocess.run([sys.executable, str(root / "scripts" / "build_site.py")], check=True)
    if not (dist / "artikel" / "ci-hero-smoke.html").is_file():
        raise SystemExit("approved article fixture was not copied")
    if not (dist / "assets" / "ci-hero-smoke.webp").is_file():
        raise SystemExit("approved article hero was not copied")
    tree = ET.parse(dist / "sitemap.xml")
    locations = [node.text or "" for node in tree.findall(".//{*}loc")]
    if "https://asnpemda.pages.dev/artikel/ci-hero-smoke" not in locations:
        raise SystemExit("approved article fixture missing from sitemap")
finally:
    smoke_record.unlink(missing_ok=True)
    smoke_page.unlink(missing_ok=True)
    smoke_image.unlink(missing_ok=True)
subprocess.run([sys.executable, str(root / "scripts" / "build_site.py")], check=True)
print("ARTICLE HERO BUILD PASS: approved article and WebP asset copied together")

