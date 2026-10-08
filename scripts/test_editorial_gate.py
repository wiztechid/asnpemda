#!/usr/bin/env python3
import importlib.util,pathlib,unittest
p=pathlib.Path(__file__).with_name("editorial_gate.py");spec=importlib.util.spec_from_file_location("editorial_gate",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
a={"id":"abc","fingerprint":"f1","url":"https://www.bkn.go.id/p","verification":"UNVERIFIED","approved":False}
d={"reviewer":"Editor","reviewedAt":"2026-10-08T08:00:00+08:00","primaryDocumentUrl":a["url"],"documentIdentity":"Surat contoh","verificationNotes":"checked original","decision":"VERIFY"}
class Tests(unittest.TestCase):
 def test_verify_not_approve(self):
  x=m.review(a,d);self.assertEqual(x["state"],"REVIEW_PENDING");self.assertFalse(x["approved"])
 def test_reject(self):
  x=m.review(a,{**d,"decision":"REJECT"});self.assertEqual(x["state"],"REJECTED")
 def test_mismatch(self):
  with self.assertRaises(ValueError):m.review(a,{**d,"primaryDocumentUrl":"https://evil.test"})
 def test_unapproved_only(self):
  with self.assertRaises(ValueError):m.review({**a,"approved":True},d)
 def test_deterministic(self):
  self.assertEqual(m.review(a,d)["reviewFingerprint"],m.review(a,d)["reviewFingerprint"])
if __name__=="__main__":unittest.main()
