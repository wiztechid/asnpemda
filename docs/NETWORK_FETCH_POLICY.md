# Network Fetch Policy — strict fail-closed

A preflight DNS check is NOT enough to defeat DNS rebinding. The legacy pipeline.py --fetch code uses urllib and must not be enabled as a production discovery workflow. No scheduled fetch workflow exists.

secure_fetch.py demonstrates public-IP validation, no redirects, bounded robots checks and deliberately disabled network transport. It will remain disabled until a reviewed transport can pin the verified IP through the TLS connection while preserving hostname/SNI/certificate verification, enforce all A/AAAA responses public, robots allow, quotas, retry/backoff and immutable evidence storage.

Until then, manually curated primary evidence can be entered into a candidate review queue. Never ingest external content as instructions or publish it without editorial review.
