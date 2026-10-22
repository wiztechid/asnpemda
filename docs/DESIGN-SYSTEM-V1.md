# ASN Pemda — Design System & Template Baku v1.0 (2026-10-20)

Status: **BASELINE / FROZEN untuk struktur visual**, perubahan hanya melalui revisi versi setelah QC. Berlaku untuk homepage, artikel baru, halaman rubrik, dan komponen navigasi.

## Identitas
- Positioning: teman baca kebijakan ASN/pemda; independen, bukan kanal resmi.
- Bahasa: Indonesia sehari-hari, hangat, ringkas, sesama ASN. Hindari jargon tanpa penjelasan. Tidak clickbait, tidak membuat kepastian hukum palsu.
- Warna: royal blue #355CF6, navy #14224A, lavender #7754E8, coral #F17B53, kuning #FFC96D, latar #F8F9FF, putih.
- Font: Plus Jakarta Sans (judul) dan DM Sans (isi), fallback system-ui.
- Bentuk: radius 12–28px, whitespace lega, kartu modular, kontras tinggi, navigasi konsisten.

## Struktur homepage yang dibakukan
1. Info strip dan navigasi brand.
2. Hero editorial dengan janji manfaat dan CTA.
3. Tiga nilai: sumber resmi, dampak, langkah praktis.
4. Artikel unggulan yang **sudah terbit**, status aturan jelas.
5. Rubrik topik (tidak menampilkan konten fiktif).
6. Metodologi sumber dan editorial.
7. Footer independensi.

## Template artikel wajib
1. Breadcrumb + kategori + tanggal publikasi/perubahan faktual.
2. Judul natural berbasis intent pembaca.
3. Ringkasan 3 kalimat: apa berubah, siapa terdampak, apa tindakan.
4. Badge status: WACANA RESMI / RANCANGAN / TERBIT / BERLAKU / DIUBAH / DICABUT. Jangan memberi badge TERBIT tanpa regulasi.
5. Bagian 'Versi gampangnya', 'Apa yang berubah?', 'Dampak buat ASN', 'Dampak buat pemda/BPKAD', 'Perlu ngapain?', 'Yang belum pasti', dan 'Sumber resmi'.
6. Referensi primer berupa URL sumber dan tanggal akses; nomor aturan dan tanggal efektif bila tersedia.
7. Riwayat pembaruan hanya untuk perubahan substantif; satu isu satu URL canonical.
8. Disclaimer: bukan instruksi resmi; cek ketentuan instansi.

## QC sebelum publish
- Mobile 360px, tablet 768px, desktop 1440px tanpa overflow horizontal.
- Kontras teks, fokus keyboard, label aksesibel, gambar dengan alt, link tidak mati.
- H1 tunggal, metadata deskripsi, canonical sesuai URL publik, struktur heading logis.
- Semua angka, tanggal, status hukum, dan kutipan diverifikasi ke sumber primer.
- Tidak mengarang berita atau mengulang artikel; tidak mengubah template ketika menerbitkan artikel baru.
- Tidak ada promosi berlebihan, auto-play, atau iklan mengganggu.

## Change control
Perubahan artikel hanya mengisi slot konten. Perubahan layout global perlu proposal, screenshot before/after, QC mobile, dan kenaikan versi v1.1 dst. Jangan mengubah struktur frozen diam-diam.

