# SOP Gaya Penulisan Artikel ASN Pemda v1.1

Status: **WAJIB untuk seluruh artikel baru dan revisi substansial**.

## Suara editorial
Tulis seperti rekan ASN yang memahami aturan dan menjelaskannya dengan ramah, santai, jernih, dan profesional. Pembaca utama: ASN, PPPK, bendahara, PPTK, PPK-SKPD, PA/KPA, pejabat OPD, dan masyarakat yang mencari penjelasan kebijakan daerah.

Santai **bukan** berarti bercanda soal hak pegawai, keuangan negara, atau konsekuensi hukum. Tidak menggunakan clickbait, hiperbola, bahasa merendahkan, jargon berlebihan, atau kepastian yang tidak didukung sumber.

## Struktur artikel yang disarankan
1. **Judul langsung menjawab kebutuhan pembaca**, tidak sensasional.
2. **Pembuka 2–3 kalimat**: apa persoalannya dan kenapa penting.
3. **Jawaban singkat**: apa yang sudah pasti diketahui, dan batasannya.
4. **Penjelasan inti** dengan subjudul berupa pertanyaan alami, misalnya “Siapa yang terdampak?” atau “Mulai kapan berlaku?”.
5. **Contoh situasi kerja** yang relevan bagi ASN/OPD; tandai sebagai ilustrasi, bukan ketentuan baru.
6. **Yang perlu dilakukan**: langkah praktis atau checklist, hanya bila didukung aturan.
7. **Dasar hukum dan sumber primer**: nama/nomor regulasi, pasal relevan, tanggal, tautan resmi, dan status berlaku bila dapat diverifikasi.
8. **Terakhir diperiksa** dan catatan perubahan substansi jika artikel diperbarui.

## Format halaman artikel standar

Gunakan pola editorial situs ASN Pemda dan Design System v1.0. Susunan ini menjadi baseline; pilih bagian yang benar-benar membantu pembaca dan jangan menambahkan blok hanya untuk memenuhi SEO.

1. **Head SEO:** satu title yang spesifik, deskripsi unik, canonical, status robots sesuai tahap publikasi, serta Open Graph dan Twitter Card. Gunakan satu H1 yang selaras dengan topik dan maksud pencarian.
2. **Navigasi halaman:** tautan lewati ke isi, header situs, breadcrumb, dan footer yang konsisten.
3. **Pembuka artikel:** kicker/topik, H1, ringkasan/deck 1–2 kalimat, nama penulis, tanggal terakhir diperiksa, dan perkiraan waktu baca.
4. **Hero image:** tampil setelah header artikel, sebelum kartu status atau jawaban singkat. Gunakan elemen `figure`, teks alternatif deskriptif, dimensi eksplisit, dan caption bila memberi konteks.
5. **Orientasi pembaca:** untuk artikel kebijakan yang berubah, tampilkan status kebijakan dan batas cakupannya. Tambahkan jawaban singkat; gunakan kartu fakta dan daftar isi bila panjang atau membantu navigasi.
6. **Isi:** susun H2/H3 berdasarkan pertanyaan dan urutan keputusan pembaca. Tambahkan tabel, contoh, langkah praktis, dan FAQ hanya bila menambah pemahaman.
7. **Penutup tepercaya:** sumber primer yang ditautkan, tanggal pemeriksaan, profil/tautan penulis, serta keterangan draft atau disclaimer yang sesuai.

### SEO dan structured data

- Tetapkan satu focus keyword dan sejumlah kecil keyword pendukung berdasarkan riset. Pakai secara alami di title, H1, slug, pembuka, dan subjudul yang relevan; hindari pengulangan mekanis.
- Meta description merangkum manfaat dan batas artikel secara akurat. Jangan mengklaim volume atau kesulitan keyword tanpa data.
- Untuk halaman artikel, isi canonical, Open Graph (`og:type=article`, `og:title`, `og:description`, `og:url`, `og:image`), `twitter:card=summary_large_image`, dan `twitter:image`.
- Gunakan JSON-LD `Article` dan `BreadcrumbList` bila cocok. `Article.image` harus menunjuk ke hero yang benar-benar tersedia pada URL publik saat halaman dirilis.
- Halaman draft tetap `noindex,follow`, tidak masuk sitemap/navigasi publik, dan tidak boleh disajikan sebagai artikel yang sudah terbit.

### Standar hero WebP

