# SOP Penulisan dan Publikasi Artikel ASN Pemda v1.5

Status: **WAJIB untuk seluruh artikel baru dan revisi substansial**.

Pembaruan v1.4 (21 Oktober 2026) menetapkan keterhubungan artikel, umpan balik pembaca, komentar tanpa akun dengan penyaringan anti-spam dan moderasi, serta pemeriksaan fitur setelah rilis.

Pembaruan v1.5 (23 Oktober 2026) menambahkan standar konsistensi kartu artikel, filter topik homepage, dan pratinjau sosial homepage.

## Suara editorial
Tulis seperti rekan ASN yang memahami aturan dan menjelaskannya dengan ramah, santai, jernih, dan profesional. Pembaca utama: ASN, PPPK, bendahara, PPTK, PPK-SKPD, PA/KPA, pejabat OPD, dan masyarakat yang mencari penjelasan kebijakan daerah.

Santai **bukan** berarti bercanda soal hak pegawai, keuangan negara, atau konsekuensi hukum. Tidak menggunakan clickbait, hiperbola, bahasa merendahkan, jargon berlebihan, atau kepastian yang tidak didukung sumber.

## Struktur artikel yang disarankan
1. **Judul langsung menjawab kebutuhan pembaca**, tidak sensasional.
2. **Pembuka 2–3 kalimat**: apa persoalannya dan kenapa penting.
3. **Inti ketentuan**: apa yang sudah pasti diketahui, dan batasannya. Untuk topik nonregulasi, gunakan judul ringkasan yang paling alami.
4. **Penjelasan inti** dengan subjudul berupa pertanyaan alami, misalnya “Siapa yang terdampak?” atau “Mulai kapan berlaku?”.
5. **Contoh situasi kerja** yang relevan bagi ASN/OPD; tandai sebagai ilustrasi, bukan ketentuan baru.
6. **Dampak dan persiapan**: sebutkan kewajiban hanya jika ada dasar resmi. Jika belum ada, sajikan hal yang dapat dipantau sebagai awareness opsional dan tandai bahwa itu bukan syarat atau instruksi.
7. **Dasar hukum dan sumber primer**: nama/nomor regulasi, pasal relevan, tanggal, tautan resmi, dan status berlaku bila dapat diverifikasi.
8. **Terakhir diperiksa** dan catatan perubahan substansi jika artikel diperbarui.

## Format halaman artikel standar

Gunakan pola editorial situs ASN Pemda dan Design System v1.0. Susunan ini menjadi baseline; pilih bagian yang benar-benar membantu pembaca dan jangan menambahkan blok hanya untuk memenuhi SEO.

1. **Head SEO:** satu title yang spesifik, deskripsi unik, canonical, status robots sesuai tahap publikasi, serta Open Graph dan Twitter Card. Gunakan satu H1 yang selaras dengan topik dan maksud pencarian.
2. **Navigasi halaman:** tautan lewati ke isi, header situs, breadcrumb, dan footer yang konsisten.
3. **Pembuka artikel:** kicker/topik, H1, ringkasan/deck 1–2 kalimat, nama penulis, tanggal terakhir diperiksa, dan perkiraan waktu baca.
4. **Hero image:** tampil setelah header artikel, sebelum kartu status atau jawaban singkat. Gunakan elemen `figure`, teks alternatif deskriptif, dimensi eksplisit, dan caption bila memberi konteks.
5. **Orientasi pembaca:** untuk artikel kebijakan yang berubah, tampilkan status kebijakan dan batas cakupannya. Tambahkan ringkasan inti (label “Inti ketentuan” untuk artikel regulasi); gunakan kartu fakta dan daftar isi bila panjang atau membantu navigasi.
6. **Isi:** susun H2/H3 berdasarkan pertanyaan dan urutan keputusan pembaca. Tambahkan tabel, contoh, langkah praktis, dan FAQ hanya bila menambah pemahaman.
   - Jika aturan atau instruksi resmi belum tersedia, jangan menyebut langkah sebagai kewajiban atau syarat. Sajikan sebagai daftar awareness/persiapan opsional, sebutkan bahwa itu bukan persyaratan resmi, dan batasi pada dampak yang bisa dipantau dari informasi yang ada.
   - **Template subjudul artikel FROZEN:** H2 bagian utama (H2 langsung di `.article-body` atau langsung di dalam `section` isi) memakai kartu sorotan bernomor urut, aksen biru, dan ruang teks yang sejajar di tengah. Jangan menambahkan label berulang seperti “Poin penting”. Judul komponen di dalam isi—misalnya kalkulator atau panel alat—tidak ikut dinomori atau diberi kartu H2. H3 memakai aksen kecil tanpa nomor. Pola harus tetap rapi pada ponsel dan diterapkan melalui stylesheet terpusat saat build, tanpa mengubah teks/urutan naskah artikel.
7. **Penutup tepercaya:** sumber primer yang ditautkan, tanggal pemeriksaan, profil/tautan penulis, serta keterangan draft atau disclaimer yang sesuai.

### Keterhubungan artikel dan partisipasi pembaca

