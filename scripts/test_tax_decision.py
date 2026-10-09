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
 def test_date_and_channel_checks(self):
  for day in ("2026-09-30","2026-10-01","2026-10-09"):
   result=m.decide({**BASE,"channel":"Marketplace","transactionDate":day})
   self.assertEqual(result["state"],"PERLU_VERIFIKASI")
   self.assertIsNone(result["taxAmount"])
   self.assertTrue(any("platform" in s.lower() for s in result["checks"]))
  old=m.decide({**BASE,"channel":"Marketplace","transactionDate":"2026-09-30"})
  self.assertTrue(any("historical" in s.lower() for s in old["checks"]))
  card=m.decide({**BASE,"channel":"KKPD","transactionDate":"2026-10-09"})
  self.assertTrue(any("KKPD" in s for s in card["checks"]))
  missing=m.decide(BASE)
  self.assertTrue(any("transaction date" in s.lower() for s in missing["checks"]))
 def test_invalid_dates(self):
  for day in ("2026-02-30","2026-13-01","09-10-2026","2026-1-01",20261009,"2026-10-09T00:00:00"):
   with self.subTest(day=day):
    self.assertEqual(m.decide({**BASE,"transactionDate":day})["state"],"INPUT_ERROR")
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
   with self.assertRaisesRegex(ValueError,"UNSAFE_RULE_CONFIGURATION"):m.decide(BASE,p)
 def test_rule_set_mutations_fail_closed(self):
  original=json.loads(m.MATRIX.read_text())
  for mutation in ("remove","duplicate","rename","enable_ready","change_state"):
   with self.subTest(mutation=mutation):
    matrix=json.loads(json.dumps(original))
    if mutation=="remove":matrix["rules"].pop()
    elif mutation=="duplicate":matrix["rules"].append(dict(matrix["rules"][0]))
    elif mutation=="rename":matrix["rules"][0]["id"]="UNKNOWN"
    elif mutation=="enable_ready":matrix["rules"][3]["enabled"]=True
    elif mutation=="change_state":matrix["rules"][0]["state"]="DAPAT_DIHITUNG"
    with tempfile.TemporaryDirectory() as tmp:
     p=pathlib.Path(tmp)/"matrix.json";p.write_text(json.dumps(matrix))
     with self.assertRaises(ValueError):m.decide(BASE,p)
if __name__=="__main__":unittest.main()
