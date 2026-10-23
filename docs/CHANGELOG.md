# Changelog

## 2026-10-23 — Sitemap and article identity URL QA
- Generated the public `robots.txt` sitemap directive from `site-config.json` and added CI checks for unique, resolvable sitemap URLs, canonical consistency, noindex exclusion, Open Graph identity URLs, and Article JSON-LD URL consistency.
- Normalized article canonical, Open Graph, and Article JSON-LD identity URLs only in the public build output; frozen article source, article master, and editorial SOP were not changed.
- PR #12 merged as `ef34fced2e8fe6aa32dd0564925a92725f94894d`; CI Light run 137 passed.
- PR #13 merged as `a0027409ddf6bd54d14c1ea6a784a8c70408c261`; CI Light run 139 passed; Cloudflare Pages deployment `b77cb590-010e-451f-9b33-3550a93a7007` completed successfully.
- Browser-level fetch of the stable production URLs and Search Console sitemap submission remain pending; deployment is not marked fully verified.

## 2026-10-20 — Dampak kebijakan, koreksi publik, dan hero article build
- Perjelas standar bahwa daftar persiapan tanpa dasar aturan resmi harus diberi label opsional, bukan kewajiban atau syarat.
- Siapkan halaman koreksi publik dan formulir GitHub dengan peringatan privasi; kanal ini tetap memakai pelaporan publik, bukan mengumpulkan email/data pribadi di situs.
- Perluas build allowlist untuk halaman koreksi dan menyalin hero WebP hanya bersama artikel yang disetujui.
- Tambahkan smoke test yang memeriksa artikel dan hero WebP ikut terbangun serta tercatat pada sitemap.

## 2026-10-20 — Article format and WebP hero standard v1.1
- Standardized the reusable article page structure, SEO metadata, structured data, and status-aware draft handling in `docs/ARTICLE_WRITING_SOP.md`.
- Added the 1200 × 675 WebP hero workflow covering embedded EXIF/XMP metadata, descriptive alt text, Open Graph/Twitter cards, Article schema, candidate records, and validation.
- Applied the standard to the PPPK 2027 article; its image remains attached to the draft PR and is not public until the separate publication gates pass.
- Preserved Design System v1.0.

## 2026-10-20 — SOP alignment and public build boundary
- Kept Design System v1.0 and refreshed the home, About, editorial, privacy, disclaimer, and not-found pages as one coherent reader journey.
- Removed the homepage promotion of an unapproved draft; topic cards now describe scope rather than link to unpublished articles.
- Added an allowlisted Cloudflare Pages build to `dist/`; drafts, research, internal docs, scripts, schemas, and candidate data are excluded.
- Added a public-build smoke test to CI and normalized root-relative links in the static site audit.
- Set the canonical site origin to `https://asnpemda.pages.dev` and added trust-page sitemap entries.
- Refined the low-poly ASN Pemda mark to match the author's hairstyle and glasses; removed the tie and facial hair.
- Publication remains PRE_RELEASE / HOLD pending evidence and human approval.
