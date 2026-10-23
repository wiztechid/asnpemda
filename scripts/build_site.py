#!/usr/bin/env python3
"""Build the public Cloudflare Pages site from an explicit allowlist.

Internal docs, research, pipeline code, candidate data, and unapproved draft pages
are never copied to the deploy artifact.
"""
from __future__ import annotations

import json
import html as html_utils
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BASE_FILES = (
    "index.html",
    "about.html",
    "editorial.html",
    "privacy.html",
    "disclaimer.html",
    "koreksi.html",
    "404.html",
    "favicon.svg",
    "favicon.ico",
    "robots.txt",
    "assets/site.css",
    "assets/article-engagement.js",
    "assets/author-suiza-ixan.webp",
    "assets/hero-sertifikasi-pbj-lkpp-2026.svg",
    "google3aabce049d4a051c.html",
)
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


FROZEN_MASTER_REQUIRED = ("article-page", "breadcrumbs", "article-content", "article-header", "article-hero", "status-card", "quick-answer", "toc", "article-body", "related-posts", "reader-engagement", "share-panel", "site-footer", "footer-grid")
FROZEN_MASTER_LEGACY = {"permenpanrb-9-2026-pppk-paruh-waktu", "pppk-paruh-waktu-penuh-waktu-2027"}


def validate_master_template(slug: str, content: str) -> None:
    if slug in FROZEN_MASTER_LEGACY:
        return
    missing = [name for name in FROZEN_MASTER_REQUIRED if name not in content]
    if missing:
        raise SystemExit(f"ERROR: {slug} diverges from FROZEN article master: {missing}")
    if content.count("<h1") != 1 or "article-engagement.js" not in content:
        raise SystemExit(f"ERROR: {slug} failed master template structural validation")


def published_articles() -> list[tuple[str, str | None, str | None]]:
    articles: list[tuple[str, str | None, str | None]] = []
    records = ROOT / "data" / "articles"
    if not records.exists():
        return articles
    for record_path in sorted(records.glob("*.json")):
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if record.get("approved") is not True or record.get("publicationState") != "PUBLISHED":
            continue
        slug = record.get("slug", "")
        if not SLUG_RE.fullmatch(slug):
            raise SystemExit(f"ERROR: invalid approved article slug in {record_path.name}")
        source = ROOT / "artikel" / f"{slug}.html"
        if not source.is_file():
            raise SystemExit(f"ERROR: approved article page is missing: {source.relative_to(ROOT)}")
        html = source.read_text(encoding="utf-8")
        if re.search(r"""<meta[^>]+name=["']robots["'][^>]+noindex""", html, re.I):
            raise SystemExit(f"ERROR: approved article is still marked noindex: {source.name}")
        validate_master_template(slug, html)
        hero_image = record.get("heroImage")
        if hero_image is not None:
            if not isinstance(hero_image, str) or not hero_image or hero_image.startswith("/"):
                raise SystemExit(f"ERROR: heroImage must be a repository-relative assets path: {source.name}")
            hero_path = Path(hero_image)
            if hero_path.is_absolute() or ".." in hero_path.parts or not hero_image.startswith("assets/") or hero_path.suffix.lower() != ".webp":
                raise SystemExit(f"ERROR: invalid approved article hero path: {hero_image}")
            hero_source = ROOT / hero_path
            if not hero_source.is_file():
                raise SystemExit(f"ERROR: approved article hero is missing: {hero_image}")
            with hero_source.open("rb") as image_file:
                header = image_file.read(12)
            if len(header) != 12 or header[:4] != b"RIFF" or header[8:12] != b"WEBP":
                raise SystemExit(f"ERROR: approved article hero is not a valid WebP: {hero_image}")
        articles.append((f"artikel/{slug}.html", record.get("dateModified"), hero_image))
    return articles



def add_article_blogroll(page: str, current: str, published: list[tuple[str, str | None, str | None]]) -> str:
    """Use one curated related-reading section with up to three published cards."""
    if 'class="related-posts"' not in page:
        return page
    candidates = []
    for relative, _, hero in reversed(published):
        if relative == current:
            continue
        source_html = (ROOT / relative).read_text(encoding="utf-8")
        title_match = re.search(r"<title>(.*?)</title>", source_html, re.I | re.S)
        title = html_utils.unescape(title_match.group(1).split(" — ASN Pemda")[0].strip()) if title_match else Path(relative).stem.replace("-", " ").title()
        picture = ('<img src="../' + html_utils.escape(hero, quote=True) + '" alt="" loading="lazy" decoding="async" width="360" height="203">') if hero else '<span class="blogroll-monogram" aria-hidden="true">ASN</span>'
        candidates.append('<a class="blogroll-card" href="' + html_utils.escape(Path(relative).name, quote=True) + '">' + picture + '<span class="blogroll-copy"><strong>' + html_utils.escape(title) + '</strong><span>Informasi dan penjelasan untuk ASN dan pemerintah daerah.</span><b>Baca artikel →</b></span></a>')
        if len(candidates) == 3:
            break
    if not candidates:
        return page
    start = page.find('<section class="related-posts"')
    if start < 0:
        return page
    # Replace the existing related block rather than adding a second block.
    end = page.find('</section>', start)
    if end < 0:
        return page
    end += len('</section>')
    block = '<section class="related-posts asn-blogroll" aria-labelledby="related-title"><div class="blogroll-heading"><span class="kicker">LANJUTKAN MEMBACA</span><h2 id="related-title">Bacaan selanjutnya</h2><p>Artikel lain yang sudah terbit di ASN Pemda.</p></div><div class="blogroll-grid">' + ''.join(candidates) + '</div><a class="blogroll-all" href="../index.html#artikel-terbaru">Lihat semua artikel →</a></section>'
    return page[:start] + block + page[end:]




