# Editorial review workflow v0.8

Evidence intake creates EVIDENCE_PENDING candidates, never articles. An editor inspects the original official document, identifies issuing authority, instrument number, legal status, applicability, and dates. Record VERIFY or REJECT with source URL, document identity, timestamp, reviewer and rationale.

Run: python scripts/editorial_gate.py candidate.json decision.json
VERIFY only creates REVIEW_PENDING with approved=false; it is not publication authorization. A separate explicit release authorization, immutable revision log and approved article record are still required.

Never treat a domain match, candidate fingerprint or reviewer name alone as proof of legal status. Sensitive rights, payroll, taxation and APBD claims require exact primary citations and independent review.
