# Date-aware tax verification v0.2

Implemented in `scripts/tax_decision.py` with regression tests in `scripts/test_tax_decision.py`.

- Optional `transactionDate` uses strict ISO `YYYY-MM-DD`; invalid dates fail with `INPUT_ERROR`. Missing dates trigger a verification prompt.
- KKPD triggers a dedicated collector/card-evidence check.
- Marketplace triggers platform, invoice and withholding evidence checks; dates before 1 October 2026 trigger historical-law review. The date is a **review flag**, not an automatic liability determination.
- Every valid scenario still returns `PERLU_VERIFIKASI` with `taxAmount: null`. `DAPAT_DIHITUNG` and `TIDAK_BERLAKU` remain disabled.
- Public HTML/JS is separate from this Python engine and is not yet date-aware. UI parity and legal review are required before release.

Reference: https://www.pajak.go.id/id/siaran-pers/pemungutan-pph-pasal-22-melalui-marketplace-mulai-dilaksanakan-1-oktober-2026

PRE_RELEASE / HOLD. No tax-rate activation or automatic publication.
