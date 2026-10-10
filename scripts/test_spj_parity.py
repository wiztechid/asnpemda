#!/usr/bin/env python3
"""Cross-check shared SPJ browser scenarios against Python decision output."""
import json
import pathlib
import subprocess
import unittest
from tax_decision import decide

ROOT=pathlib.Path(__file__).resolve().parents[1]
CASES=[
 {"amount":1000000,"channel":"UP/GU","kind":"Belanja barang","seller":"Badan usaha","documents":"Sudah diperiksa","transactionDate":"2026-10-09"},
 {"amount":1000000,"channel":"KKPD","kind":"Belanja barang","seller":"Badan usaha","documents":"Sudah diperiksa","transactionDate":"2026-10-09"},
 {"amount":1000000,"channel":"Marketplace","kind":"Belanja barang","seller":"Badan usaha","documents":"Sudah diperiksa","transactionDate":"2026-09-30"},
 {"amount":1000000,"channel":"Marketplace","kind":"Belanja barang","seller":"Badan usaha","documents":"Sudah diperiksa","transactionDate":"2026-10-01"}
]
class Parity(unittest.TestCase):
 def test_python_review_contract(self):
  for case in CASES:
   with self.subTest(channel=case["channel"],date=case["transactionDate"]):
    result=decide(case)
    self.assertEqual(result["state"],"PERLU_VERIFIKASI")
    self.assertIsNone(result["taxAmount"])
    if case["channel"]=="KKPD":
     self.assertTrue(any("KKPD" in s for s in result["checks"]))
    if case["channel"]=="Marketplace":
     self.assertTrue(any("platform" in s.lower() for s in result["checks"]))
     self.assertEqual(any("historical" in s for s in result["checks"]),case["transactionDate"]<"2026-10-01")
 def test_browser_execution(self):
  run=subprocess.run(["node","scripts/test_spj_browser.cjs"],cwd=ROOT,capture_output=True,text=True,timeout=15)
  self.assertEqual(run.returncode,0,run.stderr)
if __name__=="__main__":
 unittest.main()
