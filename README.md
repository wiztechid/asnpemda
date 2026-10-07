# ASN Pemda

**ASN Pemda** adalah portal intelligence independen untuk ASN/CPNS dan pengelola pemerintahan daerah Indonesia. Fokusnya bukan mengejar berita tercepat, tetapi menjawab: **apa yang berubah, status hukumnya apa, siapa terdampak, dan apa yang perlu dilakukan?**

## Prinsip
- **Primary-source first**: JDIH/regulasi dan kanal resmi pemerintah menjadi sumber utama.
- **Status jelas**: RUMOR → WACANA RESMI → RANCANGAN → TERBIT → BERLAKU → DIUBAH/DICABUT.
- **ASN Lens + Pemda Lens**: dampak untuk pegawai dipisahkan dari dampak operasional Pemda.
- **Living Policy Article**: satu isu utama memiliki satu URL canonical yang diperbarui saat ada delta material.
- **No fake freshness**: `dateModified` hanya berubah jika substansi berubah.
- **Anti-duplikat & cannibalization guard**.
- **Human publication gate** untuk interpretasi hukum/keuangan berisiko tinggi.

## Cakupan
ASN/CPNS & kesejahteraan; karier/manajemen talenta; perencanaan; APBD; SIPD & penatausahaan; PBJ; BLUD; audit, pertanggungjawaban & pelaporan.

## GitHub Mode Hemat
CI ringan berjalan untuk perubahan rutin. Deep audit/full regression/rebuild massal dijalankan **on-demand setelah satu batch substantif selesai**, bukan setiap commit kecil.

## Status
Foundation v0.1 — kontrak editorial, evidence, living-policy, dan CI ringan.