- Tautkan artikel lain di dalam isi hanya saat topik dan maksud pembaca benar-benar beririsan; jelaskan hubungan konteksnya dengan teks tautan yang deskriptif.
- Cantumkan blok **Artikel terkait** di bawah isi artikel jika tersedia artikel relevan. Pilih berdasarkan kesamaan kebijakan, kelompok ASN, atau langkah kerja; jangan menampilkan rekomendasi acak atau mengulang judul tanpa alasan.
- Sediakan umpan balik ringkas “Apakah artikel ini membantu?” dan kolom komentar tanpa login bila layanan komentar aktif. Jangan meminta email atau data kepegawaian.
- Komentar harus melalui Turnstile, pembatasan frekuensi, pemeriksaan tautan/promosi, dan tinjauan manual sebelum tayang. Komentar pembaca adalah masukan, bukan sumber resmi atau pernyataan ASN Pemda.
- Gunakan satu blok **Suara Pembaca** per artikel: umpan balik satu klik dan formulir komentar. Letakkan setelah artikel terkait dan sebelum profil penulis/fitur berbagi.
- Kiriman komentar harus tersimpan sebagai `pending`; endpoint publik hanya boleh mengembalikan komentar `approved`. Jangan sediakan endpoint moderasi publik.
- Terapkan perlindungan berlapis: Turnstile diverifikasi di server, honeypot, pembatasan frekuensi, dan penolakan tautan/promosi. Perlindungan otomatis membantu menyaring kiriman; keputusan tayang tetap melalui moderasi manual.
- Umpan balik satu klik cukup disimpan sebagai jumlah agregat; jangan kaitkan pilihan dengan nama atau isi komentar.
- Tampilkan pengingat agar pembaca tidak mengirim NIP, nomor rekening, kata sandi, token, dokumen internal, tautan privat, atau data pribadi. Render kiriman sebagai teks biasa, bukan HTML.
- Simpan hanya data yang diperlukan. Jangan simpan IP mentah untuk moderasi; gunakan hash berjangka pendek hanya untuk pembatasan kiriman dan bersihkan data pembatas lama. Jelaskan pemrosesan data di halaman Privasi.
- Jelaskan retensi sesuai mekanisme pembersihan yang benar-benar berjalan. Jika pembersihan dipicu saat endpoint diakses, jangan menjanjikan penghapusan pada jadwal otomatis yang tidak tersedia.
- Masukan kebijakan atau praktik dari pembaca tidak boleh dilabeli “terverifikasi” sebelum editor memeriksa sumber primer dan reproduksibilitasnya.

## Integrasi artikel dengan homepage

- Artikel baru hanya boleh masuk homepage melalui record yang berstatus approved dan PUBLISHED; jangan menambahkan kartu manual untuk artikel draft atau prototipe.
- Gunakan gambar hero artikel yang sama pada kartu homepage. Jangan membuat atau mengarang kategori, tanggal, maupun waktu baca: tanggal ditampilkan dalam format Indonesia, waktu baca hanya ditampilkan bila ada datanya, dan label kategori diambil dari kicker artikel bila tersedia.
- Pastikan kartu menampilkan judul dan ringkasan yang sesuai isi, tautannya menuju slug artikel yang benar, serta semua aset hero tersedia pada build publik.
- Filter topik homepage harus menggunakan tombol yang dapat diakses keyboard, menunjukkan status aktif, dan hanya memfilter kartu yang benar-benar tampil. Tanpa JavaScript, kontrol filter harus tetap tersembunyi agar tidak tampak sebagai fitur yang rusak.
- Jaga susunan kartu tetap seimbang pada desktop serta responsif di tablet dan ponsel. Bila jumlah kartu menghasilkan baris terakhir yang pendek, tata letaknya boleh diseimbangkan tanpa mengubah urutan editorial.
- Homepage harus memiliki canonical, deskripsi, Open Graph termasuk og:image, serta Twitter Card summary_large_image. Gambar sosial wajib ada di build publik dan teks alternatifnya menjelaskan visual secara ringkas.
- Uji kartu yang dibentuk otomatis, seluruh filter topik, metadata sosial, aset gambar, dan tampilan responsive melalui public-build regression test. Catat hasil quality gate sebelum rilis.

## SEO dan structured data

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
- [ ] Tautan kontekstual dan kartu Artikel terkait mengarah ke halaman relevan yang tersedia; hero kartu berhasil dimuat
- [ ] Umpan balik dan formulir komentar tampil tanpa login/email, peringatan data sensitif dan tautan privasi tersedia, Turnstile termuat
- [ ] Uji kiriman tak aman ditolak; komentar menunggu moderasi dan hanya komentar approved yang tampil
- [ ] Mobile readability diperiksa
- [ ] Build lulus, fungsi interaksi dan tautan diperiksa pada domain produksi setelah rilis
- [ ] Evidence review dan publication approval terpenuhi secara terpisah

**Gerbang rilis:** SOP gaya tidak menggantikan validasi sumber dan otorisasi publikasi. Review independen dapat diminta bila bermanfaat, tetapi bukan prasyarat. Untuk klaim berdampak tinggi, pemilik situs tetap wajib mencatat keputusan GO manusia yang terikat ke revisi final.
