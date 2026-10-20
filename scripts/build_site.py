#!/usr/bin/env python3
"""Build the public Cloudflare Pages site from an explicit allowlist.

Internal docs, research, pipeline code, candidate data, and unapproved draft pages
are never copied to the deploy artifact.
"""
from __future__ import annotations

import json
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
    "404.html",
    "favicon.svg",
    "favicon.ico",
    "robots.txt",
    "assets/site.css",
    "assets/author-suiza-ixan.webp",
)
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def published_articles() -> list[tuple[str, str | None]]:
    articles: list[tuple[str, str | None]] = []
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
        articles.append((f"artikel/{slug}.html", record.get("dateModified")))
    return articles


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
    for relative, _ in articles:
        target = DIST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)

    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    urlset = ET.Element(f"{{{ns}}}urlset")
    for route in ("", "about.html", "editorial.html", "privacy.html", "disclaimer.html"):
        url = ET.SubElement(urlset, f"{{{ns}}}url")
        ET.SubElement(url, f"{{{ns}}}loc").text = f"{origin}/{route}"
    for relative, modified in articles:
        url = ET.SubElement(urlset, f"{{{ns}}}url")
        ET.SubElement(url, f"{{{ns}}}loc").text = f"{origin}/{relative}"
        if modified:
            ET.SubElement(url, f"{{{ns}}}lastmod").text = modified
    ET.ElementTree(urlset).write(DIST / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    print(f"Public build complete: {len(BASE_FILES)} allowlisted files, {len(articles)} approved articles; output=dist/")


if __name__ == "__main__":
    main()
