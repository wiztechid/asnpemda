# Source Pipeline v0.2
Source registry lives in data/sources.json. Only approved official domains are candidates for primary evidence.
DISCOVER is not equivalent to VERIFY. Candidate snapshots are input, not evidence by themselves.
Delta check uses SHA-256 content fingerprints. Only changed candidates enter review; do not auto-publish.
Next implementation gate: safe HTTP fetching (timeouts, conditional GET, robots and rate limits), immutable evidence metadata, domain allowlist, date/identity validation, and human review.
No external fetcher or automatic scheduler is enabled in v0.2.
