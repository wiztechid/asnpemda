#!/usr/bin/env python3
import importlib.util,pathlib,unittest
p=pathlib.Path(__file__).with_name("evidence_intake.py");spec=importlib.util.spec_from_file_location("evidence_intake",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def sample():
 return dict(sourceId="bkn",url="https://www.bkn.go.id/pengumuman",issuer="BKN",documentDate="2026-10-08",retrievedAt="2026-10-08T08:00:00+08:00",title="Contoh",evidenceText="Teks bukti contoh")
class EvidenceTests(unittest.TestCase):
 def test_candidate_unverified(self):
  a=m.intake([sample()])[0];self.assertEqual(a["status"],"EVIDENCE_PENDING");self.assertFalse(a["approved"]);self.assertEqual(a["verification"],"UNVERIFIED")
 def test_stable_id(self):
  self.assertEqual(m.intake([sample()])[0]["id"],m.intake([sample()])[0]["id"])
 def test_fake_host(self):
  x=sample();x["url"]="https://www.bkn.go.id.evil.test/";self.assertRaises(ValueError,m.intake,[x])
 def test_no_timezone(self):
  x=sample();x["retrievedAt"]="2026-10-08T08:00:00";self.assertRaises(ValueError,m.intake,[x])
 def test_no_source(self):
  x=sample();x["sourceId"]="fake";self.assertRaises(ValueError,m.intake,[x])
if __name__=="__main__":unittest.main()
