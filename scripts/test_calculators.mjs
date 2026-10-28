import assert from 'node:assert/strict';
import {calculate as calculateSpm} from '../assets/spm-tax-engine.js';
import {calcEcatalog} from '../assets/ekatalog-tax-engine.js';

const spm = {
  amount: 10_000_000, category: 'goods', recipientTaxId: 'yes', payeeType: 'company',
  paymentMethod: 'ls', vatMode: 'regular', pkpStatus: 'yes', amountMode: 'exclusive',
  goodsException: 'none', vatCollector: 'unknown'
};
assert.equal(calculateSpm(spm).ok, false, 'SPM must hold PPN if the collector is unknown');
const spmGov = calculateSpm({...spm, vatCollector: 'government'});
assert.equal(spmGov.ok, true);
assert.equal(spmGov.vat, 1_100_000);
assert.equal(spmGov.vatGov, 1_100_000);
assert.equal(spmGov.payout, 9_850_000);
const spmVendor = calculateSpm({...spm, vatCollector: 'vendor'});
assert.equal(spmVendor.ok, true);
assert.equal(spmVendor.vatGov, 0);
assert.equal(spmVendor.payout, 10_950_000);
assert.equal(calculateSpm({...spm, amount: 2_000_000, vatCollector: 'government'}).ok, false,
  'government should not collect PPN for a standalone payment up to Rp2 million');
const spmSmallVendor = calculateSpm({...spm, amount: 2_000_000, vatCollector: 'vendor'});
assert.equal(spmSmallVendor.ok, true);
assert.equal(spmSmallVendor.vatGov, 0);

const dailyWorker = {amount:450_000,category:'temporaryDaily',vatMode:'none',amountMode:'exclusive',paymentMethod:'ls'};
assert.equal(calculateSpm(dailyWorker).pph,0,'daily TER is 0% through Rp450,000');
assert.equal(calculateSpm({...dailyWorker,amount:450_001}).pph,2_250,'daily TER is 0.5% above Rp450,000');
assert.equal(calculateSpm({...dailyWorker,amount:2_500_000}).pph,12_500,'daily TER applies through Rp2,500,000');
assert.equal(calculateSpm({...dailyWorker,amount:3_000_000}).pph,75_000,'above Rp2,500,000, half gross is taxed at Article 17');
const bosGoods = calculateSpm({...spm,goodsException:'bos',vatCollector:'government'});
assert.equal(bosGoods.ok,true); assert.equal(bosGoods.pph,0,'BOS-funded goods are excluded from PPh 22 collection');
const riceGoods = calculateSpm({...spm,goodsException:'rice',vatCollector:'government'});
assert.equal(riceGoods.ok,true); assert.equal(riceGoods.pph,0,'rice purchases are excluded from PPh 22 collection');
assert.equal(calculateSpm({...spm,category:'services',serviceException:'skb'}).ok,false,
  'PPh 23 SKB must be verified before withholding is determined');

const ecat = {
  amount: 10_000_000, route: 'ls', collectorProof: 'unknown', payeeType: 'company',
  taxId: 'valid', pkp: 'yes', taxRegime: 'regular', objectType: 'goods',
  vatType: 'standard', priceMode: 'exclusive', splitContract: false, lsVatCollector: 'unknown'
};
assert.equal(calcEcatalog(ecat).ok, false, 'E-Katalog LS must hold PPN if the collector is unknown');
const ecatGov = calcEcatalog({...ecat, lsVatCollector: 'government'});
assert.equal(ecatGov.ok, true);
assert.equal(ecatGov.pph, 150_000);
assert.equal(ecatGov.vatWithheld, 1_100_000);
assert.equal(ecatGov.net, 9_850_000);
const ecatVendor = calcEcatalog({...ecat, lsVatCollector: 'vendor'});
assert.equal(ecatVendor.ok, true);
assert.equal(ecatVendor.vatWithheld, 0);
assert.equal(ecatVendor.net, 10_950_000);
assert.equal(calcEcatalog({...ecat, amount: 2_000_000, lsVatCollector: 'government'}).ok, false);
const ecatSmallVendor = calcEcatalog({...ecat, amount: 2_000_000, lsVatCollector: 'vendor'});
assert.equal(ecatSmallVendor.ok, true);
assert.equal(ecatSmallVendor.vatWithheld, 0);
const ecatUp = calcEcatalog({...ecat, route: 'marketplaceUP', collectorProof: 'yes'});
assert.equal(ecatUp.ok, true);
assert.equal(ecatUp.pph, 50_000);
assert.equal(ecatUp.vatWithheld, 1_100_000);
assert.equal(ecatUp.net, 9_950_000);
assert.equal(calcEcatalog({...ecat, vatType: 'none', pkp: 'no'}).ok, true,
  'a PPN collector choice is unnecessary when the transaction is not subject to PPN');

console.log('SPM/SP2D and E-Katalog VAT collector guardrails passed');
