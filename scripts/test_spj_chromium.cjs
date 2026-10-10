#!/usr/bin/env node
"use strict";
const {chromium}=require("playwright");
const {pathToFileURL}=require("node:url");
const path=require("node:path");
const assert=require("node:assert/strict");
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage();
  const url=pathToFileURL(path.resolve("tools/kalkulator-pajak-spj.html")).href;
  await page.goto(url);
  assert.equal(await page.locator('meta[name="robots"]').getAttribute("content"),"noindex,nofollow");
  const base={jenis:"Belanja barang",tanggal:"2026-10-09",nilai:"1000000",rekanan:"Badan usaha",dokumen:"Sudah diperiksa",metode:"KKPD"};
  async function fill(values){
   for(const [name,value] of Object.entries(values)){
    const locator=page.locator('[name="'+name+'"]');
    if(name==="jenis"||name==="rekanan"||name==="dokumen"||name==="metode")await locator.selectOption({label:value});
    else await locator.fill(value);
   }
  }
  await fill(base);
  await page.getByRole("button",{name:"Buat checklist verifikasi"}).click();
  assert.match(await page.locator("#hasil").innerText(),/PERLU VERIFIKASI/);
  assert.match(await page.locator("#hasil").innerText(),/KKPD/);
  assert.doesNotMatch(await page.locator("#hasil").innerText(),/Total pajak:/);
  await page.locator('[name="metode"]').selectOption({label:"Marketplace"});
  await page.locator('[name="tanggal"]').fill("2026-09-30");
  await page.getByRole("button",{name:"Buat checklist verifikasi"}).click();
  assert.match(await page.locator("#hasil").innerText(),/historis/);
  await page.locator('[name="tanggal"]').fill("2026-10-01");
  await page.getByRole("button",{name:"Buat checklist verifikasi"}).click();
  assert.doesNotMatch(await page.locator("#hasil").innerText(),/historis/);
  await page.locator('[name="jenis"]').selectOption("");
  assert.equal(await page.locator("#taxform").evaluate(form=>form.checkValidity()),false);
  console.log("Chromium SPJ smoke tests passed");
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
