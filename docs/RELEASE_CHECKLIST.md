# ASN Pemda release readiness checklist

## Public site foundation
- [x] Canonical production URL and sitemap origin configured
- [x] Allowlisted static output; repository root is not deployed
- [x] Draft article and prototype paths excluded from Pages output and sitemap
- [x] Core trust pages use a shared navigation and visual system
- [x] Public build allowlist is checked by CI

## Article publication
- [x] Evidence-backed article checked against current primary sources
- [x] AI-assisted editorial assessment recorded with its limitations
- [x] Human site-owner GO recorded against exact article and evidence revisions
- [x] Independent reviewer is optional under SOP v1.0
- [x] Article metadata, robots, hero image and source links prepared for publication
- [x] Article linked from homepage and included in generated sitemap

## Post-deploy verification
- [ ] Production article URL returns the published page and image
- [ ] Desktop and mobile layout checked
- [ ] Source and internal links checked
- [ ] Canonical, robots, structured data and sitemap checked on production

Release state: DEPLOYMENT_QA_PENDING. Publication authorization is recorded; deployment is not complete until production checks pass.
