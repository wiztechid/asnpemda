# Manual evidence intake v0.7

Prepare a local JSON array with sourceId, url, issuer, documentDate (YYYY-MM-DD), retrievedAt (ISO 8601 with timezone), title and evidenceText. Execute python scripts/evidence_intake.py input.json --output candidates.json locally.

Candidate output is deliberately UNVERIFIED and EVIDENCE_PENDING. The source domain is checked against data/sources.json, but issuer authenticity, exact document identity, legal force, materiality and any quotations must be independently verified by an editor. The text is not copied into published pages.

Do not commit personal data, passwords, confidential documents, or large full-text copyrighted reproductions. Prefer minimal evidence excerpts and source URLs. Network fetching and autonomous publication remain disabled.
