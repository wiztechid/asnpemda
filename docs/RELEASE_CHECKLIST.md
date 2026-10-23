# ASN Pemda release readiness checklist

## Public site foundation
- [x] Canonical production URL and sitemap origin configured
- [x] Allowlisted static output; repository root is not deployed
- [x] Draft article and prototype paths excluded from Pages output and sitemap
- [x] Core trust pages use a shared navigation and visual system
- [x] Public build allowlist is checked by CI

## Article publication
- [x] Evidence-backed articles checked against current primary sources
- [x] AI-assisted editorial assessments recorded with their limitations
- [x] Human site-owner GO recorded against each published article and evidence revision
- [x] Independent reviewer is optional under SOP v1.0
- [x] Article metadata, robots, hero image and source links prepared for publication
- [x] Published articles linked from homepage and included in generated sitemap

## Technical SEO artifact gate
- [x] Sitemap URLs are unique, resolve to public HTML, and exclude noindex pages
- [x] Canonical and Open Graph URLs match each sitemap location
- [x] Article JSON-LD is valid and `mainEntityOfPage` matches the canonical URL
- [x] `robots.txt` sitemap directive follows the configured production origin
- [x] CI Light public build and regression checks pass

## Post-deploy verification
- [ ] Production `robots.txt`, sitemap, article pages and hero images fetched from the stable hostname
- [ ] Search Console property verified and sitemap submitted
- [ ] Desktop and mobile layout and accessibility checked on the production site
- [x] Source and local internal links checked in CI

Release state: TECHNICAL_RUNTIME_QA_PENDING. Cloudflare Pages build/deploy succeeded; browser-level production URL verification remains open.