def refresh_homepage_cards(home: str, articles: list[tuple[str, str | None, str | None]]) -> str:
    """Only approved articles appear; sort by publication date, maximum six."""
    approved = {Path(relative).stem: (relative, modified, hero) for relative, modified, hero in articles}
    card_re = re.compile(r'<article class="article-card"[\s\S]*?</article>')
    cards = {}
    for match in card_re.finditer(home):
        card = match.group(0)
        found = re.search(r'href="/artikel/([a-z0-9-]+)\.html"', card)
        if found and found.group(1) in approved:
            cards[found.group(1)] = card
    for slug, (relative, modified, hero) in approved.items():
        if slug in cards:
            continue
        body = (ROOT / relative).read_text(encoding="utf-8")
        title_match = re.search(r'<title>(.*?)</title>', body, re.I | re.S)
        title = html_utils.unescape(title_match.group(1).split(' — ASN Pemda')[0]) if title_match else slug.replace('-', ' ').title()
        description_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', body, re.I)
        description = html_utils.unescape(description_match.group(1)) if description_match else 'Informasi terbaru untuk ASN dan pemerintah daerah.'
        if not hero:
            hero_match = re.search(r'<figure[^>]*class="article-hero"[^>]*>[\s\S]*?<img[^>]*src="([^"]+)"', body, re.I)
            if hero_match:
                candidate = hero_match.group(1).replace('../', '').lstrip('/')
                if candidate.startswith('assets/') and (ROOT / candidate).is_file():
                    hero = candidate
        img = ('<img src="/' + html_utils.escape(hero, quote=True) + '" alt="" width="1200" height="675" loading="lazy">') if hero else '<span class="article-card-placeholder">ASN Pemda</span>'
        date = (modified or '')[:10]
        cards[slug] = '<article class="article-card"><a class="article-card-image" href="/' + relative + '">' + img + '</a><div class="article-card-body"><div class="article-card-meta"><span>' + html_utils.escape(date) + '</span></div><h3><a href="/' + relative + '">' + html_utils.escape(title) + '</a></h3><p>' + html_utils.escape(description[:150]) + '</p><a class="text-link" href="/' + relative + '">Baca artikel →</a></div></article>'
    ordered = sorted(cards, key=lambda slug: ((approved[slug][1] or '')[:10], slug), reverse=True)[:6]
    start = home.find('<div class="article-grid">')
    if start < 0:
        raise SystemExit('ERROR: homepage article grid missing')
    end = home.find('</div>\n</section>\n<section class="home-topics"', start)
    if end < 0:
        raise SystemExit('ERROR: homepage grid boundary missing')
    return home[:start] + '<div class="article-grid">\n' + '\n'.join(cards[slug] for slug in ordered) + '\n  ' + home[end:]


def main() -> None:
    config = json.loads((ROOT / "site-config.json").read_text(encoding="utf-8"))
    origin = config.get("siteUrl", "").rstrip("/")
    if not origin.startswith("https://") or "example" in origin:
        raise SystemExit("ERROR: set a valid HTTPS siteUrl before building")

    if DIST == ROOT or ROOT not in DIST.parents:
        raise SystemExit("ERROR: unsafe output directory")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    for relative in BASE_FILES:
        source = ROOT / relative
        if not source.is_file():
            raise SystemExit(f"ERROR: required public file missing: {relative}")
        target = DIST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    articles = published_articles()
    home_path = DIST / 'index.html'
    home_path.write_text(refresh_homepage_cards(home_path.read_text(encoding='utf-8'), articles), encoding='utf-8')
    for relative, _, hero_image in articles:
        target = DIST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        original = (ROOT / relative).read_text(encoding='utf-8')
        target.write_text(add_article_blogroll(original, relative, articles), encoding='utf-8')
        if hero_image:
            image_target = DIST / hero_image
            image_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / hero_image, image_target)

    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    urlset = ET.Element(f"{{{ns}}}urlset")
    for route in ("", "about.html", "editorial.html", "privacy.html", "disclaimer.html", "koreksi.html"):
        url = ET.SubElement(urlset, f"{{{ns}}}url")
        ET.SubElement(url, f"{{{ns}}}loc").text = f"{origin}/{route}"
    for relative, modified, _ in articles:
        url = ET.SubElement(urlset, f"{{{ns}}}url")
        ET.SubElement(url, f"{{{ns}}}loc").text = f"{origin}/{relative}"
        if modified:
            ET.SubElement(url, f"{{{ns}}}lastmod").text = modified
    ET.ElementTree(urlset).write(DIST / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    print(f"Public build complete: {len(BASE_FILES)} allowlisted files, {len(articles)} approved articles; output=dist/")


if __name__ == "__main__":
    main()
