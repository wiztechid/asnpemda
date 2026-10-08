# Fetcher security review v0.5

Threats: SSRF via DNS resolution or rebinding, redirects, malicious HTML, excessive payload, unbounded requests, credential leakage, remote content instructions and source impersonation.

Implemented: HTTPS exact-host URL checks, reject redirects, timeout, maximum response bytes, allowed MIME, deterministic candidate-only output, no automatic publish, default dry-run, basic adversarial URL tests.

Open: resolve DNS and reject private/link-local/reserved IPs on every connection; enforce IP pinning and re-check redirect policy; robots.txt compliance; retry/backoff; per-domain quota; HTML parsing and document-level provenance; immutable evidence storage; independent security review.

Until these controls exist, DO NOT run scripts/pipeline.py --fetch on untrusted or broad source registries. No scheduled network workflow is configured.
