# Moderasi komentar pembaca

Komentar publik ASN Pemda tidak memerlukan akun dan tidak tampil otomatis. Kiriman baru berstatus `pending`; hanya baris yang disetujui yang dibaca endpoint publik.

## Standar keputusan

- **Setujui** komentar yang relevan, sopan, tidak memuat data pribadi/rahasia, tidak mempromosikan layanan, dan tidak mengandung klaim yang berpotensi menyesatkan tanpa sumber.
- **Tolak** spam, tautan/ajakan promosi, penipuan, ujaran menyerang, data sensitif, atau komentar di luar konteks.
- Jangan mengubah komentar pembaca menjadi kesimpulan editorial. Jika memuat fakta kebijakan, verifikasi melalui sumber primer sebelum mengutip di artikel.
- Hapus atau tolak data sensitif sesegera mungkin. Jangan menyalinnya ke artikel, laporan, atau tangkapan layar.

## Operasi antrean

Gunakan Cloudflare D1 database `asnpemda-reader-comments` pada binding `COMMENTS_DB`. Jangan membuka endpoint moderasi publik. Untuk meninjau antrean, jalankan query read-only berikut melalui Cloudflare D1:

```sql
SELECT id, article_slug, display_name, comment_text, created_at
FROM reader_comments
WHERE status = 'pending'
ORDER BY created_at ASC;
```

Setelah keputusan editorial, perbarui satu komentar berdasarkan ID yang diperiksa:

```sql
UPDATE reader_comments
SET status = 'approved'
WHERE id = ? AND status = 'pending';
```

atau:

```sql
UPDATE reader_comments
SET status = 'rejected'
WHERE id = ? AND status = 'pending';
```

Selalu gunakan parameter binding untuk ID. Jangan menampilkan antrean `pending` atau `rejected` ke publik. Komentar `pending` dihapus otomatis setelah 90 hari, komentar `rejected` setelah 30 hari, dan komentar `approved` setelah paling lama satu tahun. Ringkasan suara pembaca hanya berupa jumlah “membantu” dan “belum membantu”; sistem tidak menyimpan nama atau komentar untuk pilihan tersebut.
