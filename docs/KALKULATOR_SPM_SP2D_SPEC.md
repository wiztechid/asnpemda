# Kalkulator Potongan SPM/SP2D — DEV v0.1
Tanggal telaah aturan: 28 Oktober 2026. Status: **DRAFT / human review required before production**.
Halaman: `/kalkulator-spm-sp2d.html`; mesin: `/assets/spm-tax-engine.js`.
Tidak mengubah template artikel yang FROZEN.

## Cakupan
1. PPh 21: Bukan Pegawai/profesional (DPP 50% bruto, Pasal 17), peserta kegiatan (bruto, Pasal 17), PNS honor final APBD (PP 80/2010).
2. PPh 22: belanja barang 1,5% (tanpa NPWP 3%) dengan ambang Rp2 juta dan pengecualian KKPD, pihak lain, SKB, barang tertentu.
3. PPh 23: jasa badan, sewa selain tanah/bangunan (2% / 4% jika tidak ada NPWP).
4. PPh final 4(2): pekerjaan konstruksi 1,75% / 2,65% / 4%; konsultansi 3,5% / 6%; sewa tanah/bangunan 10%.
5. PPN: nonmewah 12% × 11/12 (efektif 11%), barang mewah 12% (PPnBM belum dihitung), nilai invoice termasuk/belum termasuk PPN, pilihan instansi/rekanan/pihak lain.
6. Potongan nonpajak: retensi, uang muka, denda, lain-lain (tidak otomatis mengurangi DPP pajak).
7. Ringkasan nilai pembayaran, potongan PPh, PPN dipungut instansi, dan estimasi transfer; salin/cetak.

## Contoh uji DEV v0.1 (17/17 lulus pada 28 Oktober 2026)
| Skenario | Pajak PPh | Netto |
| --- | ---: | ---: |
| Penerjemah orang pribadi bukan pegawai Rp5.100.000 | Rp127.500 | Rp4.972.500 |
| Barang Rp2.000.000 | Rp0 | Rp2.000.000 |
| Barang Rp10.000.000 + PPN | Rp150.000 | Rp9.850.000 |
| Barang invoice incl. PPN Rp11.100.000 | Rp150.000 | Rp9.850.000 |
| Barang KKPD Rp10.000.000 + PPN | Rp0 | Rp11.100.000 (PPN dipungut pihak yang wajib, bukan instansi) |
| Barang tanpa NPWP Rp10.000.000 | Rp300.000 | Rp9.700.000 |
| Jasa badan Rp5.000.000 | Rp100.000 | Rp4.900.000 |
| Jasa badan tanpa NPWP | Rp200.000 | Rp4.800.000 |
| Fisik kualifikasi kecil Rp100.000.000 + PPN | Rp1.750.000 | Rp98.250.000 |
| Konsultan konstruksi bersertifikat Rp100.000.000 | Rp3.500.000 | Rp96.500.000 |
| Honor PNS golongan III Rp5.100.000 | Rp255.000 | Rp4.845.000 |
| Tanpa status pajak / DPP nilai lain khusus | Ditahan sampai verifikasi | — |

## Quality gates sebelum production
- [x] Source rules diarahkan ke situs peraturan DJP/JDIH.
- [x] Hitungan uji independen 17/17 sesuai ekspektasi.
- [x] Tidak memodifikasi template artikel FROZEN.
- [x] Tidak ada penyimpanan PII: input dihitung di browser.
- [ ] Verifikasi tampilan HP dan desktop di URL Cloudflare Pages preview.
- [ ] Review pajak oleh petugas yang kompeten (Bendahara/BPKAD/konsultan pajak).
- [ ] Review peraturan khusus dan potongan SP2D OPD sesuai praktik setempat.
- [ ] Konfirmasi sebelum merge dan publikasi.
- [ ] End-to-end print-to-PDF dan salin hasil di perangkat nyata.

## Aturan keamanan penggunaan
Kalkulator tidak boleh dianggap sebagai instruksi pemungutan otomatis. Untuk PPh final UMKM, PPh 26, 15, TER gaji/TPP, PPnBM, kontrak campuran, faktur dengan DPP khusus, withholding dari sistem pengadaan, perlakuan penerima luar negeri, dan termin/retensi kompleks, tampilkan batasan dan eskalasi manual. Jangan memaksa memilih jenis PPh hanya karena nama rekening/kegiatan.

## Dasar resmi
- PMK 168 Tahun 2023 — https://pajak.go.id/id/peraturan/petunjuk-pelaksanaan-pemotongan-pajak-atas-penghasilan-sehubungan-dengan-pekerjaan-jasa-1
- PMK 51 Tahun 2025 — https://pajak.go.id/id/peraturan/pemungutan-pajak-penghasilan-pasal-22-sehubungan-dengan-pembayaran-atas-penyerahan-1
- PMK 231/2019 jo. PMK 59/2022 — https://www.pajak.go.id/sites/default/files/Lampiran%20PMK59PMK032022.pdf
- PPN PMK 131/2024; PMK 11/2025 — https://www.pajak.go.id/index.php/id/peraturan/perlakuan-pajak-pertambahan-nilai-atas-impor-barang-kena-pajak-penyerahan-barang-kena
- Jasa konstruksi PP 9/2022 — https://pajak.go.id/en/node/35073
- Honor PNS PP 80/2010 — https://jdih.bpkp.go.id/dokumen/data_dokumen/PP%2080%20Tahun%202010.pdf
