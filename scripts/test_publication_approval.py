#!/usr/bin/env python3
import importlib.util,json,pathlib,unittest
p=pathlib.Path(__file__).with_name("publication_approval.py");spec=importlib.util.spec_from_file_location("approval",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
article=b'{"id":"p1","title":"Sample"}'
evidence={"state":"REVIEW_PENDING","approved":False,"sourceFingerprint":"abc","reviewFingerprint":"def"}
decision={"reviewer":"Editor","approvedAt":"2026-10-08T10:00:00+08:00","articleId":"p1","evidenceFingerprint":"abc","decision":"APPROVE"}
class Tests(unittest.TestCase):
 def test_valid_exact_bytes(self):
  a=m.authorize(article,evidence,decision);self.assertTrue(m.check(article,evidence,a))
 def test_edit_revokes(self):
  a=m.authorize(article,evidence,decision);self.assertFalse(m.check(article+b" ",evidence,a))
 def test_changed_evidence_revokes(self):
  a=m.authorize(article,evidence,decision);self.assertFalse(m.check(article,{**evidence,"sourceFingerprint":"new"},a))
 def test_changed_review_revokes(self):
  a=m.authorize(article,evidence,decision);self.assertFalse(m.check(article,{**evidence,"reviewFingerprint":"new"},a))
 def test_reject_not_approved(self):
  with self.assertRaises(ValueError):m.authorize(article,evidence,{**decision,"decision":"REJECT"})
 def test_no_timezone(self):
  with self.assertRaises(ValueError):m.authorize(article,evidence,{**decision,"approvedAt":"2026-10-08T10:00:00"})
if __name__=="__main__":unittest.main()
