# ASN Pemda — Current Status

Updated: 2026-10-20

## Release state
PRE_RELEASE / HOLD. The public site shell is available at Cloudflare Pages. No policy article is approved for public publication yet.

## Public output
Cloudflare Pages builds with `python scripts/build_site.py` into `dist/`. The builder copies an explicit allowlist: home, About, editorial policy, privacy, disclaimer, 404, design CSS, author image, favicons, and robots file. Approved articles enter output only when a matching record is both `approved: true` and `publicationState: PUBLISHED`.

## Editorial readiness
- Article structure and hero-image workflow are standardized in `docs/ARTICLE_WRITING_SOP.md` v1.1; WebP hero metadata, accessibility, social preview, and structured-data checks apply to new articles.
- Primary-source verification and a separate human publication authorization are required for material legal, tax, payroll, personnel, and APBD claims.
- Draft article pages and prototypes are omitted from the public build and sitemap.
- No private operating playbook or keyword research is included in the Cloudflare artifact.
- The homepage describes the site's method and scope without presenting an unapproved item as a current article.

## Remaining release gates
- Approve an evidence-backed launch article and preserve its review record.
- Complete a live mobile/accessibility and link review on the final content corpus.
- Finalize the public correction/contact route before inviting corrections or comments.
- Record a separate human GO decision for publication.

## Technical baseline
- Design System v1.0 remains frozen.
- CI light checks source links and tests the public build allowlist.
- Heavy validation stays manual/on-demand after a substantive batch.
