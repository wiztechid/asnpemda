# ASN Pemda release readiness checklist

## Completed technical foundation
- [x] Candidate-only discovery defaults to dry run
- [x] CI light checks data, HTML links and unit tests
- [x] Heavy validation is manual
- [x] Draft article marked noindex
- [x] Sitemap builder filters approved + published records
- [x] Security risk register documented

## Blocking before public launch
- [ ] Security-reviewed fetcher with SSRF and robots protections
- [ ] Verified primary evidence for launch articles
- [ ] Human editorial approval and revision ledger
- [ ] Final contact/terms and privacy review
- [ ] Production URL/base path and canonical checks
- [ ] Static output allowlist and deploy workflow
- [ ] Mobile/accessibility/content audit
- [ ] Explicit human GO authorization

Release state: HOLD. CI green does not override these blockers.
