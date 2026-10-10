"use strict";
const fs=require("node:fs"),vm=require("node:vm"),assert=require("node:assert/strict");
const source=fs.readFileSync("assets/spj-prototype.js","utf8");
function simulate(data){
 let handler;
 const form={addEventListener:(type,cb)=>{assert.equal(type,"submit");handler=cb;}};
 const output={textContent:"",children:[],replaceChildren(...items){this.children=items;}};
 function node(tag){return {tag,textContent:"",children:[],append(...items){this.children.push(...items);}};}
 const sandbox={
  document:{getElementById:id=>id==="taxform"?form:id==="hasil"?output:null,createElement:node},
  FormData:class {constructor(){this.values=data;}get(k){return Object.prototype.hasOwnProperty.call(this.values,k)?this.values[k]:null;}},
  Date,Number,String
 };
 vm.runInNewContext(source,sandbox,{timeout:1000,filename:"spj-prototype.js"});
 assert.equal(typeof handler,"function");
 handler({preventDefault(){}});
 return {error:output.textContent,heading:output.children[0]?.children[0]?.textContent||"",checks:output.children[0]?.children[2]?.children.map(x=>x.textContent)||[]};
}
const base={nilai:"1000000",tanggal:"2026-10-09",metode:"UP/GU",jenis:"Belanja barang",rekanan:"Badan usaha",dokumen:"Sudah diperiksa"};
for(const amount of ["0","1000000","9007199254740991"]){const r=simulate({...base,nilai:amount});assert.match(r.heading,/PERLU VERIFIKASI/);}
for(const amount of ["-1","1.5","abc","9007199254740992"]){assert.match(simulate({...base,nilai:amount}).error,/valid/);}
for(const day of ["2026-02-30","2026-13-01","2026-1-01","2026-10-09T00:00:00"]){assert.match(simulate({...base,tanggal:day}).error,/valid/);}
assert(simulate({...base,metode:"KKPD"}).checks.some(x=>x.includes("KKPD")));
assert(simulate({...base,metode:"Marketplace",tanggal:"2026-09-30"}).checks.some(x=>x.includes("historis")));
assert(!simulate({...base,metode:"Marketplace",tanggal:"2026-10-01"}).checks.some(x=>x.includes("historis")));
assert(simulate({...base,metode:"Marketplace"}).checks.some(x=>x.includes("platform")));
console.log("SPJ JavaScript behavior tests passed");


const {spawnSync}=require("node:child_process");
function compareWithPython(data){
 const payload={amount:Number(data.nilai),transactionDate:data.tanggal,channel:data.metode,kind:data.jenis,seller:data.rekanan,documents:data.dokumen};
 const py='import json,sys;from scripts.tax_decision import decide;print(json.dumps(decide(json.loads(sys.argv[1]))))';
 const run=spawnSync("python",["-c",py,JSON.stringify(payload)],{encoding:"utf8",timeout:3000});
 assert.equal(run.status,0,run.stderr);
 const engine=JSON.parse(run.stdout),browser=simulate(data);
 assert.equal(engine.state,"PERLU_VERIFIKASI");
 assert.equal(engine.taxAmount,null);
 assert.match(browser.heading,/PERLU VERIFIKASI/);
 if(data.metode==="KKPD"){
  assert(browser.checks.some(s=>s.includes("KKPD")));
  assert(engine.checks.some(s=>s.includes("KKPD")));
 }
 if(data.metode==="Marketplace"){
  assert(browser.checks.some(s=>s.includes("platform")));
  assert(engine.checks.some(s=>s.includes("platform")));
  const old=data.tanggal<"2026-10-01";
  assert.equal(browser.checks.some(s=>s.includes("historis")),old);
  assert.equal(engine.checks.some(s=>s.includes("historical")),old);
 }
}
for(const method of ["UP/GU","LS","KKPD","Marketplace"]){
 for(const day of ["2026-09-30","2026-10-01","2026-10-09"]){
  compareWithPython({...base,metode:method,tanggal:day});
 }
}
console.log("SPJ same-input cross-engine parity passed");
