#!/usr/bin/env python3
import importlib.util,pathlib,unittest
p=pathlib.Path(__file__).with_name("pipeline.py");spec=importlib.util.spec_from_file_location("pipeline",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SecurityTests(unittest.TestCase):
 def test_unsafe_urls(self):
  bad=["http://www.bkn.go.id/","https://www.bkn.go.id.evil.org/","https://user:pass@www.bkn.go.id/","https://www.bkn.go.id:444/","file:///etc/passwd","https://127.0.0.1/"]
  for u in bad:self.assertFalse(m.allowed(u,"www.bkn.go.id"),u)
 def test_redirect_rejected(self):
  with self.assertRaises(ValueError):m.NoRedirect().redirect_request(None,None,302,"redirect",{},"https://evil.org")
 def test_candidate_only(self):
  self.assertTrue(all(x["status"]=="DRY_RUN" for x in m.discover()))
if __name__=="__main__":unittest.main()
