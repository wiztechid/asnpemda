# Publication Authorization v0.9

An editor's APPROVE decision is bound to SHA-256 of the exact article file bytes, a reviewed evidence fingerprint and review fingerprint. Editing the article (even whitespace), replacing the evidence or revising the review invalidates authorization.

Command: python scripts/publication_approval.py article.json reviewed-evidence.json decision.json

This produces an approval proposal record; it does not publish or modify the article. Protect the approval record with repository branch protection, reviewer separation, append-only audit history and human authorization before production use. The author must not self-approve high-impact claims.

Next gate: build a publication validator that requires this approval record for every published article and enforces revision ledger continuity. Current site remains PRE_RELEASE.
