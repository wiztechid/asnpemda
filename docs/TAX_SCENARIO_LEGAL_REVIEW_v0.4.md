# Matriks review hukum per skenario SPJ — v0.4

**PRE_RELEASE / HOLD — bukan penetapan pajak.** Matriks ini mengarahkan verifikasi manusia; seluruh skenario tetap `PERLU_VERIFIKASI` dan `taxAmount = null`.

| Skenario | Fakta yang harus dicatat | Pertanyaan hukum yang wajib dijawab | Bukti minimum | Status |
| --- | --- | --- | --- | --- |
| Pembelian barang UP/GU | Tanggal, nominal, barang, identitas penjual, dokumen | Apakah objek termasuk pemungutan PPh 22 instansi pemerintah; adakah batas/pengecualian yang relevan; siapa pemungut | Invoice, bukti bayar, identitas/status perpajakan, dasar aturan berlaku | HOLD |
| Pembelian barang LS | Kontrak/SPK, tanggal, nominal, penyedia, dokumen tagihan | Periksa pihak pemungut dan jenis pajak menurut objek, mekanisme LS, serta pengecualian | Kontrak, BAST, invoice, dokumen pajak, bukti pembayaran | HOLD |
| Jasa katering | Rincian layanan, penyedia, tempat penyerahan, tanggal | Bedakan jasa boga/katering dengan penyediaan makan-minum restoran; cek klasifikasi PPh/PPN/PBJT dan aturan daerah | Kontrak, rincian menu/layanan, invoice, bukti usaha, aturan daerah | HOLD |
| Makan-minum restoran | Bentuk transaksi, jenis penyedia, tempat, tanggal | Apakah termasuk objek PBJT makanan/minuman atau kategori lain; apakah ada kewajiban PPh yang berbeda | Struk, invoice, identitas usaha, aturan PBJT setempat | HOLD |
| Jasa lainnya | Uraian jasa, kontrak, penerima penghasilan | Identifikasi objek PPh berdasarkan jasa dan status penerima, bukan hanya label umum | SPK, BAST, invoice, identitas rekanan, ketentuan PPh | HOLD |
| Pembayaran KKPD | Penerbit kartu, merchant, invoice, pihak yang menagih | Apakah instrumen pembayaran mengubah pihak pemungut? Jangan mengasumsikan KKPD menghapus kewajiban pajak | Bukti transaksi KKPD, invoice, bukti potong/pungut, SOP bank | HOLD |
| Marketplace | Platform, tanggal, identitas pedagang, invoice, bukti pungut | Apakah platform ditunjuk dan memungut PPh 22 pedagang; apakah kewajiban instansi pemerintah tetap terpisah; cek ketentuan efektif pada tanggal transaksi | Bukti penunjukan platform, invoice, bukti pemungutan, peraturan dan riwayat perubahan | HOLD |
| Dokumen pengecualian | Jenis pajak yang dikecualikan, dasar dan periode | Apakah pengecualian sah, spesifik pada objek dan tanggal transaksi | Dokumen pengecualian yang valid, pasal, reviewer | HOLD |

## Evidence checklist reviewer

Untuk setiap skenario, catat: **ID skenario, tanggal transaksi, dasar hukum resmi, nomor pasal/ayat, status berlaku/perubahan, tanggal mulai berlaku, kutipan terbatas, dokumen transaksi, penanggung jawab pemungutan, reviewer, tanggal review, dan keputusan**. Jika satu unsur kritis belum ada, tetap HOLD.

Rujukan awal (belum diverifikasi lengkap untuk setiap skenario):

- [Permendagri 77/2020](https://peraturan.bpk.go.id/Details/162792/permendagri-no-77-tahun2020) — penatausahaan keuangan daerah.
- [PMK 59/2022](https://peraturan.bpk.go.id/Details/215497/pmk-no-59pmk032022) — pemungutan/pemotongan pajak instansi pemerintah.
- [DJP PPh 22 Instansi Pemerintah](https://pajak.go.id/id/pemungutan-pajak-penghasilan-pasal-22-instansi-pemerintah).
- [PMK 37/2025](https://www.pajak.go.id/sites/default/files/lampiran/PMK%2037%20TAHUN%202025.pdf) dan [siaran pers DJP marketplace 1 Oktober 2026](https://www.pajak.go.id/id/siaran-pers/pemungutan-pph-pasal-22-melalui-marketplace-mulai-dilaksanakan-1-oktober-2026).

**Larangan aktivasi:** tidak boleh mengubah `enabled`, `autoCalculation`, atau menerbitkan angka tarif sebelum review peraturan resmi, uji contoh transaksi, approval independen, dan keputusan release manusia.
