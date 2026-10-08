# ASN Pemda — SERP Opportunity Map v0.2 (8 October 2026)

**State: RESEARCH ONLY / PRE_RELEASE HOLD.** No automatic article publication or unverified tax rules. This is a qualitative opportunity assessment, **not** measured search volume, KD, or a completed top-10 SERP scrape. Keyword inventory: 50 candidates in `keyword-map-50.csv`.

## Evidence reviewed (official sources)
- DJP PPh 22 instansi pemerintah: https://pajak.go.id/index.php/id/pemungutan-pajak-penghasilan-pasal-22-instansi-pemerintah
- DJP classification issue for government food/catering purchases: https://www.pajak.go.id/id/berita/kpp-cibeunying-bahas-aspek-pajak-pengadaan-makanan-dan-minuman
- DJP older article (2019; **historical only**, not current tax rate authority): https://www.pajak.go.id/en/node/37509
- PMK 59/PMK.03/2022 on BPK legal portal (check subsequent amendments): https://peraturan.bpk.go.id/Details/215497/pmk-no-59pmk032022
- Government regional SPJ/SPM example: https://bpkpd.natunakab.go.id/uploads/produk_hukum/perbup/Perbup_10_Thn_2023_ttg_Sistem_dan_Prosedur_Pengeloaan_Keuangan_Daerah.pdf

## Competition insight
- **Tax**: DJP owns authoritative explanation and regulatory facts. Compete on transparent case decision trees, calculators, exceptions, and human-readable examples—not claiming superior legal authority.
- **SPJ**: Local-government checklists exist, but applicability varies by jurisdiction. Provide national baseline + clearly identified local examples, never treat a regional Perbup as universal.
- **Pension**: Generic calculator queries are broader; win on transparent inputs, privacy, and explicit nonofficial assumptions.

## Ten proposed URLs (not yet published)

| Order | URL path | Primary keyword | Priority | Qualitative confidence | Distinct value |
|---|---|---|---|---|---|
| 1 | `/tools/kalkulator-pajak-spj/` | kalkulator pajak belanja pemerintah | P0 | HIGH | interactive calculator; explicit verification states |
| 2 | `/pajak/pph-22-belanja-pemerintah/` | kalkulator PPh 22 bendahara pemerintah | P0 | MEDIUM | transaction examples and exceptions; DJP dominates generic intent |
| 3 | `/pajak/pajak-makan-minum-kegiatan/` | pajak belanja makan minum pemerintah | P0 | HIGH | decision tree restaurant/catering/packaged food |
| 4 | `/pajak/pajak-jasa-catering/` | pajak jasa catering pemerintah daerah | P0 | MEDIUM | classification cases; avoid outdated 2019 rate |
| 5 | `/pajak/pph-22-di-bawah-2-juta/` | PPh 22 belanja di bawah 2 juta | P0 | MEDIUM | threshold, transaction-splitting and exceptions |
| 6 | `/pajak/cara-hitung-dpp-ppn/` | cara menghitung DPP PPN belanja pemerintah | P1 | MEDIUM | interactive formula with verified current tax rules |
| 7 | `/penatausahaan/checklist-spj-belanja-barang/` | checklist SPJ belanja barang | P0 | HIGH | interactive checklist with national/local applicability |
| 8 | `/penatausahaan/kelengkapan-spm-gu-tu-ls/` | kelengkapan SPM GU pemerintah daerah | P1 | MEDIUM | side-by-side UP/GU/TU/LS and exceptions |
| 9 | `/penatausahaan/rekonsiliasi-bku-rekening-koran/` | contoh rekonsiliasi BKU rekening koran | P1 | HIGH | worked example and reconciliation template |
| 10 | `/tools/kalkulator-masa-kerja-pns/` | kalkulator masa kerja PNS | P1 | MEDIUM | client-side date calculator; distinguish service concepts |

**Confidence means editorial product-fit only**, not evidence of low ranking difficulty.

## First three editorial briefs

### 1. `/tools/kalkulator-pajak-spj/`
- User: bendahara, verifikator, PPK-SKPD; intent: classify a real transaction, check whether enough facts exist, then compute and explain.
- UX: type of goods/services; seller/taxpayer status; transaction value, VAT-inclusive flag; procurement channel; exemption flags; tax-period/rule version.
- Output: decision tree, formula, assumptions, citations, warning states **PERLU VERIFIKASI** and **TIDAK DAPAT DITENTUKAN**; no unconditional tax-rate claims.
- P0 legal gate: primary current law, amendment status, threshold applicability, marketplace/KKPD specifics, VAT base and rounding, reviewed test cases.
- CTA: related articles and free single-transaction PDF; no ad lock.

### 2. `/pajak/pajak-makan-minum-kegiatan/`
- User intent: understand different treatment of restaurant, catering, packaged food, and procurement arrangements.
- H2 outline: identify what was actually purchased; evidence checklist; tax classification decision tree; three worked cases; frequent mistakes; when to ask tax office.
- Caveat: DJP's 2019 explainer is background context, **not** evidence that its stated VAT rates remain valid in 2026.
- Distinguish local food/beverage tax from national VAT and the separate income-tax question.
- CTA: calculator with classification fields prefilled, only after legal gate.

### 3. `/penatausahaan/checklist-spj-belanja-barang/`
- User intent: know which documents to prepare and why SPM/SPJ gets returned.
- H2 outline: identify payment route; baseline evidence; conditional evidence; verifier checklist; 5 return reasons; local-regulation differences; downloadable checklist.
- Separate national rules, jurisdiction-specific Sisdur, and operational recommendations. Do not use Natuna checklist as binding Bontang procedure.
- CTA: free printable checklist; link to GU/TU/LS article.

## Publication gates
1. Complete **top-10 live SERP audit per selected keyword** (domain, content type, publication date, user intent, gap); not completed here.
2. Confirm each current primary regulation and amendments as of publication date; reviewer and review timestamp.
3. Avoid keyword cannibalization: calculator = transaction execution, PPh22 article = legal explainer, food article = classification cases.
4. One page per distinct intent; useful interactive or original case material; internal links and schema only if accurate.
5. Human review, editorial approval, release authorization; keep PRE_RELEASE HOLD until explicit GO.

## Next action
Complete live SERP top-10 evidence for first three keywords, then draft the three pages in staging with noindex and tests. Avoid scaling to 50 articles until Search Console gives impression/click evidence.
