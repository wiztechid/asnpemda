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
    "assets/home-topic-filters.js",
    "assets/article-template.css",
    "assets/article-insights.css",
    "assets/article-engagement.js",
    "assets/author-suiza-ixan.webp",
    "assets/hero-sertifikasi-pbj-lkpp-2026.svg",
    "google3aabce049d4a051c.html",
)
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


FROZEN_MASTER_SEQUENCE = (
    "article-page", "breadcrumbs", "article-content", "article-header", "article-hero",
    "status-card", "quick-answer", "takeaways", "toc", "article-body", "related-posts",
    "reader-engagement", "share-panel", "site-footer", "footer-grid",
)
FROZEN_MASTER_REQUIRED = FROZEN_MASTER_SEQUENCE


def class_matches(content: str, name: str) -> list[re.Match[str]]:
    return list(re.finditer(r'class=["\\'][^"\\']*(?:^|\\s)' + re.escape(name) + r'(?:\\s|$)[^"\\']*["\\']', content))


def validate_master_template(slug: str, content: str) -> None:
    missing = [name for name in FROZEN_MASTER_REQUIRED if len(class_matches(content, name)) != 1]
    if missing:
        raise SystemExit(f"ERROR: {slug} must contain exactly one of each frozen article module: {missing}")
    if content.count("<h1") != 1 or "article-engagement.js" not in content:
        raise SystemExit(f"ERROR: {slug} failed frozen article template structural validation")
    if re.search(r"<style\\b", content, re.I):
        raise SystemExit(f"ERROR: {slug} contains inline CSS; use the shared frozen article stylesheet")
    if len(re.findall(r'href=["\\'][^"\\']*article-template\\.css(?:\\?[^"\\']*)?["\\']', content, re.I)) != 1:
        raise SystemExit(f"ERROR: {slug} must link exactly one shared article-template.css")
    if len(re.findall(r'href=["\\'][^"\\']*site\\.css(?:\\?[^"\\']*)?["\\']', content, re.I)) != 1:
        raise SystemExit(f"ERROR: {slug} must link exactly one site.css")
    if len(class_matches(content, "fact-grid")):
        raise SystemExit(f"ERROR: {slug} uses legacy fact-grid instead of frozen takeaways")
    quick = re.search(r"<section\\b[^>]*class=["\\'][^"\\']*quick-answer[^"\\']*["\\'][^>]*>([\\s\\S]*?)</section>", content, re.I)
    if not quick or not re.search(r"<h2\\b", quick.group(1), re.I):
        raise SystemExit(f"ERROR: {slug} quick answer must be one semantic section with a heading")
    toc = re.search(r"<nav\\b[^>]*class=["\\'][^"\\']*toc[^"\\']*["\\'][^>]*>([\\s\\S]*?)</nav>", content, re.I)
    ids = re.findall(r'\\bid=["\\']([^"\\']+)["\\']', content, re.I)
    if len(ids) != len(set(ids)):
        raise SystemExit(f"ERROR: {slug} contains duplicate element ids")
    if not toc:
        raise SystemExit(f"ERROR: {slug} table of contents is missing")
    broken = sorted({target for target in re.findall(r'href=["\\']#([^"\\']+)["\\']', toc.group(1), re.I) if target not in ids})
    if broken:
        raise SystemExit(f"ERROR: {slug} table of contents points to missing sections: {broken}")
    takeaways = re.search(r'<div\\b[^>]*class=["\\'][^"\\']*takeaways[^"\\']*["\\'][^>]*>([\\s\\S]*?)</div>\\s*<nav\\b[^>]*class=["\\'][^"\\']*toc', content, re.I)
    if not takeaways or len(re.findall(r'<div\\b[^>]*>\\s*<strong\\b', takeaways.group(1), re.I)) != 3:
        raise SystemExit(f"ERROR: {slug} must place exactly three takeaway cards before the TOC")
    positions = [class_matches(content, name)[0].start() for name in FROZEN_MASTER_SEQUENCE]
    if positions != sorted(positions):
        raise SystemExit(f"ERROR: {slug} modules are out of frozen master order")


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
            if hero_path.is_absolute() or ".." in hero_path.parts or not hero_image.startswith("assets/") or hero_path.suffix.lower() not in {".webp", ".svg"}:
                raise SystemExit(f"ERROR: invalid approved article hero path: {hero_image}")
            hero_source = ROOT / hero_path
            if not hero_source.is_file():
                raise SystemExit(f"ERROR: approved article hero is missing: {hero_image}")
            if hero_path.suffix.lower() == ".webp":
                with hero_source.open("rb") as image_file:
                    header = image_file.read(12)
                if len(header) != 12 or header[:4] != b"RIFF" or header[8:12] != b"WEBP":
                    raise SystemExit(f"ERROR: approved article hero is not a valid WebP: {hero_image}")
            else:
                raw_svg = hero_source.read_bytes()
                if re.search(rb"<!DOCTYPE|<!ENTITY", raw_svg, re.I):
                    raise SystemExit(f"ERROR: SVG hero must not contain a document type or entity declaration: {hero_image}")
                try:
                    svg_root = ET.fromstring(raw_svg)
                except ET.ParseError as error:
                    raise SystemExit(f"ERROR: approved SVG hero is malformed: {hero_image}: {error}") from error
                allowed_tags = {"svg", "title", "desc", "g", "rect", "circle", "ellipse", "line", "polyline", "polygon", "path", "text", "tspan"}
                if svg_root.tag.rsplit("}", 1)[-1].lower() != "svg":
                    raise SystemExit(f"ERROR: approved SVG hero must have an SVG root: {hero_image}")
                for node in svg_root.iter():
                    tag = node.tag.rsplit("}", 1)[-1].lower()
                    if tag not in allowed_tags:
                        raise SystemExit(f"ERROR: SVG hero contains an unsupported element {tag}: {hero_image}")
                    for attribute, value in node.attrib.items():
                        name = attribute.rsplit("}", 1)[-1].lower()
                        if name.startswith("on"):
                            raise SystemExit(f"ERROR: SVG hero contains an event handler: {hero_image}")
                        if name in {"href", "src"} and value and not value.startswith("#"):
                            raise SystemExit(f"ERROR: SVG hero contains an external reference: {hero_image}")
                        if re.search(r"url\s*\(\s*['\"]?(?:https?:|data:|//)", value, re.I):
                            raise SystemExit(f"ERROR: SVG hero contains an external URL: {hero_image}")
        articles.append((f"artikel/{slug}.html", record.get("dateModified"), hero_image))
    return articles




def clean_public_route(route: str) -> str:
    if route == "index.html":
        return ""
    return route[:-5] if route.endswith(".html") else route


def normalize_public_urls(content: str, origin: str) -> str:
    """Align published links and metadata with Cloudflare Pages clean URLs."""
    def clean_match(match: re.Match[str]) -> str:
        value = match.group(0)
        if value.endswith("/index.html"):
            return value[:-10]
        return value[:-5]
    # Only rewrite URL/path tokens, preserving source filenames and script text.
    content = re.sub(r"(?:https://asnpemda\.pages\.dev)?(?:/|\.{1,2}/)[A-Za-z0-9_./-]+\.html(?=[#?\"'\s])", clean_match, content)
    content = re.sub(re.escape(origin) + r"/([A-Za-z0-9_/-]+)\.html(?=[#?\"'\s])", lambda m: origin + "/" + m.group(1), content)
    return content

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
        candidates.append('<a class="blogroll-card" href="' + html_utils.escape(Path(relative).stem, quote=True) + '">' + picture + '<span class="blogroll-copy"><strong>' + html_utils.escape(title) + '</strong><span>Informasi dan penjelasan untuk ASN dan pemerintah daerah.</span><b>Baca artikel →</b></span></a>')
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
    block = '<section class="related-posts asn-blogroll" aria-labelledby="related-title"><div class="blogroll-heading"><span class="kicker">LANJUTKAN MEMBACA</span><h2 id="related-title">Bacaan selanjutnya</h2><p>Artikel lain yang sudah terbit di ASN Pemda.</p></div><div class="blogroll-grid">' + ''.join(candidates) + '</div><a class="blogroll-all" href="/#artikel-terbaru">Lihat semua artikel →</a></section>'
    return page[:start] + block + page[end:]




def homepage_topic(slug: str) -> str:
    if "pensiun" in slug or "gaji-pensiun" in slug:
        return "pensiun"
    if "pppk" in slug:
        return "pppk"
    if "wfh" in slug or "pemda" in slug:
        return "pemda"
    if "pbj" in slug or "pengadaan" in slug or "blud" in slug:
        return "pengadaan"
    return "lainnya"


def format_indonesian_date(value: str | None) -> str:
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", value or "")
    if not match:
        return ""
    year, month, day = match.groups()
    months = ("Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember")
    month_number = int(month)
    if not 1 <= month_number <= 12:
        return ""
    return f"{int(day)} {months[month_number - 1]} {year}"


def refresh_homepage_cards(home: str, articles: list[tuple[str, str | None, str | None]]) -> str:
    """Only approved articles appear; align generated cards with the homepage card template."""
    approved = {Path(relative).stem: (relative, modified, hero) for relative, modified, hero in articles}
    card_re = re.compile(r'<article class="article-card"[^>]*>[\s\S]*?</article>')
    cards = {}
    for match in card_re.finditer(home):
        card = match.group(0)
        found = re.search(r'href="/artikel/([a-z0-9-]+)(?:\.html)?"', card)
        if found and found.group(1) in approved:
            slug = found.group(1)
            card = re.sub(r'<article class="article-card"[^>]*>', '<article class="article-card" data-topic="' + homepage_topic(slug) + '">', card, count=1)
            cards[slug] = card
    for slug, (relative, modified, hero) in approved.items():
        if slug in cards:
            continue
        body = (ROOT / relative).read_text(encoding="utf-8")
        title_match = re.search(r'<title>(.*?)</title>', body, re.I | re.S)
        title = html_utils.unescape(title_match.group(1).split(' — ASN Pemda')[0]) if title_match else slug.replace('-', ' ').title()
        description_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', body, re.I)
        description = html_utils.unescape(description_match.group(1)) if description_match else 'Informasi terbaru untuk ASN dan pemerintah daerah.'
        published_match = re.search(r'<meta\s+property="article:published_time"\s+content="([^"]+)"', body, re.I)
        date = format_indonesian_date(published_match.group(1) if published_match else modified)
        reading_match = re.search(r'Waktu baca:\s*(?:sekitar\s*)?(\d+)\s*menit', body, re.I)
        reading = (reading_match.group(1) + ' menit baca') if reading_match else ''
        kicker_match = re.search(r'<div class="article-kicker">([\s\S]*?)</div>', body, re.I)
        category = ''
        if kicker_match:
            kicker_text = html_utils.unescape(re.sub(r'<[^>]+>', ' ', kicker_match.group(1)))
            parts = [part.strip() for part in kicker_text.split('•') if part.strip()]
            category = parts[-1].title() if parts else ''
        if not hero:
            hero_match = re.search(r'<figure[^>]*class="article-hero"[^>]*>[\s\S]*?<img[^>]*src="([^"]+)"', body, re.I)
            if hero_match:
                candidate = hero_match.group(1).replace('../', '').lstrip('/')
                if candidate.startswith('assets/') and (ROOT / candidate).is_file():
                    hero = candidate
        img = ('<img src="/' + html_utils.escape(hero, quote=True) + '" alt="" width="1200" height="675" loading="lazy">') if hero else '<span class="article-card-placeholder">ASN Pemda</span>'
        badge = '<span class="article-card-label">' + html_utils.escape(category) + '</span>' if category else ''
        meta = '<span>' + html_utils.escape(date) + '</span>' + ('<span>' + html_utils.escape(reading) + '</span>' if reading else '')
        cards[slug] = '<article class="article-card" data-topic="' + homepage_topic(slug) + '"><a class="article-card-image" href="/' + html_utils.escape(clean_public_route(relative), quote=True) + '">' + img + badge + '</a><div class="article-card-body"><div class="article-card-meta">' + meta + '</div><h3><a href="/' + html_utils.escape(clean_public_route(relative), quote=True) + '">' + html_utils.escape(title) + '</a></h3><p>' + html_utils.escape(description[:150]) + '</p><a class="text-link" href="/' + html_utils.escape(clean_public_route(relative), quote=True) + '">Baca artikel →</a></div></article>'
    ordered = sorted(cards, key=lambda slug: ((approved[slug][1] or '')[:10], slug), reverse=True)[:6]
    start = home.find('<div class="article-grid">')
    if start < 0:
        raise SystemExit('ERROR: homepage article grid missing')
    end = home.find('</div>\n</section>\n<section class="home-topics"', start)
    if end < 0:
        raise SystemExit('ERROR: homepage grid boundary missing')
    grid_class = 'article-grid article-grid-count-' + str(len(ordered))
    return home[:start] + '<div class="' + grid_class + '" data-topic-filter-grid>\n' + '\n'.join(cards[slug] for slug in ordered) + '\n  ' + home[end:]

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

    robots_path = DIST / "robots.txt"
    robots_text = robots_path.read_text(encoding="utf-8")
    robots_lines = [line for line in robots_text.splitlines() if not line.strip().lower().startswith("sitemap:")]
    robots_lines.append(f"Sitemap: {origin}/sitemap.xml")
    robots_path.write_text("\n".join(robots_lines) + "\n", encoding="utf-8")

    articles = published_articles()
    home_path = DIST / 'index.html'
    home_path.write_text(refresh_homepage_cards(home_path.read_text(encoding='utf-8'), articles), encoding='utf-8')
    for page_name in ("index.html", "about.html", "editorial.html", "privacy.html", "disclaimer.html", "koreksi.html"):
        page_path = DIST / page_name
        page_path.write_text(normalize_public_urls(page_path.read_text(encoding="utf-8"), origin), encoding="utf-8")
    for relative, _, hero_image in articles:
        target = DIST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        original = (ROOT / relative).read_text(encoding='utf-8')
        public_html = add_article_blogroll(original, relative, articles)
        insights_link = '<link rel="stylesheet" href="../assets/article-insights.css?v=20261023-2">'
        if insights_link in public_html:
            raise SystemExit(f"ERROR: duplicate article insights stylesheet: {relative}")
        if "</head>" not in public_html:
            raise SystemExit(f"ERROR: article head closing tag is missing: {relative}")
        public_html = public_html.replace("</head>", insights_link + "</head>", 1)
        canonical_tags = list(re.finditer(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*>', public_html, re.I))
        if len(canonical_tags) != 1:
            raise SystemExit(f"ERROR: published article must have exactly one canonical: {relative}")
        canonical_tag = canonical_tags[0].group(0)
        source_href = re.search(r'\bhref=["\']([^"\']+)["\']', canonical_tag, re.I)
        if not source_href:
            raise SystemExit(f"ERROR: published article canonical href is missing: {relative}")
        public_canonical = f"{origin}/{clean_public_route(relative)}"
        if source_href.group(1) != public_canonical:
            public_html = public_html.replace(source_href.group(1), public_canonical)
        target.write_text(normalize_public_urls(public_html, origin), encoding='utf-8')
        if hero_image:
            image_target = DIST / hero_image
            image_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / hero_image, image_target)

    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    urlset = ET.Element(f"{{{ns}}}urlset")
    for route in ("", "about", "editorial", "privacy", "disclaimer", "koreksi"):
        url = ET.SubElement(urlset, f"{{{ns}}}url")
        ET.SubElement(url, f"{{{ns}}}loc").text = f"{origin}/{route}"
    for relative, modified, _ in articles:
        url = ET.SubElement(urlset, f"{{{ns}}}url")
        ET.SubElement(url, f"{{{ns}}}loc").text = f"{origin}/{clean_public_route(relative)}"
        if modified:
            ET.SubElement(url, f"{{{ns}}}lastmod").text = modified
    ET.ElementTree(urlset).write(DIST / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    print(f"Public build complete: {len(BASE_FILES)} allowlisted files, {len(articles)} approved articles; output=dist/")


if __name__ == "__main__":
    main()
