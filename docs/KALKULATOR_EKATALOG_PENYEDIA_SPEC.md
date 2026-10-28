# Modul Pajak E-Katalog/INAPROC untuk Penyedia — DEV v0.2 (2026)

**QA: draft. Belum layak menjadi acuan final/produksi tanpa telaah pajak dan uji browser.**
Dibuat sebagai modul tambahan kalkulator potongan SPM/SP2D ASN Pemda (tanpa mengubah artikel FROZEN).

## Masalah yang diselesaikan
Penyedia dan petugas SPM/SP2D kerap menyamakan E-Katalog, platform pengadaan Pihak Lain, dan transaksi langsung sehingga keliru menerapkan PPh 22 **0,5% versus 1,5%**. Keduanya memiliki pemungut dan kondisi berbeda. 

## Route pajak yang wajib diverifikasi
1. **LS (pembayaran langsung)**: tidak menggunakan pemungutan **PPh 22 oleh Pihak Lain 0,5%** dalam PMK 58/2022. Evaluasi PPh berdasarkan objek/penerima (barang PPh 22, jasa badan PPh 23, Bukan Pegawai PPh 21, konstruksi PPh final, sewa bangunan PPh final). Pemeriksaan fasilitas PPh final UMKM/SK sengaja memblokir perhitungan otomatis.
2. **UP atau KKP melalui Pihak Lain yang ditunjuk** menurut PMK 58/2022: PPh 22 **0,5% dari nilai tagihan sebelum PPN**, berlaku untuk barang, jasa, sewa, konstruksi. Jika sudah dipungut PPh 22 oleh Pihak Lain, instansi tidak melakukan pemotongan PPh lain atas penghasilan yang sama. Jika rekanan adalah PKP dan penyerahan terutang PPN, PPN dipungut Pihak Lain. Jasa angkutan umum orang pribadi dikecualikan.
3. **Belum jelas pemungut/platform**: jangan memutuskan tarif secara otomatis. Verifikasi pesanan, mekanisme bayar, penunjukan Pihak Lain, dokumen tagihan dan bukti pungut.
4. **PPh final dan selisih**: PPh 22 yang dipungut Pihak Lain dapat menjadi bagian pelunasan PPh final; untuk konstruksi/sewa tanah bangunan, estimasi selisih dari PPh final penuh ditampilkan terpisah dari potongan saat pembayaran. Penyedia mungkin wajib menyetor sendiri kekurangan menurut PMK 58 Pasal 6 ayat (6).
5. **UMKM (PP 55/2022 jo PP 20/2026)**: status kelayakan, bentuk usaha, omzet dan bukti surat keterangan harus diverifikasi; khusus orang pribadi, pembebasan bagian omzet s.d. Rp500 juta per tahun dapat mempengaruhi kewajiban final. Jangan beranggapan semua CV/PT/perorangan otomatis 0,5%.

## Data input
- Mekanisme: LS, UP/KKP via Pihak Lain dengan bukti penunjukan, atau belum terverifikasi.
- Bentuk penyedia, identitas NPWP/NIK, PKP/non-PKP, rezim PPh umum/UMKM.
- Objek: barang, jasa badan, jasa profesional OP, pekerjaan/konsultansi konstruksi, sewa tanah/bangunan, sewa kendaraan/peralatan, angkutan umum OP.
- Kualifikasi konstruksi sesuai SBU/SKK; harga termasuk atau belum termasuk PPN; status PPN terutang (efektif 11%), tidak terutang, mewah/PPnBM, DPP khusus.
- Hasil: bruto, PPN, pungutan PPh, pemungut PPh dan PPN, net transfer, estimasi selisih PPh final, dan dokumen verifikasi.

