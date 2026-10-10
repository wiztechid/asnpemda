# Register bukti hukum pajak SPJ — review v0.3

**Status: PRE_RELEASE / HOLD.** Ini daftar bukti untuk pemeriksaan manusia, bukan kesimpulan tarif, kewajiban pemungutan, atau keputusan pajak otomatis.

| Rule | Jalur | Sumber awal | Perlu dibuktikan reviewer | Status |
| --- | --- | --- | --- | --- |
| SPJ-GENERAL | UP/GU, LS, KKPD, lainnya | [PMK 59/2022](https://peraturan.bpk.go.id/Details/215497/pmk-no-59pmk032022), [DJP PPh 22 Instansi Pemerintah](https://pajak.go.id/id/pemungutan-pajak-penghasilan-pasal-22-instansi-pemerintah) | Ketentuan yang masih berlaku pada tanggal transaksi, objek, pemungut, pengecualian, dokumen, dan pembulatan | PERLU_VERIFIKASI |
| MARKETPLACE-2026 | Marketplace | [PMK 37/2025](https://www.pajak.go.id/sites/default/files/lampiran/PMK%2037%20TAHUN%202025.pdf), [siaran pers DJP 1 Oktober 2026](https://www.pajak.go.id/id/siaran-pers/pemungutan-pph-pasal-22-melalui-marketplace-mulai-dilaksanakan-1-oktober-2026) | Platform yang benar-benar ditunjuk, tanggal efektif, status pedagang, invoice dan bukti pungut, serta kemungkinan kewajiban instansi pemerintah yang berbeda | PERLU_VERIFIKASI |
| NON-APPLICABLE | Pengecualian | Belum ditetapkan per jenis pajak | Bukti pengecualian dan persetujuan reviewer | DISABLED |
| READY | Perhitungan | Belum tersedia matriks tarif terotorisasi | Peraturan terkini, tanggal berlaku, dasar pengenaan, perhitungan, rounding, uji, persetujuan rilis | DISABLED |

## Audit status regulasi — 10 Oktober 2026

**Temuan material:** JDIH Kementerian Keuangan mencatat PMK 59/PMK.03/2022 (perubahan PMK 231/2019) **dicabut sebagian** oleh PMK 81 Tahun 2024, dengan catatan Pasal 2 sampai Pasal 7 dan Pasal 23. Karena itu PMK 59/2022 tidak dapat dipakai sendirian sebagai dasar keputusan transaksi 2026. Detail ketentuan konsolidasi dan perubahan sesudahnya masih wajib dicek pasal per pasal.

Sumber resmi:
- https://jdih.kemenkeu.go.id/dok/59-pmk-03-2022/summary
- https://jdih.kemenkeu.go.id/dok/pmk-81-tahun-2024/summary
- https://pajak.go.id/index.php/id/pemungutan-pajak-penghasilan-pasal-22-instansi-pemerintah

**Gate wajib:** reviewer memverifikasi pasal yang berlaku pada tanggal transaksi, perubahan/pencabutan, perbedaan PPh 22 instansi pemerintah dan PPh 22 marketplace, serta perlakuan KKPD. Informasi tarif/ambang dalam materi DJP diperlakukan sebagai petunjuk penelitian, bukan angka siap hitung. Seluruh rule tetap fail-closed.

## Pengendalian perubahan

- Tanggal **1 Oktober 2026** dipakai hanya untuk memicu pemeriksaan historis marketplace, **bukan** untuk memutuskan pajak otomatis.
- PPh 22 yang dipungut platform atas penghasilan pedagang **tidak boleh otomatis disamakan** dengan pemungutan PPh 22 oleh instansi pemerintah.
- Sebelum rilis: catat nomor pasal, kutipan singkat, tanggal berlaku, status pencabutan/perubahan, sumber resmi, tanggal akses, reviewer, dan keputusan setiap skenario. Tinjau juga Perkada/Sisdur yang berlaku.
- Jangan mengaktifkan state DAPAT_DIHITUNG atau TIDAK_BERLAKU hanya karena sebuah tautan sumber tersedia.
- Browser Chromium smoke dan CI Light telah lulus pada commit 504279f; pengujian teknis bukan pengesahan dasar hukum.

## Release gate

Perlu review hukum dan perpajakan independen, validasi transaksi uji, evidence snapshot bertanggal, dan persetujuan manusia. Hingga seluruhnya terpenuhi, semua keluaran tetap PERLU_VERIFIKASI dan taxAmount null.
