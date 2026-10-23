# ASN Pemda — Current Status

Updated: 2026-10-23

## Release state
PUBLICATION_ACTIVE / HOMEPAGE_DEPLOYED / VISUAL_QA_PENDING. Homepage improvements are live on Cloudflare Pages. Five article records are approved and published under the human publication gate; automatic publishing remains disabled.

## Production deployment
- Site: https://asnpemda.pages.dev
- Git commit: `2da56e41d4a64a19151ca8cb899c3cd5d56dfb4f`
- Cloudflare Pages deployment: `cf8deb79-5891-4a8d-93b9-7b1844b44b5d`
- Cloudflare build and deploy stages: success
- Browser-level HTTP verification of the stable URLs remains pending because the connected Opera browser was unavailable during this check.

## Public output and SEO
Cloudflare Pages builds with `python scripts/build_site.py` into `dist/`. The explicit allowlist excludes research, internal docs, scripts, schemas, candidate data, and unapproved draft pages. Approved article pages and their hero assets enter output only when a matching record is both `approved: true` and `publicationState: PUBLISHED`.

The builder generates the sitemap from six public information pages and the approved published articles. The sitemap excludes drafts and noindex pages. The public `robots.txt` sitemap directive is generated from `site-config.json`.

Published article identity URLs are normalized in the public build so the canonical URL, Open Graph URL, Article JSON-LD `mainEntityOfPage`, and sitemap location agree. Frozen article source files and the article master remain unchanged. The editorial SOP is now v1.5 and includes the homepage integration requirements.

## Technical validation
- CI Light run 137 (`39888358080`) passed the sitemap and canonical regression gate.
- CI Light run 139 (`39889056544`) passed canonical, Open Graph, Article JSON-LD, sitemap, public-build, and article-hero checks.
- CI Light run 182 (`39926173331`) passed homepage filter, card consistency, social metadata, public-build, and existing regression checks.
- Homepage now has accessible topic filters, localized generated-card metadata, balanced desktop card rows, and Open Graph/Twitter large-image preview metadata. SOP v1.5 records the reusable requirements.
- Cloudflare Pages build and deploy completed successfully for the production commit above.
- Automated local-link and indexability audits passed in CI.

## Remaining checks
- Fetch the stable production `robots.txt`, `sitemap.xml`, and article URLs in a connected browser and confirm the served responses.
- Verify the Search Console property and submit `https://asnpemda.pages.dev/sitemap.xml`.
- Complete the remaining live mobile/accessibility review before closing deployment QA.

## Editorial readiness
- Article structure and hero-image workflow follow `docs/ARTICLE_WRITING_SOP.md` v1.5.
- Primary-source verification and a separate human publication authorization remain required for material legal, tax, payroll, personnel, and APBD claims.
- Draft article pages and prototypes are omitted from the public build and sitemap.
- No private operating playbook or keyword research is included in the Cloudflare artifact.
- Design System v1.0 and the article master remain frozen. The editorial SOP is maintained separately and is updated to v1.5.
