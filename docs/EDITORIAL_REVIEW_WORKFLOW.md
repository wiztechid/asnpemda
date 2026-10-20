# Editorial assessment and publication workflow v1.0

Evidence intake creates a candidate. An editor or AI assistant can check the original official source, issuing authority, document identity, legal/policy status, applicability and dates. Record the source URL, retrieval time, rationale and limitations.

An AI-assisted editorial assessment is advisory. It may identify scope, attribution, tone and freshness risks. It is not a human review and must not be represented as an ASN's professional judgment.

Independent editorial or legal review may be requested when useful, but is not required for publication. The human site owner records the final decision and remains accountable for the published material. For high-materiality policy claims, the approval must identify the exact article bytes, evidence fingerprint, approver and approval time.

Run: python scripts/editorial_gate.py candidate.json decision.json
VERIFY means evidence has been checked; it does not itself authorize publication. Publication still requires the separate, explicit human owner GO decision, an immutable revision record and a published article record.

Never treat a domain match, candidate fingerprint or reviewer name alone as proof of legal status. Cite primary sources, state limitations, and do not present an announcement or plan as a regulation in force.