## Penegasan freeze artikel (22 Oktober 2026)
- **Referensi struktur HTML artikel yang dibekukan:** `artikel/permenpanrb-9-2026-pppk-paruh-waktu.html` (header, navigasi, footer 3 kolom, metadata, komponen engagement, sumber, penulis, share, related posts). Artikel baru tidak boleh menggunakan footer satu baris atau header alternatif.
- **Hero editorial wajib:** rasio intrinsik 1200 × 675, alt deskriptif, tampilan utuh tanpa crop (`height:auto;object-fit:contain`). Gaya visual yang diminta: ilustrasi low-poly/geometris; jangan mengganti gaya menjadi foto atau kartun 3D tanpa persetujuan.
- **Publication gate:** `data/articles/<slug>.json` harus approved dan PUBLISHED; aset hero harus termasuk dalam build allowlist. Deploy sukses dan inspeksi URL publik adalah bagian dari QC.
- **SOP konten:** artikel mendalam minimal 900 kata bila topik memungkinkan, sumber primer, SERP intent, status hukum terverifikasi, dan tidak mengarang mekanisme. Jangan klaim lulus QC mobile tanpa pengujian nyata.
- **Change control:** jangan mengubah desain frozen secara ad hoc. Perubahan layout global harus diajukan sebagai revisi versi, bukan ditimpa per artikel.

## Master Template Artikel — Referensi WFH (22 Oktober 2026)
- **MASTER VISUAL:** `artikel/aturan-wfh-asn-pemda-2026-se-mendagri-4412-sj.html` sesuai screenshot yang disetujui pengguna. Ini menggantikan contoh referensi PPPK sebagai acuan utama layout; jangan membuat HTML/CSS artikel dari nol.
- Urutan wajib: breadcrumb → kicker/judul/deck/metadata → hero utuh → status resmi → versi gampangnya → tiga manfaat → daftar isi → artikel >900 kata bila layak → sumber → artikel terkait/blogroll → feedback/komentar → penulis → share → footer tiga kolom.
- **Pemisahan konten dan desain:** artikel baru menggunakan class `article-page`, `article-content`, `article-hero`, `status-card`, `quick-answer`, `toc`, `article-body`, `related-posts`, `reader-engagement`, `author-box`, `share-panel`, `site-footer`; hindari CSS inline yang menduplikasi desain global.
- **Blogroll:** otomatis dari artikel berstatus approved/PUBLISHED pada build, tidak perlu edit setiap artikel. Jangan tampilkan tautan draft.
- **Freeze:** modifikasi layout global memerlukan proposal versi, QC responsif 360/768/1440, cek footer, gambar, aksesibilitas, tautan, dan hasil build. Perbaikan teks artikel boleh tanpa perubahan layout.

## 🔒 FROZEN — Master Artikel ASN Pemda v1.1 (22 Oktober 2026)
**Keputusan pemilik:** layout artikel terakhir disetujui dan dibekukan sebagai acuan artikel baru. Acuan visual: artikel WFH ASN Pemda; acuan perbaikan terkini: artikel sertifikasi PBJ Level-1 dan PPK Tipe C.

**Komponen wajib dan urutan:** breadcrumb → judul/deck/metadata → hero low-poly utuh (tanpa crop) → status regulasi → ringkasan → tiga kartu manfaat sejajar di desktop / satu kolom di ponsel → daftar isi → isi dan sumber resmi → **satu** blok Bacaan selanjutnya (maksimal tiga artikel approved/PUBLISHED, tanpa duplikasi) → feedback/komentar → penulis → berbagi → footer lengkap.

**Perubahan rutin yang diizinkan:** judul, slug, tanggal, metadata, konten, rujukan, gambar pada slot hero, kategori, dan rekomendasi artikel berdasarkan relevansi. **Dilarang** mengubah CSS global, struktur/urutan komponen, header, footer, tata letak tiga kartu, atau menambah blok rekomendasi kedua saat update artikel.

**Kontrol:** `scripts/build_site.py` menjaga struktur dasar master dan publication gate. Pengubahan master harus atas persetujuan eksplisit pemilik, revisi versi, review diff, regression test build, serta QC visual desktop/mobile. Freeze ini merupakan aturan proyek; bukan jaminan visual pixel-perfect otomatis.

## Editorial Voice v1.0 — ASN Milenial & Gen Z (22 Oktober 2026)

**Audiens utama:** ASN/CPNS/PPPK generasi milenial dan Gen Z di pemerintah daerah. **Positioning:** teman baca kebijakan yang cerdas, ringan, dekat dengan keseharian OPD, dan tetap berpegang pada sumber primer.

