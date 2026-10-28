/* ASN Pemda — kalkulator potongan SPM/SP2D DEV v0.1
 * Asumsi: transaksi domestik, satu jenis objek per simulasi.
 * Untuk telaah SPJ saja, bukan penetapan resmi atau bukti potong.
 */
export const RATES = Object.freeze({
  goods: {normal: 0.015},
  service: {npwp: 0.02, noNpwp: 0.04},
  construction: {
    worksSmall: 0.0175, worksOther: 0.0265, worksNoCert: 0.04,
    integratedCert: 0.0265, integratedNoCert: 0.04,
    consultantCert: 0.035, consultantNoCert: 0.06
  },
  rentBuilding: 0.10,
  pnsHonor: {I_II: 0, III: 0.05, IV: 0.15}
});
const num = v => Number.isFinite(Number(v)) ? Math.max(0, Number(v)) : 0;
export const rupiah = n => 'Rp' + Math.round(num(n)).toLocaleString('id-ID');
export const tax17 = n => {
  let rest = num(n), tax = 0;
  for (const [band, rate] of [[60000000,.05],[190000000,.15],[250000000,.25],[4500000000,.30],[Infinity,.35]]) {
    const x = Math.min(rest, band);
    if (x <= 0) break;
    tax += x * rate; rest -= x;
  }
  return Math.round(tax);
};
const warning = (alerts, message) => alerts.push(message);