- Nama berkas deskriptif, huruf kecil dan tanda hubung, misalnya `assets/hero-{slug}.webp`. Format baku WebP; kanvas hero dianjurkan 1200 × 675 (16:9), dengan target ukuran sekitar 150 KB atau lebih kecil bila kualitas visual tetap baik.
- Gunakan ilustrasi editorial yang selaras dengan Design System v1.0 dan konteks artikel. Jangan membuat gambar seolah-olah foto bukti kejadian, memakai lambang resmi tanpa izin, atau menyisipkan teks yang berulang dengan judul.
- Tanam metadata EXIF/XMP yang tersedia: title/headline, description, creator/credit, subject, dan keyword target yang relevan. Catat path, format, dimensi, alt text, dan keyword pada record kandidat artikel.
- Metadata file memberi konteks/credit, tetapi tidak menjamin ranking. Utamakan filename bermakna, konteks halaman, alt text yang akurat, caption relevan, dan metadata sosial/structured data yang cocok.
- Tulis alt untuk menjelaskan isi/fungsi visual dalam satu kalimat ringkas; jangan menjejalkan keyword. Bila gambar dekoratif murni, gunakan alt kosong.
- Pada gambar hero, isi `width` dan `height`, gunakan `decoding=async`, serta prioritaskan pemuatan awal (`loading=eager`, `fetchpriority=high`). Gambar non-hero di bawah lipatan boleh memakai lazy loading.
- Sebelum review, cek file dapat dibuka dan benar-benar WebP, dimensi/rasio/ukuran masuk akal, metadata terbaca, URL/path cocok, alt/caption sesuai visual, serta OG dan Article schema menunjuk file yang sama.

## Aturan gaya bahasa
- Utamakan kalimat aktif dan pendek; satu gagasan utama per paragraf.
- Jelaskan singkatan pada penyebutan pertama (contoh: Surat Perintah Pencairan Dana/SP2D).
- Terjemahkan jargon birokrasi ke bahasa sehari-hari **tanpa mengubah istilah hukum aslinya**.
- Gunakan “Anda”, “kita”, atau penyebutan peran secara wajar; jangan menggurui.
- Gunakan tabel hanya jika benar-benar memudahkan perbandingan.
- Untuk mobile: paragraf ideal 2–4 kalimat, subjudul jelas, tidak ada dinding teks.
- Kutipan regulasi singkat dan tepat; jangan menyalin peraturan panjang tanpa kebutuhan.

## Aturan bukti dan status kebijakan
- Pisahkan dengan tegas **BERLAKU**, **DIUSULKAN/DIBAHAS**, **BELUM TERVERIFIKASI**, dan **TIDAK BERLAKU/DICABUT**.
- Jangan menyebut rencana, rumor, opini pejabat, atau berita sekunder sebagai ketentuan yang sudah berlaku.
- Jika aturan berbeda menurut instansi, daerah, tahun anggaran, jenis ASN, atau kondisi tertentu, jelaskan ruang lingkupnya.
- Klaim hak, gaji, tunjangan, pajak, pengadaan, dan APBD memerlukan rujukan primer yang spesifik.
- Jika sumber belum memadai, tandai keterbatasan dan **jangan terbitkan sebagai panduan definitif**.
- Jangan mengarang nomor pasal, tanggal, nominal, persentase, atau kutipan.

## Contoh transformasi
**Kaku:** “Sehubungan dengan diberlakukannya ketentuan dimaksud, aparatur sipil negara diwajibkan melakukan penyesuaian.”

**ASN Pemda:** “Apa yang berubah dari aturan ini? Siapa yang perlu menyesuaikan? Kita bahas poin pentingnya satu per satu.”

## Checklist editorial sebelum approval
- [ ] Pembuka menjawab kebutuhan ASN dalam 10 detik pertama
- [ ] Bahasa santai, profesional, dan tidak bertele-tele
- [ ] Ada contoh praktis bila relevan
- [ ] Semua singkatan dan istilah penting dijelaskan
- [ ] Status kebijakan dan cakupan penerapan jelas
- [ ] Klaim material ditautkan ke sumber primer dan pasal relevan
- [ ] Tidak ada judul sensasional atau kesimpulan melampaui sumber
- [ ] Satu H1, title/description/canonical, robots, Open Graph/Twitter, dan Article/Breadcrumb schema sesuai status rilis
- [ ] Hero WebP tersedia, metadata/record kandidat cocok, alt akurat, ukuran dan URL valid
- [ ] Mobile readability diperiksa
- [ ] Evidence review dan publication approval terpenuhi secara terpisah

**Gerbang rilis:** SOP gaya tidak menggantikan validasi sumber, legal review, maupun otorisasi publikasi.
