# Automation Policy v0.1

Pipeline: DISCOVER → DEDUPE → VERIFY → CLASSIFY → MATERIALITY → DRAFT/PATCH → REVIEW → PUBLISH → REVISION LEDGER.

## Delta-first
Bandingkan fingerprint/evidence sumber dengan versi terakhir. Tidak ada delta material = STOP tanpa rebuild massal.

## GitHub Mode Hemat
- PR/push: CI ringan saja.
- Heavy validation: `workflow_dispatch` setelah batch substantif selesai.
- Hindari schedule berat, matrix build, trigger ganda, dan full-site rebuild untuk perubahan kecil.
- Jika heavy validation gagal: perbaiki secara batch dengan CI ringan, lalu heavy validation sekali lagi.