export function calculate(raw = {}) {
  const a = {...raw}, alerts = [], labels = [];
  const total = num(a.amount), vatRate = a.vatMode === 'regular' ? 0.11 : a.vatMode === 'luxury' ? 0.12 : 0;
  const included = a.amountMode === 'inclusive';
  const base = included && vatRate ? Math.round(total / (1 + vatRate)) : Math.round(total);
  const vat = vatRate ? (included ? Math.max(0, Math.round(total - base)) : Math.round(base * vatRate)) : 0;
  const invoice = included ? Math.round(total) : Math.round(base + vat);
  let pph = 0, taxName = '', taxBase = base, rateLabel = '', taxExplain = '', blocked = false;
  if (total <= 0) { warning(alerts,'Isi nilai pembayaran lebih dari Rp0.'); blocked = true; }
  if (!a.vatMode || a.vatMode === 'unselected') { warning(alerts,'Tentukan apakah transaksi terutang PPN. Jangan menganggap otomatis tidak kena PPN.'); blocked = true; }
  if (a.vatMode === 'special') { warning(alerts,'PPN dengan DPP nilai lain/besaran tertentu khusus perlu verifikasi faktur. Kalkulasi belum bisa difinalisasi.'); blocked = true; }
  if (a.vatMode === 'luxury') { warning(alerts,'BKP mewah/PPnBM memerlukan hitungan tambahan; kalkulator ini tidak menetapkan nominal akhir.'); blocked = true; }
  if (['kkpd','upMarketplace'].includes(a.paymentMethod)) { warning(alerts,'Untuk belanja KKPD atau UP melalui Pihak Lain, gunakan kalkulator E-Katalog agar pemungut PPh 22/PPN tidak tertukar atau terpotong ganda.'); blocked = true; }
  if (a.pkpStatus === 'unknown' && a.vatMode === 'regular') { warning(alerts,'Pastikan penyedia benar-benar PKP sebelum memasukkan PPN; pilih status PKP di formulir.'); blocked = true; }
  if (a.pkpStatus === 'no' && a.vatMode === 'regular') { warning(alerts,'Penyedia non-PKP tidak boleh otomatis menagih PPN seperti PKP. Periksa faktur dan objek.'); blocked = true; }
  if (a.recipientTaxId === 'unknown' && ['goods','services','honor','rentMovable'].includes(a.category)) {
    warning(alerts,'Status NPWP/NIK penerima belum terverifikasi. Hasil PPh ditahan sampai status pajaknya jelas.');
    blocked = true;
  }
  switch (a.category) {
    case 'goods': {
      taxName = 'PPh Pasal 22'; rateLabel = '1,5% × nilai sebelum PPN';
      const ex = a.goodsException;
      if (base <= 2000000 && !a.splitContract) { pph = 0; rateLabel='Tidak dipungut'; taxExplain = 'Tidak dipungut: transaksi paling banyak Rp2 juta (tidak termasuk PPN), bukan pemecahan transaksi.'; }
      else if (a.paymentMethod === 'kkpd' || a.paymentMethod === 'upMarketplace' || (ex && ex !== 'none')) { pph = 0; rateLabel='Tidak dipungut oleh instansi'; taxExplain = 'Tidak dipungut oleh instansi pada mekanisme/kondisi pengecualian yang dipilih; periksa bukti pemungutan pihak lain.'; }
      else { const pct = a.recipientTaxId === 'no' ? 0.03 : RATES.goods.normal; pph = Math.round(base * pct); rateLabel = (pct * 100).toLocaleString('id-ID') + '% × nilai sebelum PPN'; taxExplain = 'PMK 51/2025: pembelian barang oleh instansi pemerintah (di luar pengecualian).'; }
      if (a.splitContract) warning(alerts,'Transaksi dipecah: ambang Rp2 juta harus diuji berdasarkan nilai transaksi sebenarnya.');
      if (ex === 'skb') warning(alerts,'Wajib verifikasi salinan SKB atau surat keterangan yang masih berlaku sebelum membebaskan PPh 22.');
      if (ex === 'kkpd' && a.paymentMethod !== 'kkpd') { blocked = true; warning(alerts,'Pengecualian KKPD hanya bisa digunakan untuk mekanisme kartu kredit pemerintah.'); }
      if (a.recipientTaxId === 'no') warning(alerts,'PPh 22 tanpa NPWP menggunakan tarif lebih tinggi 100% jika pemungutan berlaku; cek identitas pajak.');
      break;
    }
    case 'services':
    case 'rentMovable': {
      if (a.category === 'services' && a.payeeType === 'person') {
        taxName = 'PPh Pasal 21 (Bukan Pegawai)';
        taxBase = Math.round(base * 0.5);
        const prior = num(a.priorDpp), priorTax = tax17(prior);
        pph = Math.max(0,tax17(prior + taxBase) - priorTax);
        if (a.recipientTaxId === 'no') { pph = Math.round(pph * 1.2); rateLabel += ' (+20% jika tanpa NPWP)'; warning(alerts,'PPh 21 nonfinal tanpa NPWP/NIK yang sah: tarif pemotongan 20% lebih tinggi dari hasil normal.'); }
        rateLabel = prior + taxBase <= 60000000 ? 'Tarif 5% (Pasal 17) × DPP 50% bruto, bukan TER' : 'Tarif progresif Pasal 17 × DPP 50% bruto, bukan TER';
        taxExplain = 'Profesi/jasa orang pribadi (bukan pegawai), bukan PPh 23; bukan TER.';
        if (prior > 0) warning(alerts,'DPP terdahulu yang dimasukkan harus sesuai masa pajak dan ketentuan pemotongan relevan.');
      } else {
        taxName = 'PPh Pasal 23';
        const pct = a.recipientTaxId === 'no' ? RATES.service.noNpwp : RATES.service.npwp;
        rateLabel = (pct * 100).toLocaleString('id-ID') + '% × jumlah bruto sebelum PPN';
        pph = Math.round(base * pct);
        taxExplain = 'Jasa/sewa harta selain tanah-bangunan yang merupakan objek PPh 23; tidak termasuk jasa konstruksi final.';
        if (a.recipientTaxId === 'no') warning(alerts,'Tarif PPh 23 lebih tinggi karena NPWP tidak tersedia; pastikan validasi identitas dan ketentuan yang berlaku.');
      }
      break;
    }
    case 'construction':
      taxName = 'PPh Final Pasal 4 ayat (2)';
      if (!Object.prototype.hasOwnProperty.call(RATES.construction, a.constructionType)) {
        warning(alerts,'Pilih klasifikasi jasa konstruksi yang sesuai dokumen SBU/SKK.'); blocked = true;
      } else {
        const pct = RATES.construction[a.constructionType];
        pph = Math.round(base * pct);
        rateLabel = (pct * 100).toLocaleString('id-ID') + '% × nilai pembayaran sebelum PPN';
        taxExplain = 'PP 9/2022: jenis pekerjaan dan status sertifikasi menentukan tarif final.';
      }
      warning(alerts,'Uji klasifikasi pekerjaan, SBU/SKK, termin, retensi, uang muka dan faktur pajak. Kontrak campuran harus dipisahkan.');
      break;
    case 'rentBuilding':
      taxName = 'PPh Final Pasal 4 ayat (2)';
      pph = Math.round(base * RATES.rentBuilding);
      rateLabel = '10% × bruto sewa sebelum PPN';
      taxExplain = 'Sewa tanah/bangunan final. Bruto sewa dapat mencakup biaya layanan terkait.';
      break;
    case 'honor': {
      if (a.honorType === 'nonemployee') {
        taxName = 'PPh Pasal 21 — Bukan Pegawai';
        taxBase = Math.round(base * 0.5);
        const prior = num(a.priorDpp);
        pph = Math.max(0,tax17(prior + taxBase) - tax17(prior));
        if (a.recipientTaxId === 'no') { pph = Math.round(pph * 1.2); rateLabel += ' (+20% jika tanpa NPWP)'; warning(alerts,'PPh 21 nonfinal tanpa NPWP/NIK yang sah: tarif pemotongan 20% lebih tinggi dari hasil normal.'); }
        rateLabel = prior + taxBase <= 60000000 ? 'Tarif 5% (Pasal 17) × DPP 50% bruto, bukan TER' : 'Tarif progresif Pasal 17 × DPP 50% bruto, bukan TER';
        taxExplain = 'Narasumber, penerjemah, dan profesional orang pribadi yang bukan pegawai.';
      } else if (a.honorType === 'participant') {
        taxName = 'PPh Pasal 21 — Peserta Kegiatan';
        const prior = num(a.priorDpp);
        pph = Math.max(0,tax17(prior + base) - tax17(prior));
        if (a.recipientTaxId === 'no') { pph = Math.round(pph * 1.2); rateLabel += ' (+20% jika tanpa NPWP)'; warning(alerts,'PPh 21 nonfinal tanpa NPWP/NIK yang sah: tarif pemotongan 20% lebih tinggi dari hasil normal.'); }
        rateLabel = 'Tarif Pasal 17 × bruto (bukan TER)';
        taxExplain = 'Imbalan atas keikutsertaan kegiatan, bukan jasa profesional sebagai Bukan Pegawai.';
      } else if (a.honorType === 'pns') {
        if (!(a.pnsGroup in RATES.pnsHonor)) { blocked = true; warning(alerts,'Pilih golongan PNS yang sesuai dokumen kepegawaian.'); }
        else {
          const pct = RATES.pnsHonor[a.pnsGroup];
          taxName = 'PPh Pasal 21 Final — Honor PNS APBD';
          pph = Math.round(base * pct);
          rateLabel = (pct*100).toLocaleString('id-ID') + '% × bruto';
          taxExplain = 'PP 80/2010, hanya honorarium atau imbalan lain yang memenuhi syarat khusus dari APBN/APBD.';
        }
      } else {
        blocked = true; warning(alerts,'Pilih status honorarium agar penentuan pajak tidak salah.');
      }
      if (a.honorType !== 'pns' && num(a.priorDpp) > 0) warning(alerts,'Pastikan DPP sebelumnya benar; progresivitas Pasal 17 dapat mengubah hasil.');
      break;
    }
    default:
      blocked = true; warning(alerts,'Pilih kategori pembayaran.');
  }
  if (a.category === 'honor' && vatRate) { blocked = true; warning(alerts,'Honorarium orang pribadi bukan transaksi PKP biasa; hapus PPN atau verifikasi sifat pengadaannya.'); }
  if (a.category === 'goods' && a.payeeType === 'person') warning(alerts,'Pastikan pembelian benar-benar barang, bukan jasa orang pribadi, untuk memilih PPh 22.');
  const method = a.vatCollector || 'auto';
  let collector = 'Tidak ada PPN', vatGov = 0;
  if (vat > 0) {
    const autoGov = base > 2000000 || !!a.splitContract;
    const isGov = method === 'government' || (method === 'auto' && autoGov && !['kkpd','upMarketplace'].includes(a.paymentMethod));
    collector = isGov ? 'Instansi pemerintah' : method === 'thirdparty' ? 'Pihak lain' : 'Rekanan/pihak lain (bukan dipungut instansi)';
    if (isGov) vatGov = vat;
    if (method === 'government' && base <= 2000000 && !a.splitContract) warning(alerts,'PPN biasanya tidak dipungut instansi untuk transaksi ≤ Rp2 juta; periksa pengecualian.');
    if (method === 'auto' && a.paymentMethod === 'kkpd') warning(alerts,'Kartu kredit pemerintah: perlakuan pemungutan PPN/PPh oleh instansi dapat dikecualikan; periksa mekanisme platform.');
    if (method === 'auto' && a.paymentMethod === 'upMarketplace') warning(alerts,'Belanja UP melalui pihak lain/platform dapat memiliki pemungut PPN/PPh sendiri: verifikasi bukti.');
  }
  if (a.paymentMethod === 'upMarketplace' && a.category === 'goods' && a.goodsException !== 'alreadyCollected')
    warning(alerts,'Bila PPh 22 sudah dipungut Pihak Lain, pilih pengecualian khusus agar tidak memungut dua kali.');
  const retention = num(a.retention), advance = num(a.advance), penalty = num(a.penalty), misc = num(a.other);
  const nonTax = Math.round(retention + advance + penalty + misc);
  const payout = invoice - pph - vatGov - nonTax;
  if (nonTax > 0) warning(alerts,'Retensi, angsuran uang muka, denda dan potongan lain bersifat simulasi kas; dasar pengenaan pajaknya harus dicocokkan dengan kontrak dan bukti transaksi.');
  if (payout < 0) { blocked = true; warning(alerts,'Total potongan melebihi nilai tagihan. Periksa data.'); }
  if (a.vatMode === 'regular') warning(alerts,'PPN nonmewah umumnya 12% × DPP nilai lain 11/12 (= 11% harga). Skema khusus PMK 11/2025 tidak dihitung otomatis.');
  if (a.vatMode === 'luxury') warning(alerts,'Tarif 12% penuh hanya pada penyerahan yang benar-benar memenuhi kategori barang mewah; PPnBM tidak dihitung.');
  if (blocked) { pph = null; vatGov = null; }
  return {
    ok: !blocked, invoice, base, vat, vatGov, collector, pph, taxName, taxBase,
    rateLabel, taxExplain, nonTax, retention, advance, penalty, misc,
    payout: blocked ? null : Math.max(0,payout), alerts, labels
  };
}
