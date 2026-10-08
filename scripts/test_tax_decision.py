#!/usr/bin/env python3
import importlib.util,json,pathlib,tempfile,unittest
root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("tax_decision",root/"scripts/tax_decision.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
BASE={"amount":1000000,"channel":"UP/GU","kind":"Belanja barang","seller":"Badan usaha","documents":"Sudah diperiksa"}
class TaxDecisionTests(unittest.TestCase):
 def test_ten_scenarios(self):
  scenarios=[
   {"channel":"UP/GU","kind":"Belanja barang"},
   {"channel":"LS","kind":"Jasa lainnya"},
   {"channel":"UP/GU","kind":"Makan-minum restoran"},
   {"channel":"LS","kind":"Jasa katering"},
   {"channel":"KKPD","kind":"Belanja barang"},
   {"channel":"Marketplace","kind":"Belanja barang"},
   {"documents":"Tidak diketahui"},
   {"channel":"Marketplace","documents":"Belum diperiksa"},
   {"amount":0},
   {"amount":9007199254740991}
  ]
  for override in scenarios:
   with self.subTest(override=override):
    p={**BASE,**override};r=m.decide(p)
    self.assertEqual(r["state"],"PERLU_VERIFIKASI")
    self.assertIsNone(r["taxAmount"])
    self.assertEqual(r["ruleId"],"MARKETPLACE-2026" if p["channel"]=="Marketplace" else "SPJ-GENERAL")
 def test_invalid_amounts(self):
  for amount in [-1,1.2,"1000",True,None,9007199254740992]:
   with self.subTest(amount=amount):
    self.assertEqual(m.decide({**BASE,"amount":amount})["state"],"INPUT_ERROR")
 def test_invalid_classification(self):
  for key,value in [("channel","UNKNOWN"),("kind",""),("seller",None),("documents","invalid")]:
   self.assertEqual(m.decide({**BASE,key:value})["state"],"INPUT_ERROR")
 def test_unknown_matrix_status_fails_closed(self):
  matrix=json.loads(m.MATRIX.read_text())
  matrix["status"]="PRODUCTION"
  with tempfile.TemporaryDirectory() as tmp:
   p=pathlib.Path(tmp)/"matrix.json";p.write_text(json.dumps(matrix))
   with self.assertRaisesRegex(ValueError,"UNEXPECTED_MATRIX_STATUS"):m.decide(BASE,p)
 def test_enabled_computation_fails_closed(self):
  matrix=json.loads(m.MATRIX.read_text())
  matrix["rules"][2]["enabled"]=True
  with tempfile.TemporaryDirectory() as tmp:
   p=pathlib.Path(tmp)/"matrix.json";p.write_text(json.dumps(matrix))
   with self.assertRaisesRegex(ValueError,"UNSAFE_ENABLED_STATE"):m.decide(BASE,p)
if __name__=="__main__":unittest.main()
