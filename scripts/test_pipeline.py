#!/usr/bin/env python3
import importlib.util,pathlib,unittest
p=pathlib.Path(__file__).with_name("pipeline.py")
spec=importlib.util.spec_from_file_location("pipeline",p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class Tests(unittest.TestCase):
 def test_https_exact_host(self):
  self.assertTrue(mod.allowed("https://www.bkn.go.id/","www.bkn.go.id"))
  for url in ["http://www.bkn.go.id","https://www.bkn.go.id.evil.test","https://evil.test/?next=www.bkn.go.id","https://user@www.bkn.go.id/","https://www.bkn.go.id:8080/"]:
   self.assertFalse(mod.allowed(url,"www.bkn.go.id"))
 def test_fingerprint(self):
  self.assertEqual(mod.sha("same"),mod.sha("same"))
  self.assertNotEqual(mod.sha("same"),mod.sha("changed"))
 def test_no_network_by_default(self):
  results=mod.discover()
  self.assertTrue(results)
  self.assertTrue(all(r["status"]=="DRY_RUN" for r in results))
if __name__=="__main__":unittest.main()
