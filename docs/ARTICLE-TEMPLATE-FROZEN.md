# Master Template Artikel ASN Pemda — FROZEN

Status: FROZEN  
Scope: every published article under `artikel/`  
Visual source of truth: `assets/article-template.css` and `assets/article-insights.css`

## Struktur wajib

Urutan modul halaman harus tetap seperti berikut:

1. `main.article-page`
2. Breadcrumb
3. `article.article-content`
4. Header artikel: kicker, satu H1, deck, dan metadata
5. Hero 16:9 dengan alt text dan caption
6. Status aturan
7. Jawaban singkat dalam satu elemen `section.quick-answer` yang memiliki heading
8. Tepat tiga kartu ringkasan dalam `div.takeaways`; setiap kartu memakai strong dan paragraf
9. Daftar isi yang seluruh tautannya cocok dengan ID bagian yang tersedia
10. Isi utama dalam `div.article-body`
11. Bacaan terkait
12. Feedback pembaca
13. Panel berbagi
14. Footer situs

Komponen khusus seperti kalkulator tetap boleh ada di isi artikel. Komponen tersebut harus memakai kelas yang spesifik, tidak mengubah urutan modul utama, dan tidak membawa CSS inline sendiri.

## Aturan visual dan HTML

- Semua artikel menggunakan satu stylesheet bersama `../assets/article-template.css`; sorotan subjudul menggunakan stylesheet `article-insights.css` dari proses build.
- Dilarang menyimpan blok `<style>` inline, menggandakan tautan `site.css`, atau membuat variasi CSS shell per artikel.
- Jangan gunakan struktur ringkasan lama `fact-grid`; gunakan tiga kartu `takeaways`.
- Gunakan satu H1, satu hero, satu jawaban singkat, satu daftar isi, satu isi utama, dan tepat satu dari setiap modul wajib.
- ID elemen harus unik. Setiap tautan daftar isi wajib memiliki target.
- Isi artikel dan komponen khusus tidak boleh mengubah template visual bersama tanpa pembaruan dokumen ini dan regression test.

## Quality Gate

Build menolak artikel jika modul wajib hilang atau berulang, urutan berubah, CSS inline ditemukan, stylesheet bersama tidak ada/duplikat, ringkasan tidak tepat tiga kartu, atau tautan daftar isi rusak. Regression test memeriksa seluruh artikel terbit dalam output publik sebelum merge/deploy.

Template hanya berubah melalui PR yang memperbarui dokumen ini, CSS bersama, dan tes terkait. Artikel baru wajib mengikuti master ini sebelum dinyatakan siap terbit.