- Gunakan bahasa Indonesia populer-profesional; hangat, ringkas, tidak menggurui. Boleh menggunakan pertanyaan pembuka, analogi pekerjaan kantor, dan kalimat seperti “Apa dampaknya buat kita di OPD?” Hindari bahasa birokratis bertele-tele, jargon tanpa penjelasan, slang yang cepat basi, serta clickbait yang melebih-lebihkan.
- Judul harus menjawab intent pembaca dan memuat topik/aturan relevan. Lead maksimal 2 paragraf pendek: apa yang baru, status resminya, dan mengapa penting. Paragraf ideal 2–4 kalimat; gunakan subjudul berbentuk pertanyaan, contoh konkret, checklist tindakan, dan FAQ yang tidak mengulang isi.
- Struktur artikel mengikuti **master template v1.1 FROZEN**; ubah **copywriting saja**, jangan mengubah layout, CSS, komponen, header/footer, atau urutan. Gunakan kartu “Yang berubah / Siapa terdampak / Perlu dilakukan” untuk informasi paling praktis.
- **Akurasi wajib:** bedakan RESMI/TERBIT, RANCANGAN, ARAH KEBIJAKAN, dan WACANA RESMI. Cantumkan nomor/tanggal aturan bila terverifikasi, pihak terdampak, tanggal efektif/tenggat, konsekuensi praktis, dan tautan sumber primer. Jangan mengarang hak, kewajiban, konversi otomatis, atau kepastian yang belum ada.
- **SEO dan kualitas:** riset intent SERP dan sumber primer; artikel mendalam idealnya minimal 900 kata jika topik layak, tetapi tetap mudah dipindai. Jangan memanjangkan paragraf hanya demi target kata; informasi yang sama tidak boleh diulang. Internal link ke artikel yang benar-benar terkait.
- **Quality Gate bahasa:** sebelum publish, cek keterbacaan di ponsel, konsistensi istilah, ketepatan hukum, kejelasan tindakan, minim repetisi, dan apakah pembaca ASN dapat memahami inti artikel dalam 30 detik pertama.

## SEO Editorial Gate v1.1 — Search Demand First (22 Oktober 2026)
- **Panjang artikel:** minimal **lebih dari 700 kata isi utama** (target operasional >= 701 kata; tidak menghitung menu, footer, blogroll, dan metadata). Rentang ideal 900–1.200 kata bila topik cukup kaya; dilarang filler dan pengulangan.
- **Keyword harus memiliki bukti demand:** sebelum drafting, riset SERP Indonesia, intent, autocomplete/PAA sebagai sinyal awal; prioritas keyword dengan metrik rata-rata pencarian bulanan terverifikasi dari Google Keyword Planner, Google Ads API, atau alat SEO tepercaya. Catat angka, periode, geografi, dan sumber. Jangan mengklaim volume berdasarkan autocomplete/PAA saja.
- **Prioritas keyword:** relevan ASN/CPNS/PPPK/Pemda, sesuai berita resmi, long-tail berintensi jelas, kompetisi organik realistis. Angka 'competition' Keyword Planner adalah kompetisi iklan, bukan kesulitan ranking organik.
- **Brief wajib sebelum publish:** keyword utama, 3–6 turunan, search intent, bukti demand dan tanggal cek, analisis 5–10 hasil SERP, content gap, judul SEO, slug, meta description, H1/H2, FAQ relevan, internal link, dan sumber primer.
- **Publication gate:** bila volume tidak tersedia, tandai 'demand belum terverifikasi' dan jangan labeli sebagai keyword tervalidasi. Artikel berita material tetap boleh dipertimbangkan melalui keputusan editorial eksplisit, tanpa mengarang volume.
- **Gaya:** ASN milenial dan Gen Z; bahasa ringan, paragraf pendek, contoh kasus OPD, tetap tepat hukum. Master template visual v1.1 tetap FROZEN.
