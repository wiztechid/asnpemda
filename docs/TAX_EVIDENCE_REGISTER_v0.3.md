# Register bukti hukum pajak SPJ — review v0.3

**Status: PRE_RELEASE / HOLD.** Ini daftar bukti untuk pemeriksaan manusia, bukan kesimpulan tarif, kewajiban pemungutan, atau keputusan pajak otomatis.

| Rule | Jalur | Sumber awal | Perlu dibuktikan reviewer | Status |
| --- | --- | --- | --- | --- |
| SPJ-GENERAL | UP/GU, LS, KKPD, lainnya | [PMK 59/2022](https://peraturan.bpk.go.id/Details/215497/pmk-no-59pmk032022), [DJP PPh 22 Instansi Pemerintah](https://pajak.go.id/id/pemungutan-pajak-penghasilan-pasal-22-instansi-pemerintah) | Ketentuan yang masih berlaku pada tanggal transaksi, objek, pemungut, pengecualian, dokumen, dan pembulatan | PERLU_VERIFIKASI |
| MARKETPLACE-2026 | Marketplace | [PMK 37/2025](https://www.pajak.go.id/sites/default/files/lampiran/PMK%2037%20TAHUN%202025.pdf), [siaran pers DJP 1 Oktober 2026](https://www.pajak.go.id/id/siaran-pers/pemungutan-pph-pasal-22-melalui-marketplace-mulai-dilaksanakan-1-oktober-2026) | Platform yang benar-benar ditunjuk, tanggal efektif, status pedagang, invoice dan bukti pungut, serta kemungkinan kewajiban instansi pemerintah yang berbeda | PERLU_VERIFIKASI |
| NON-APPLICABLE | Pengecualian | Belum ditetapkan per jenis pajak | Bukti pengecualian dan persetujuan reviewer | DISABLED |
| READY | Perhitungan | Belum tersedia matriks tarif terotorisasi | Peraturan terkini, tanggal berlaku, dasar pengenaan, perhitungan, rounding, uji, persetujuan rilis | DISABLED |

## Pengendalian perubahan

- Tanggal **1 Oktober 2026** dipakai hanya untuk memicu pemeriksaan historis marketplace, **bukan** untuk memutuskan pajak otomatis.
- PPh 22 yang dipungut platform atas penghasilan pedagang **tidak boleh otomatis disamakan** dengan pemungutan PPh 22 oleh instansi pemerintah.
- Sebelum rilis: catat nomor pasal, kutipan singkat, tanggal berlaku, status pencabutan/perubahan, sumber resmi, tanggal akses, reviewer, dan keputusan setiap skenario. Tinjau juga Perkada/Sisdur yang berlaku.
- Jangan mengaktifkan state DAPAT_DIHITUNG atau TIDAK_BERLAKU hanya karena sebuah tautan sumber tersedia.
- Browser Chromium smoke dan CI Light telah lulus pada commit 504279f; pengujian teknis bukan pengesahan dasar hukum.

## Release gate

Perlu review hukum dan perpajakan independen, validasi transaksi uji, evidence snapshot bertanggal, dan persetujuan manusia. Hingga seluruhnya terpenuhi, semua keluaran tetap PERLU_VERIFIKASI dan taxAmount null.
