# Changelog

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
