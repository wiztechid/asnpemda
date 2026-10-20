# ASN Pemda MVP Release Gate v1.0

## Scope
MVP foundation-to-publication: official source registry, candidate intake, evidence metadata, editorial assessment, static site, SEO and legal/trust pages.

## Release principles
- No autonomous publication of legal, financial, or personnel-policy claims.
- Candidate, verified evidence, editorial assessment, human approval and deployment are separate states.
- An official domain alone does not establish that a statement is law.
- Primary evidence identifies original URL, issuer, document/statement date, retrieval time and content fingerprint.
- Material policy content requires a recorded human site-owner approval and revision history. Independent review is optional.
- AI-assisted assessment can support quality control but is not represented as human review or professional ASN judgment.
- dateModified tracks substantive edits; lastVerified tracks source rechecks.
- Unapproved content stays out of the sitemap and remains noindex.
- Never treat a failed source fetch as a policy withdrawal.
- Do not claim freshness without successful verification.

## Gate
P0: verified evidence + explicit human owner GO bound to exact article and evidence revisions + schema validation.
P1: content quality, accessible mobile UI, working source links, canonical, structured data, sitemap and robots.
P2: discovery automation only after conditional requests, timeouts, backoff, rate limits, domain controls and failure tests.

## Release policy
CI light runs on push/PR; heavy audit is workflow_dispatch at the end of a substantive batch. A green syntax check is not publication approval. Production verification remains required after deployment.
