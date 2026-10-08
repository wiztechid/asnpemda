# Candidate intake

No automatic publication. Each candidate requires an immutable ID, source URL, discoveredAt, evidence snapshot/fingerprint, dedupe key, classification, materiality and review state. Store no credentials or private personnel information.

The current delta checker only reads local source-snapshots.json if present. A production HTTP fetcher and scheduling remain intentionally disabled until safeguards are implemented and tested.
