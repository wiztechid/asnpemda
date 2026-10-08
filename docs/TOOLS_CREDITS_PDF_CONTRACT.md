# ASN Pemda Tools — Credits & Detailed PDF Contract v0.1

Status: DESIGN ONLY / NOT LIVE. No payment collection, credit ledger, or paid PDF is deployed.

## Value proposition
On-screen calculators remain free. Credits purchase an optional, substantive downloadable report with calculation breakdown, assumptions, applicable legal references, verification checklist and reproducibility metadata. Never charge for access to legal texts or public rules.

## Proposed experimental pricing
Starter 10 credits Rp10.000; Regular 30 credits Rp25.000; Pro 100 credits Rp75.000. Summary PDF 2 credits; detailed PDF 5 credits; batch PDF 10 credits plus disclosed volume limits. All prices subject to payment-provider fees, tax, refund and market testing. Display effective rupiah price and exact credits before purchase.

## PDF report specification
Tax SPJ: input snapshot and transaction classification; taxes and exceptions; itemized formulas and rounding; result and net payable; article-level primary legal citations with verification date; required-document checklist; ambiguous conditions and escalation; calculation ID, engine version, regulation version, generation timestamp and clear non-official disclaimer.
Pension: birthdate, role, retirement-age assumption and caveats; remaining service; income/expense inputs; inflation and savings scenarios; year-by-year projection; assumptions, sensitivity, version and non-official disclaimer.
No invented regulation or benefit entitlement. Block detailed legal PDF when source evidence is missing or stale.

## Credit transaction contract
Use a server-authoritative append-only double-entry ledger: purchase_pending -> provider_webhook_verified -> credit_granted; report_quote -> credit_reserved -> report_generated -> credit_captured. On failure, release reservation. Use unique idempotency keys for webhook events and report requests; atomic database transaction and unique constraints prevent duplicate charges. Never trust client-supplied balance or payment status. Credit balance is derived from ledger entries and reconciled daily.

Re-download of the same immutable report is free for a defined retention period; a changed calculation is a new quote. Explicitly disclose expiration policy (prefer no expiration), refund policy, report retention, privacy policy, and price before payment. Do not deduct credits for validation errors or failed PDF generation.

## Privacy and security
Prefer client-side calculations. Avoid storing employee identity, NIP, taxpayer identifiers, salary details or full SPJ unless essential and consented. Encrypt necessary data in transit and at rest; short retention; authenticated access and ownership checks. PDFs use random opaque IDs and signed short-lived download links. Do not expose reports by predictable URLs. Protect webhooks with signature verification, replay defense and event deduplication. Rate-limit generation and prevent arbitrary HTML/template injection.

## Rollout gate
Phase 1: free calculators + local PDF prototype, no payment.
Phase 2: payment-provider selection, legal/privacy/ASN conflict-of-interest review, database/ledger and adversarial tests in sandbox.
Phase 3: small paid beta only after human GO.
No paid credits, balance claims or production checkout before these gates pass.
