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
  pnsHonor: {I_II: 0, III: 0.05, IV: 0.15},
  pph21Daily: {zeroUpTo: 450000, terUpTo: 2500000, terRate: 0.005}
});
// Batas penghasilan bruto bulanan dari Lampiran PP 58/2023 (di atas batas ini).
const TER = Object.freeze({
  A: [[0,0],[5400000,.0025],[5650000,.005],[5950000,.0075],[6300000,.01],[6750000,.0125],[7500000,.015],[8550000,.0175],[9650000,.02],[10050000,.0225],[10350000,.025],[10700000,.03],[11050000,.035],[11600000,.04],[12500000,.05],[13750000,.06],[15100000,.07],[16950000,.08],[19750000,.09],[24150000,.10],[26450000,.11],[28000000,.12],[30050000,.13],[32400000,.14],[35400000,.15],[39100000,.16],[43850000,.17],[47800000,.18],[51400000,.19],[56300000,.20],[62200000,.21],[68600000,.22],[77500000,.23],[89000000,.24],[103000000,.25],[125000000,.26],[157000000,.27],[206000000,.28],[337000000,.29],[454000000,.30],[550000000,.31],[695000000,.32],[910000000,.33],[1400000000,.34],[Infinity,.34]],
  B: [[0,0],[6200000,.0025],[6500000,.005],[6850000,.0075],[7300000,.01],[9200000,.015],[10750000,.02],[11250000,.025],[11600000,.03],[12600000,.04],[13600000,.05],[14950000,.06],[16400000,.07],[18450000,.08],[21850000,.09],[26000000,.10],[27700000,.11],[29350000,.12],[31450000,.13],[33950000,.14],[37100000,.15],[41100000,.16],[45800000,.17],[49500000,.18],[53800000,.19],[58500000,.20],[64000000,.21],[71000000,.22],[80000000,.23],[93000000,.24],[109000000,.25],[129000000,.26],[163000000,.27],[211000000,.28],[374000000,.29],[459000000,.30],[555000000,.31],[704000000,.32],[957000000,.33],[1405000000,.34],[Infinity,.34]],
  C: [[0,0],[6600000,.0025],[6950000,.005],[7350000,.0075],[7800000,.01],[8850000,.0125],[9800000,.015],[10950000,.0175],[11200000,.02],[12050000,.03],[12950000,.04],[14150000,.05],[15550000,.06],[17050000,.07],[19500000,.08],[22700000,.09],[26600000,.10],[28100000,.11],[30100000,.12],[32600000,.13],[35400000,.14],[38900000,.15],[43000000,.16],[47400000,.17],[51200000,.18],[55800000,.19],[60400000,.20],[66700000,.21],[74500000,.22],[83200000,.23],[95600000,.24],[110000000,.25],[134000000,.26],[169000000,.27],[221000000,.28],[390000000,.29],[463000000,.30],[561000000,.31],[709000000,.32],[965000000,.33],[1419000000,.34],[Infinity,.34]]
});
const PTKP = Object.freeze({TK0:54000000,TK1:58500000,TK2:63000000,TK3:67500000,K0:58500000,K1:63000000,K2:67500000,K3:72000000});
const terRate = (group, gross) => {
  let selected = null;
  for (const [threshold, pct] of TER[group] || []) { if (gross > threshold) selected = pct; else break; }
  return selected;
};
const num = v => Number.isFinite(Number(v)) ? Math.max(0, Number(v)) : 0;
export const rupiah = n => 'Rp' + Math.round(num(n)).toLocaleString('id-ID');
export const tax17 = n => {
  let rest = Math.floor(num(n) / 1000) * 1000, tax = 0;
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
  const total = num(a.amount), vatRate = a.vatMode === 'regular' || a.vatMode === 'luxury' ? 0.12 : 0;
  const vatDppFactor = a.vatMode === 'regular' ? 11/12 : 1;
  const vatEffectiveRate = vatRate * vatDppFactor;
  const included = a.amountMode === 'inclusive';
  const base = included && vatRate ? Math.round(total / (1 + vatEffectiveRate)) : Math.round(total);
  const vat = vatRate ? (included ? Math.max(0, Math.round(total - base)) : Math.round(base * vatEffectiveRate)) : 0;
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
    case 'fixedEmployee': {
      taxName = 'PPh Pasal 21 — Pegawai Tetap';
      taxBase = base;
      if (!PTKP[a.ptkp]) { blocked = true; warning(alerts,'Pilih status PTKP awal tahun sesuai data payroll.'); }
      else if (a.employeePeriod === 'last') {
        const months = Number(a.jobMonths);
        if (!Number.isInteger(months) || months < 1 || months > 12) { blocked = true; warning(alerts,'Isi jumlah bulan bekerja yang benar (1–12).'); }
        if (a.partYear === 'yes') { blocked = true; warning(alerts,'Masa pajak bagian tahun memerlukan annualisasi dan prorata. Rekonsiliasi manual payroll diperlukan.'); }
        const grossYear = num(a.annualGross);
        if (grossYear <= 0) { blocked = true; warning(alerts,'Isi bruto setahun dari rekap payroll sebelum menghitung masa pajak terakhir.'); }
        const jobCost = Math.min(Math.round(grossYear * 0.05), 500000 * months);
        const otherDeduct = num(a.pensionYear) + num(a.zakatYear);
        const pkp = Math.max(0, grossYear - jobCost - otherDeduct - PTKP[a.ptkp]);
        const annualTax = tax17(pkp);
        pph = annualTax - num(a.priorWithheld);
        taxBase = pkp;
        rateLabel = `Masa terakhir: Pasal 17 atas PKP ${rupiah(pkp)} − PPh yang telah dipotong ${rupiah(a.priorWithheld)}`;
        taxExplain = `Rekonsiliasi tahunan. Biaya jabatan ${rupiah(jobCost)} (5% bruto, maks. Rp500.000 per bulan); dikurangi iuran pensiun/zakat melalui pemberi kerja ${rupiah(otherDeduct)} dan PTKP ${rupiah(PTKP[a.ptkp])}.`;
        if (pph < 0) { blocked = true; warning(alerts,'Pemotongan terdahulu melebihi PPh tahunan. Kekurangan setoran bukan potongan negatif; rekonsiliasi pengembalian melalui payroll sebelum menetapkan hasil.'); }
      } else {
        const group = a.ptkp === 'TK0' || a.ptkp === 'TK1' || a.ptkp === 'K0' ? 'A' : ['TK2','TK3','K1','K2'].includes(a.ptkp) ? 'B' : 'C';
        const pct = terRate(group, base);
        pph = Math.round(base * pct);
        rateLabel = `TER bulanan kategori ${group} ${(pct*100).toLocaleString('id-ID')}% × bruto bulanan`;
        taxExplain = `Pegawai tetap, masa pajak selain masa terakhir. Kategori ${group} mengikuti status PTKP awal tahun.`;
      }
      if (a.vatMode !== 'none') { blocked = true; warning(alerts,'Gaji/TPP pegawai bukan tagihan PKP. Pilih PPN tidak terutang/tidak dihitung.'); }
      break;
    }
    case 'temporaryDaily': {
      taxName = 'PPh Pasal 21 — Pegawai Tidak Tetap Harian';
      if (base <= RATES.pph21Daily.zeroUpTo) {
        pph = 0; rateLabel = '0% untuk bruto harian sampai dengan Rp450.000';
      } else if (base <= RATES.pph21Daily.terUpTo) {
        pph = Math.round(base * RATES.pph21Daily.terRate);
        rateLabel = 'TER harian 0,5% × bruto harian';
      } else {
        taxBase = Math.round(base * 0.5);
        pph = tax17(taxBase);
        rateLabel = '50% bruto × tarif progresif Pasal 17';
      }
      taxExplain = 'Pegawai tidak tetap yang menerima penghasilan harian: PP 58/2023 dan PMK 168/2023. Isi bruto untuk satu hari kerja. Skema pembayaran bulanan, borongan, atau satuan hasil tidak dicakup mode ini.';
      if (a.vatMode !== 'none') { blocked = true; warning(alerts,'Penghasilan pegawai bukan tagihan PKP. Pilih PPN tidak terutang/tidak dihitung.'); }
      break;
    }
    case 'goods': {
      taxName = 'PPh Pasal 22'; rateLabel = '1,5% × nilai sebelum PPN';
      const ex = a.goodsException;
      if (base <= 2000000 && !a.splitContract) { pph = 0; rateLabel='Tidak dipungut'; taxExplain = 'Tidak dipungut: transaksi paling banyak Rp2 juta (tidak termasuk PPN), bukan pemecahan transaksi.'; }
      else if (a.paymentMethod === 'kkpd' || a.paymentMethod === 'upMarketplace' || (ex && ex !== 'none')) { pph = 0; rateLabel='Tidak dipungut oleh instansi'; taxExplain = 'Tidak dipungut oleh instansi pada mekanisme/kondisi pengecualian yang dipilih; periksa bukti pemungutan pihak lain.'; }
      else { const pct = a.recipientTaxId === 'no' ? 0.03 : RATES.goods.normal; pph = Math.round(base * pct); rateLabel = (pct * 100).toLocaleString('id-ID') + '% × nilai sebelum PPN'; taxExplain = 'PMK 51/2025: pembelian barang oleh instansi pemerintah (di luar pengecualian).'; }
      if (a.splitContract) warning(alerts,'Transaksi dipecah: ambang Rp2 juta harus diuji berdasarkan nilai transaksi sebenarnya.');
      if (ex === 'skb') warning(alerts,'Wajib verifikasi salinan SKB atau surat keterangan yang masih berlaku sebelum membebaskan PPh 22.');
      if (ex === 'kkpd' && a.paymentMethod !== 'kkpd') { blocked = true; warning(alerts,'Pengecualian KKPD hanya bisa digunakan untuk mekanisme kartu kredit pemerintah.'); }
      if (['bos','rice'].includes(ex)) warning(alerts,'PPh 22 tidak dipungut untuk objek yang dipilih. Simpan bukti penggunaan dana BOS atau dokumen pembelian gabah/beras.');
      if (ex === 'sipdUP' && a.paymentMethod !== 'upMarketplace') { blocked = true; warning(alerts,'Pengecualian SIPD/UP memerlukan pemungutan oleh Pihak Lain yang ditunjuk dan bukti pemungutan transaksi.'); }
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
        if (a.recipientTaxId === 'no') { pph = Math.round(pph * 1.2); warning(alerts,'PPh 21 nonfinal tanpa NPWP/NIK yang sah: tarif pemotongan 20% lebih tinggi dari hasil normal.'); }
        rateLabel = prior + taxBase <= 60000000 ? 'Tarif 5% (Pasal 17) × DPP 50% bruto, bukan TER' : 'Tarif progresif Pasal 17 × DPP 50% bruto, bukan TER';
        taxExplain = 'Profesi/jasa orang pribadi (bukan pegawai), bukan PPh 23; bukan TER.';
        if (prior > 0) warning(alerts,'DPP terdahulu yang dimasukkan harus sesuai masa pajak dan ketentuan pemotongan relevan.');
      } else {
        taxName = 'PPh Pasal 23';
        if (a.category === 'services' && a.serviceException && a.serviceException !== 'none') {
          blocked = true;
          warning(alerts, a.serviceException === 'pp55'
            ? 'Suket PP 55 dapat mengubah perlakuan menjadi PPh Final UMKM, bukan otomatis bebas pajak. Pastikan dasar dan kewajiban yang berlaku sebelum menetapkan potongan.'
            : 'SKB PPh 23 harus valid serta sesuai objek, penerima, dan masa berlaku. Kalkulator menahan hasil sampai dokumen diverifikasi.');
        }
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
        if (a.recipientTaxId === 'no') { pph = Math.round(pph * 1.2); warning(alerts,'PPh 21 nonfinal tanpa NPWP/NIK yang sah: tarif pemotongan 20% lebih tinggi dari hasil normal.'); }
        rateLabel = prior + taxBase <= 60000000 ? 'Tarif 5% (Pasal 17) × DPP 50% bruto, bukan TER' : 'Tarif progresif Pasal 17 × DPP 50% bruto, bukan TER';
        taxExplain = 'Narasumber, penerjemah, dan profesional orang pribadi yang bukan pegawai.';
      } else if (a.honorType === 'participant') {
        taxName = 'PPh Pasal 21 — Peserta Kegiatan';
        const prior = num(a.priorDpp);
        pph = Math.max(0,tax17(prior + base) - tax17(prior));
        if (a.recipientTaxId === 'no') { pph = Math.round(pph * 1.2); warning(alerts,'PPh 21 nonfinal tanpa NPWP/NIK yang sah: tarif pemotongan 20% lebih tinggi dari hasil normal.'); }
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
  if (a.recipientTaxId === 'no' && ((a.category === 'services' && a.payeeType === 'person') || (a.category === 'honor' && a.honorType !== 'pns'))) rateLabel += ' (+20% pemotongan tanpa NPWP/NIK valid)';
  if (['honor','temporaryDaily'].includes(a.category) && vatRate) { blocked = true; warning(alerts,'Penghasilan orang pribadi bukan transaksi PKP biasa; hapus PPN atau verifikasi sifat pengadaannya.'); }
  if (a.category === 'goods' && a.payeeType === 'person') warning(alerts,'Pastikan pembelian benar-benar barang, bukan jasa orang pribadi, untuk memilih PPh 22.');
  const method = a.vatCollector || 'unknown';
  let collector = 'Tidak ada PPN', vatGov = 0;
  if (vat > 0) {
    const knownCollectors = ['government','vendor','thirdparty'];
    if (!knownCollectors.includes(method)) {
      blocked = true;
      warning(alerts,'Pilih pemungut PPN sesuai faktur dan mekanisme transaksi. Ambang Rp2 juta memiliki pengecualian, jadi pemungut tidak ditentukan otomatis.');
    }
    const smallNonSplit = base <= 2000000 && !a.splitContract;
    const isGov = method === 'government';
    collector = isGov ? 'Instansi pemerintah' : method === 'vendor' ? 'Rekanan/PKP' : method === 'thirdparty' ? 'Pihak lain' : 'Belum ditentukan';
    if (isGov) vatGov = vat;
    if (isGov && smallNonSplit) {
      blocked = true;
      warning(alerts,'Transaksi paling banyak Rp2 juta (bukan pemecahan transaksi) termasuk pengecualian pemungutan PPN oleh instansi. Cocokkan invoice dan gunakan pemungut yang tercantum pada dokumen.');
    }
    if (method === 'government' && a.paymentMethod === 'kkpd') {
      blocked = true;
      warning(alerts,'Pembayaran kartu kredit pemerintah termasuk pengecualian pemungutan PPN oleh instansi; verifikasi pihak yang memungut pada dokumen transaksi.');
    }
    if (method === 'government' && a.paymentMethod === 'upMarketplace') {
      blocked = true;
      warning(alerts,'Untuk UP melalui Pihak Lain, pastikan pemungut PPN sesuai bukti transaksi dan hindari pungutan ganda.');
    }
  }
  if (a.paymentMethod === 'upMarketplace' && a.category === 'goods' && a.goodsException !== 'alreadyCollected')
    warning(alerts,'Bila PPh 22 sudah dipungut Pihak Lain, pilih pengecualian khusus agar tidak memungut dua kali.');
  const retention = num(a.retention), advance = num(a.advance), penalty = num(a.penalty), misc = num(a.other);
  const nonTax = Math.round(retention + advance + penalty + misc);
  const payout = invoice - pph - vatGov - nonTax;
  if (nonTax > 0) warning(alerts,'Retensi, angsuran uang muka, denda dan potongan lain bersifat simulasi kas; dasar pengenaan pajaknya harus dicocokkan dengan kontrak dan bukti transaksi.');
  if (payout < 0) { blocked = true; warning(alerts,'Total potongan melebihi nilai tagihan. Periksa data.'); }
  if (a.vatMode === 'regular') warning(alerts,'Tarif PPN 12% dikenakan atas DPP nilai lain 11/12 untuk BKP/JKP nonmewah yang memenuhi ketentuan (efektif 11% harga). Skema khusus PMK 11/2025 tidak dihitung otomatis.');
  if (a.vatMode === 'luxury') warning(alerts,'Tarif 12% penuh hanya pada penyerahan yang benar-benar memenuhi kategori barang mewah; PPnBM tidak dihitung.');
  if (blocked) { pph = null; vatGov = null; }
  return {
    ok: !blocked, invoice, base, vat, vatGov, collector, pph, taxName, taxBase,
    rateLabel, taxExplain, nonTax, retention, advance, penalty, misc,
    payout: blocked ? null : Math.max(0,payout), alerts, labels
  };
}
