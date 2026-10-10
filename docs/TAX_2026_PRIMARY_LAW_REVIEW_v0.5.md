# Pemeriksaan dasar hukum pajak SPJ 2026 — v0.5

Status: PRE_RELEASE / HOLD. Catatan penelitian sumber primer, bukan penetapan tarif atau pengecualian.

## Hierarki aturan

1. PMK 59/2022 tidak dapat digunakan sendirian. JDIH Kemenkeu mencatat pencabutan sebagian melalui PMK 81/2024.
2. PMK 81/2024 tercatat mengalami perubahan terbaru oleh PMK 1/2026. Verifikasi pasal konsolidasi dan ketentuan peralihan untuk setiap tanggal transaksi.
3. Artikel DJP mengenai PPh 22 instansi pemerintah hanya rujukan penjelasan, bukan pengganti pemeriksaan teks peraturan yang berlaku.

Sumber: https://jdih.kemenkeu.go.id/dok/pmk-81-tahun-2024 dan https://pajak.go.id/index.php/id/pemungutan-pajak-penghasilan-pasal-22-instansi-pemerintah

## Klasifikasi transaksi

| Kasus | Dasar awal | Fakta yang harus diuji | Status |
| --- | --- | --- | --- |
| Barang UP/GU | PMK 81/2024 dan perubahan sampai PMK 1/2026 | Jenis barang, nilai, status rekanan, tanggal, pemungut, pengecualian, bukti | HOLD |
| Barang LS | PMK 81/2024 dan perubahan sampai PMK 1/2026 | Kontrak, pembayaran, status penjual, dokumen pajak | HOLD |
| Katering | PMK 70/2022 Pasal 4 ayat (3) dan Pasal 8 | Pemesanan, proses produksi, lokasi penyajian berbeda, dokumen penyedia, PBJT daerah | HOLD |
| Restoran | PMK 70/2022 Pasal 4 ayat (2), (4), (5) | Layanan restoran versus toko/pabrik, struk, jenis gerai, PBJT daerah | HOLD |

Sumber teks PMK 70/2022: https://www.pajak.go.id/id/peraturan/kriteria-danatau-rincian-makanan-dan-minuman-jasa-kesenian-dan-hiburan-jasa-perhotelan

## Gate wajib

Reviewer harus mencatat pasal, ayat, perubahan, tanggal efektif, fakta transaksi, bukti, dan keputusan independen. Perlakuan PPh 23 katering serta hubungan PPN/PBJT dan peraturan daerah belum disimpulkan dalam dokumen ini. Jangan menyamakan tidak dikenai PPN dengan bebas dari semua pajak. Tidak ada aktivasi perhitungan otomatis.


## Verifikasi pasal sumber primer (10 Oktober 2026)

- **PMK 70/2022 Pasal 4 ayat (2)**: restoran/rumah makan/warung menyediakan layanan penyajian makan-minum, setidaknya fasilitas meja, kursi dan/atau peralatan makan di tempat.
- **Pasal 4 ayat (3)**: katering meliputi persiapan berdasarkan pesanan, penyajian di lokasi pemesan yang berbeda dari lokasi produksi/penyimpanan, dengan atau tanpa petugas/peralatan.
- **Pasal 4 ayat (4)–(5)**: penjualan makanan/minuman oleh toko swalayan tertentu, pabrik, atau lounge bandara termasuk kelompok yang dikenai PPN.
- **Pasal 8**: kategori jasa boga/katering yang tidak dikenai PPN merujuk pada kriteria Pasal 4 ayat (3).
- **PMK 81/2024**: JDIH mencatat perubahan keempat oleh **PMK 1/2026** bertanggal 22 Januari 2026. Ini verifikasi riwayat dokumen, **belum** verifikasi pasal spesifik PPh 22/PPh 23.

Sumber primer: https://pajak.go.id/id/peraturan/kriteria-danatau-rincian-makanan-dan-minuman-jasa-kesenian-dan-hiburan-jasa-perhotelan ; https://jdih.kemenkeu.go.id/dok/pmk-81-tahun-2024/overview ; https://jdih.kemenkeu.go.id/dok/pmk-1-tahun-2026/overview

**OPEN / BLOCKER:** teks konsolidasi pasal pemungutan PPh 22 instansi pemerintah dan PPh 23 jasa, pengecualian dan ketentuan efektif belum divalidasi menyeluruh; PBJT harus merujuk ketentuan daerah sesuai lokasi dan tanggal transaksi. Tidak ada tarif otomatis.


## Koreksi ruang lingkup PMK 1/2026 (audit 10 Oktober 2026)

**Penting:** PMK 1/2026 memang merupakan perubahan keempat PMK 81/2024, tetapi abstrak resmi JDIH BPK menerangkan substansinya terutama **penggunaan nilai buku atas pengalihan harta dalam restrukturisasi/penggabungan usaha**. Dengan demikian, **tidak tepat menyatakan bahwa PMK 1/2026 sendiri mengubah tarif atau tata cara PPh 22/PPh 23 belanja pemerintah** tanpa menunjukkan pasal yang relevan. Perubahan keempat tetap dicatat dalam riwayat konsolidasi, tetapi relevansi materinya terhadap tiap skenario SPJ harus diuji, bukan diasumsikan.

Sumber primer: https://peraturan.bpk.go.id/Details/342160/pmk-no-1-tahun-2026 ; https://stats.pajak.go.id/id/peraturan/perubahan-keempat-atas-peraturan-menteri-keuangan-nomor-81-tahun-2024-tentang-ketentuan

### Verifikasi lanjutan PPh 22/PPh 23 — belum boleh diputuskan otomatis

- PPh 22 belanja barang: cari pasal pemungut instansi pemerintah, dasar pengenaan, batas/pengecualian, dan tanggal efektif pada naskah konsolidasi; bedakan jalur UP/GU, LS, KKPD dan marketplace.
- PPh 23 jasa: pastikan klasifikasi objek jasa dan status penerima, dasar hukum pemotongan serta kemungkinan rezim lain; jangan menyimpulkan dari nama transaksi saja.
- Sumber sekunder yang menyebut tarif dipakai sebagai petunjuk penelusuran, bukan sumber otorisasi mesin.
- Catat setiap pasal/ayat, sumber primer, status perubahan, reviewer dan bukti transaksi sebelum mengubah state.

**Release gate tidak berubah:** PERLU_VERIFIKASI; taxAmount null; PRE_RELEASE / HOLD.