## 13 pengujian deterministik DEV
| Skenario | DPP | PPh saat pembayaran | PPN | Bersih ke rekanan | Lainnya |
|---|---:|---:|---:|---:|---|
| Barang LS PKP | Rp10 jt | PPh22 Rp150 rb | Rp1,1 jt dipungut instansi | Rp9,85 jt | Pasal 22 umum |
| Barang UP via Pihak Lain | Rp10 jt | PPh22 Rp50 rb | Rp1,1 jt oleh Pihak Lain | Rp9,95 jt | **Bukan** 1,5% |
| Jasa badan UP Pihak Lain | Rp10 jt | PPh22 Rp50 rb | Rp1,1 jt | Rp9,95 jt | Tidak tambah PPh23 |
| Konstruksi UP Pihak Lain kecil bersertifikat | Rp100 jt | PPh22 Rp500 rb | Rp11 jt | Rp99,5 jt | Sisa final estimasi Rp1,25 jt |
| Sewa tanah/bangunan UP Pihak Lain | Rp10 jt | PPh22 Rp50 rb | Rp1,1 jt | Rp9,95 jt | Sisa final estimasi Rp950 rb |
| Barang LS Rp2 juta | Rp2 jt | Rp0 | Rp220 rb terutang (bukan dipungut instansi) | Rp2,22 jt | Pemungut PPN harus diverifikasi |
| Barang UP Pihak Lain Rp1 jt | Rp1 jt | PPh22 Rp5 rb | Rp110 rb | Rp995 rb | Tidak pakai ambang LS 2 juta |
| Jasa badan LS PKP Rp10 jt | Rp10 jt | PPh23 Rp200 rb | Rp1,1 jt | Rp9,8 jt | Klasifikasi objek diverifikasi |
| Status penunjukan Pihak Lain belum ada | — | DITAHAN | — | — | Anti penetapan prematur |
| Mekanisme belum diketahui | — | DITAHAN | — | — | Anti default tidak berdasar |
| Rezim UMKM LS belum diverifikasi | — | DITAHAN | — | — | Perlu surat keterangan |
| Non-PKP melalui platform PMK58 tanpa dasar pengecualian | — | DITAHAN | — | — | Pasal 3–4 |
| Non-PKP meminta PPN 11% | — | DITAHAN | — | — | Periksa PKP |

## Acceptance sebelum production
- [x] 13 skenario inti lulus saat pengujian engine 28 Okt 2026.
- [x] Data yang belum lengkap memblokir hasil.
- [x] Tidak menyimpan data rekening, NPWP, atau identitas pribadi di backend.
- [x] Halaman terpisah untuk penyedia dengan link dari kalkulator utama dan homepage DEV.
- [ ] Uji langsung perangkat HP/desktop pada URL preview Cloudflare Pages dan export PDF.
- [ ] Audit pajak independen terhadap semua kategori dan pengecualian (termasuk nilai transaksi, PKP/non-PKP, jasa profesional berulang, PPh final UMKM).
- [ ] Review SOP dan dokumen e-purchasing versi 6 serta surat tagihan / sistem pembayaran BPKAD.
- [ ] Merge dan publish hanya setelah QA PASS dan otorisasi manusia.

## Regulasi primer
- PMK 58/PMK.03/2022 (status aktif): https://www.pajak.go.id/id/peraturan/penunjukan-pihak-lain-sebagai-pemungut-pajak-dan-tata-cara-pemungutan-penyetoran-dan-atau
- Lampiran contoh pemotongan PMK58: https://www.pajak.go.id/sites/default/files/Lampiran_PMK582022.pdf
- PMK 231/2019 jo PMK 59/2022: https://www.pajak.go.id/sites/default/files/Lampiran%20PMK59PMK032022.pdf
- PMK 51/2025: https://stats.pajak.go.id/id/peraturan/pemungutan-pajak-penghasilan-pasal-22-sehubungan-dengan-pembayaran-atas-penyerahan-1
- PP 20/2026 jo PP 55/2022: https://www.pajak.go.id/id/peraturan/perubahan-atas-peraturan-pemerintah-nomor-55-tahun-2022-tentang-penyesuaian-pengaturan-0
- Katalog versi 6 SEB LKPP-Kemendagri 1/2025: https://jdih.lkpp.go.id/regulation/surat-edaran-bersama/surat-edaran-bersama-nomor-1-tahun-2025

**Batasan penting:** istilah "marketplace" dalam PMK 37/2025 untuk pasar komersial dan PMK 58/2022 untuk Sistem Informasi Pengadaan Pemerintah bukan dasar pertukaran tarif. Produk katalog saja tidak membuktikan Pihak Lain bertindak sebagai pemungut. 
