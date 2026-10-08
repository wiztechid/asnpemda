# Content model and lifecycle v0.4

Topics: asn-cpns, kesejahteraan, karier, keuangan-daerah, pemerintahan-daerah, pengadaan-aset, pengawasan.

Article formats: policy-update, living-explainer, operational-guide.

Candidate state machine:
DISCOVERED -> DEDUPED -> EVIDENCE_PENDING -> VERIFIED -> DRAFTED -> REVIEW_PENDING -> APPROVED -> PUBLISHED
Any state -> BLOCKED (with reason). Rejected candidates -> REJECTED.
PUBLISHED -> REVIEW_PENDING when material changes occur; existing published revision remains available until replacement approved.

Canonical issue ID is stable. Separate claims from analysis, unknowns and scenario discussion.
Approval must identify reviewer, timestamp, revision fingerprint and source evidence.
Avoid duplicating the same news into multiple canonical URLs.
