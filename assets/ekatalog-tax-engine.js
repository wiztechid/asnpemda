/* ASN Pemda | E-Katalog/INAPROC vendor tax engine | DEV v0.2 (2026).
 * Classification: PMK 58/2022 Art 5–9, PP 9/2022, PMK 231/2019
 * jo PMK 59/2022, PMK 51/2025, PP 55/2022 jo PP 20/2026.
 * No automatic withholding when collector identity or mode is not verified.
 */
import {calculate as calculateGovernment, rupiah} from './spm-tax-engine.js';
export {rupiah};
const round = n => Math.round(n);
const amt = v => Number.isFinite(+v) ? Math.max(0,+v) : 0;
const constRates = Object.freeze({
 worksSmall:.0175,worksOther:.0265,worksNoCert:.04,
 integratedCert:.0265,integratedNoCert:.04,
 consultantCert:.035,consultantNoCert:.06
});
const TYPE = Object.freeze({
 goods:'Belanja barang', services:'Jasa badan nonkonstruksi',
 professional:'Jasa profesional orang pribadi', construction:'Pekerjaan/jasa konstruksi',
 rentBuilding:'Sewa tanah atau bangunan',rentMovable:'Sewa alat/kendaraan',
 transport:'Angkutan umum orang pribadi'
});
function blocked(notes, partial={}) {
 return {ok:false, title:'Data belum cukup untuk menetapkan potongan', notes,
  base:partial.base??0,vat:partial.vat??0,invoice:partial.invoice??0,
  pph:null,net:null,finalGap:null,vatCollector:'Belum ditentukan',
  pphCollector:'Belum ditentukan',taxType:'Perlu verifikasi',taxRate:'—',
  why:'Jangan memilih tarif berdasarkan kata E-Katalog saja.',
  checklist:baseChecklist(), ...partial};
}
function baseChecklist() {
 return ['Pesanan/kontrak dan rincian objek belanja',
 'Mekanisme LS atau UP/KKP dan identitas pemungut pada dokumen transaksi',
 'NPWP/NIK, status PKP, serta tarif dan jenis PPh sesuai penerima',
 'Invoice/tagihan, rincian PPN dan bukti potong/pungut',
 'Jika konstruksi: SBU/SKK, kualifikasi usaha, termin dan nilai pembayaran'];
}
export function calcEcatalog(incoming={}) {
 const i={...incoming}, notes=[];
 const amount=amt(i.amount);
 const rate=i.vatType==='standard'?.11:i.vatType==='luxury'?.12:0;
 const mode=i.priceMode==='inclusive'?'inclusive':'exclusive';
 const base=round(rate&&mode==='inclusive'?amount/(1+rate):amount);
 const vat=round(mode==='inclusive'?amount-base:base*rate);
 const invoice=mode==='inclusive'?round(amount):round(base+vat);
 const partial={base,vat,invoice};
 if(!amount) notes.push('Masukkan harga transaksi lebih dari nol.');
 if(!['ls','marketplaceUP','unverified'].includes(i.route)||i.route==='unverified')
   notes.push('Mekanisme pembayaran/pihak pemungut belum terkonfirmasi; perlu cocokkan dengan pesanan dan bukti transaksi.');
 if(!TYPE[i.objectType]) notes.push('Pilih objek transaksi agar PPh tidak tertukar.');
 if(!['valid','no'].includes(i.taxId)) notes.push('NPWP/NIK penerima belum terverifikasi.');
 if(!['yes','no'].includes(i.pkp)) notes.push('Status Pengusaha Kena Pajak (PKP) belum dikonfirmasi.');
 if(!['standard','luxury','none','special'].includes(i.vatType)) notes.push('Pilih perlakuan PPN sesuai objek transaksi, status PKP, dan faktur.');
 if(i.vatType==='special') notes.push('Skema PPN dengan DPP khusus, nilai lain/besaran tertentu belum didukung kalkulasi otomatis.');
 if(i.pkp==='no' && ['standard','luxury'].includes(i.vatType)) notes.push('Penyedia non-PKP tidak boleh otomatis memungut PPN seperti PKP.');
 if(i.objectType==='transport'&&i.route==='ls') notes.push('Jasa angkutan umum memiliki aturan khusus dan tidak dihitung otomatis pada LS.');
 if(i.route==='marketplaceUP' && i.taxId==='no') notes.push('PMK 58/2022 Pasal 4 mensyaratkan penyampaian NPWP rekanan kepada Pihak Lain; data identitas pajak belum sesuai.');
 if(i.objectType==='professional'&&i.payeeType!=='person') notes.push('Jasa profesional orang pribadi harus dipilih bersama bentuk penyedia Orang Pribadi.');
 if(i.route==='marketplaceUP' && i.collectorProof!=='yes')
   notes.push('Belum ada bukti bahwa platform adalah Pihak Lain yang ditunjuk sebagai pemungut menurut PMK 58/2022.');
 if(i.route==='marketplaceUP'&&i.pkp==='no'&&i.objectType!=='transport')
   notes.push('PMK 58/2022 pada umumnya mewajibkan status PKP rekanan melalui Pihak Lain; periksa pengecualian Pasal 3 sebelum simulasi.');
 if(i.route==='ls'&&i.taxRegime==='unknown') notes.push('Konfirmasi apakah penyedia memakai PPh umum atau PPh Final UMKM; jangan memakai tarif biasa sebelum status diketahui.');
 if(i.route==='ls'&&i.taxRegime==='umkm')
   notes.push('Penggunaan fasilitas PPh Final UMKM 0,5% pada LS memerlukan konfirmasi kelayakan PP 55/2022 jo PP 20/2026 dan Surat Keterangan; tidak disubstitusikan otomatis untuk PPh 22/23.');
 if(i.objectType==='construction' && !Object.hasOwn(constRates,i.constructionType)) notes.push('Kualifikasi pekerjaan konstruksi dan dokumen SBU/SKK belum ditetapkan.');
 if(i.pkp==='yes' && i.vatType==='none') notes.push('PPN nol hanya boleh dipilih bila objek memang tidak dikenai/dibebaskan/tidak dipungut dengan dasar yang jelas.');
 if(i.route==='ls' && rate>0 && !['government','vendor'].includes(i.lsVatCollector))
   notes.push('Pilih siapa yang memungut PPN pada invoice/dokumen. Ambang nilai memiliki pengecualian, sehingga pemungut tidak diasumsikan otomatis.');
 if(notes.length) return blocked(notes,partial);
 if(i.route==='marketplaceUP') {
   const specialTransport=i.objectType==='transport';
   const pph= specialTransport?0:round(base*.005);
   let finalGap=0, finalTax=null;
   if(i.objectType==='construction') finalTax=round(base*constRates[i.constructionType]);
   if(i.objectType==='rentBuilding') finalTax=round(base*.1);
   if(i.taxRegime==='umkm'){
      notes.push('PP 20/2026: fasilitas final UMKM 0,5% hanya bagi pihak yang memenuhi bentuk usaha, batas omzet, dan ketentuan lainnya. Untuk OP, ada ketentuan omzet tahunan Rp500 juta. Periksa sebelum menganggap PPh 22 sebagai pelunasan final.');
   }
   if(finalTax!==null) {
     finalGap=Math.max(0,finalTax-pph);
     notes.push('PPh 22 sebesar 0,5% yang dipungut Pihak Lain adalah bagian pelunasan PPh final; selisih kurang PPh final disetor sendiri oleh penyedia (PMK 58/2022 Pasal 6 ayat 6).');
   }
   if(i.vatType==='luxury') notes.push('PPnBM barang mewah belum diperhitungkan; nominal tagihan bersih belum lengkap.');
   notes.push('Skema PMK 58/2022 berlaku hanya jika transaksi benar-benar melalui Pihak Lain yang ditunjuk dan dibayar melalui UP/KKP, bukan setiap katalog elektronik.');
   const net=invoice-pph-vat;
   return {ok:i.vatType!=='luxury', title:'Dipungut oleh Pihak Lain — UP/KKP',base,vat,invoice,pph,
    taxType:specialTransport?'Pengecualian PPh 22':'PPh Pasal 22 (PMK 58/2022)',
    taxRate:specialTransport?'Tidak dipungut':'0,5% × dasar sebelum PPN',
    vatCollector:vat?'Pihak Lain yang ditunjuk':'Tidak dipungut',
    pphCollector:specialTransport?'Tidak dipungut':'Pihak Lain yang ditunjuk',
    net:i.vatType==='luxury'?null:net,
    finalTax,finalGap:i.vatType==='luxury'?null:finalGap,vatWithheld:i.vatType==='luxury'?null:vat,
    why:specialTransport?'Pengecualian angkutan umum orang pribadi pada Pasal 5 ayat (5).':
        'UP/KKP via Pihak Lain pemungut: PPh 22 0,5% berlaku untuk penjualan barang, jasa, sewa, dan konstruksi. Tidak ditambah PPh 21/23/4(2) oleh instansi atas pembayaran yang sama.',
    notes,checklist:baseChecklist().concat(['Bukti pemungutan PPh 22 0,5% oleh Pihak Lain','Jika PPh final: hitung selisih pelunasan sendiri'])};
 }
 const mappedType=i.objectType==='professional'?'services':i.objectType;
 const g=calculateGovernment({
  category:mappedType,amount:base,amountMode:'exclusive',
  recipientTaxId:i.taxId==='valid'?'yes':'no',
  payeeType:i.objectType==='professional'?'person':i.payeeType==='person'?'person':'company',
  vatMode:i.vatType==='none'?'none':i.vatType==='standard'?'regular':i.vatType==='luxury'?'luxury':'none',
  vatCollector:vat?(i.lsVatCollector||'unknown'):'unknown',paymentMethod:'ls',
  constructionType:i.constructionType,
  goodsException:'none',splitContract:i.splitContract===true
 });
 if(!g.ok) return blocked(g.alerts,partial);
 if(i.vatType==='luxury') return blocked(['BKP mewah memerlukan PPnBM dan prosedur yang belum dihitung otomatis.'],partial);
 const vatGov=g.vatGov;
 if(vat && base<=2000000 && !i.splitContract) notes.push('Pembayaran paling banyak Rp2 juta (bukan pecahan transaksi) termasuk pengecualian pemungutan PPN oleh instansi; cocokkan dengan invoice.');
 if(i.taxRegime==='unknown') notes.push('Status pajak usaha (termasuk kemungkinan fasilitas UMKM) belum diverifikasi; hasil hanya menggunakan klasifikasi objek biasa.');
 notes.push('Pembayaran LS melalui E-Katalog tetap mengikuti pemotongan PPh berdasarkan objek dan penerima; tarif PMK 58/2022 sebesar 0,5% tidak otomatis berlaku.');
 const net=invoice-g.pph-vatGov;
 return {ok:true,title:'Dipotong/dipungut instansi — LS',base,vat,invoice,pph:g.pph,
   net,finalTax:null,finalGap:null,vatWithheld:vatGov,
   taxType:g.taxName,taxRate:g.rateLabel,
   pphCollector:'Instansi pemerintah',
   vatCollector:g.collector,
   why:g.taxExplain,notes:notes.concat(g.alerts||[]),
   checklist:baseChecklist()};
}
