# ASN Pemda MVP Release Gate v0.4

## Scope
MVP foundation-to-publication: official source registry, candidate intake, deterministic dedupe/delta, evidence metadata, editorial approval, static site, SEO and legal/trust pages.

## Non-negotiable
- No autonomous publication of legal, financial, or personnel rights claims.
- Candidate != verified. Draft != approved. Approved != deployed.
- Official domain alone does not establish that a statement is law.
- Primary evidence must identify original URL, issuer, document/statement date, retrieval time, and content fingerprint.
- Material policy changes require human approval and an append-only revision record.
- dateModified tracks substantive edits; lastVerified tracks rechecks.
- Unapproved content must not appear in sitemap and must remain noindex.
- Never treat a failed source fetch as a policy withdrawal.
- Do not claim freshness without successful verification.

## Gate
P0: verified evidence + explicit human approval + schema validation.
P1: content quality, accessible mobile UI, source links, canonical, structured data, sitemap and robots.
P2: discovery automation only after HTTP conditional requests, timeouts, backoff, rate limits, domain controls and failure tests.

## Release policy
CI light on push/PR, heavy audit only workflow_dispatch at end of substantive batch. A green syntax check is not publication approval.
