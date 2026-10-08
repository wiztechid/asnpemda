# Offline evidence intake v0.7

1. Open the original official source in a browser; confirm issuer, date, legal status and exact URL.
2. Save a short factual excerpt as a local UTF-8 text file (do not include private personnel data or secrets).
3. Preview: python scripts/manual_intake.py --source-id bkn --url https://www.bkn.go.id/berita/example --document-date 2026-10-08 --text-file evidence.txt
4. Only after checking: append --write to create an unverified candidate in data/candidates/queue.json.
5. Review source and article claims separately; approval is a later human action, never implicit.

The queue stores a fingerprint and metadata, not the source text itself. Keep originals in controlled evidence storage. A hash without preserved evidence is not independently auditable; publication remains blocked until evidence retention is implemented.

Remote fetching via scripts/pipeline.py --fetch is disabled; the legacy urllib implementation was removed.
