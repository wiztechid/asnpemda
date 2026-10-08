# Tax Decision Matrix v0.1 — FAIL CLOSED

**Release:** PRE_RELEASE / HOLD. This is a **verification workflow**, not a tax calculation engine. `DAPAT_DIHITUNG` and `TIDAK_BERLAKU` are defined but intentionally DISABLED. Every public input currently yields `PERLU_VERIFIKASI`.

## Rechecked primary sources (2026-10-08)
- [PMK 231/2019 as amended by PMK 59/2022](https://peraturan.bpk.go.id/Details/215497/pmk-no-59pmk032022): government withholding/collection and special procurement/card pathways require case-specific checks. Further amendments and effective rules must be validated before formulas.
- [PMK 37/2025 official PDF](https://www.pajak.go.id/sites/default/files/lampiran/PMK%2037%20TAHUN%202025.pdf): marketplace seller-income withholding is not automatically identical to government purchasing withholding.
- [DJP earlier postponement](https://www.pajak.go.id/id/pengumuman/penundaan-waktu-pemberlakuan-ketentuan-pemungutan-pph-pasal-22-oleh-marketplace): originally postponed until November.
- [DJP press release dated 1 Oct 2026](https://www.pajak.go.id/id/siaran-pers/pemungutan-pph-pasal-22-melalui-marketplace-mulai-dilaksanakan-1-oktober-2026): later announcement supersedes the previously announced implementation timetable, and names four appointed marketplaces. Verify actual transaction documents before claiming withholding occurred.
- [DJP current marketplace FAQ](https://pajak.go.id/marketplace): informational explanation, distinguish from primary PMK text.

## Decision flow
1. Validate amount as safe nonnegative integer, type, seller and payment channel. If invalid, ask for corrections.
2. If Marketplace, ask platform, transaction date, seller status, evidence of platform withholding and invoice; flag `PERLU_VERIFIKASI`.
3. If UP/GU, LS, KKPD or other, check applicable government withholding rules, goods vs services, seller status, exceptions and evidence; flag `PERLU_VERIFIKASI`.
4. Only an approved, effective-date-scoped, source-cited legal matrix can activate `TIDAK_BERLAKU` or `DAPAT_DIHITUNG`.
5. Never compute PPh/PPN/PBJT or net payment from a generic transaction amount until base, treatment and rounding are established.

## Acceptance tests before enablement
| ID | Scenario | Current expected | Future requirement |
|---|---|---|---|
| T01 | ordinary goods purchase via UP/GU | PERLU_VERIFIKASI | Check tax object and exclusions |
| T02 | LS consulting service | PERLU_VERIFIKASI | PPh category, supplier status, invoice |
| T03 | restaurant meal | PERLU_VERIFIKASI | Distinguish PBJT/PPN/PPh |
| T04 | catering service | PERLU_VERIFIKASI | Evidence-based classification |
| T05 | KKPD purchase | PERLU_VERIFIKASI | Card-specific collector provisions |
| T06 | marketplace purchase Oct 2026 | PERLU_VERIFIKASI | PMSE designation and withholding proof |
| T07 | claim of exemption without document | PERLU_VERIFIKASI | Verify exemption evidence |
| T08 | transaction dated before rule change | PERLU_VERIFIKASI | Historical effective-date rules |
| T09 | zero amount | PERLU_VERIFIKASI | Determine meaningful transaction first |
| T10 | negative, fractional or unsafe amount | INPUT_ERROR | Reject invalid input |

No auto-approval, no publication, no rate assertions. Human legal review and full case coverage are required before any computation is switched on.
