#!/usr/bin/env python3
import importlib.util,pathlib,unittest
p=pathlib.Path(__file__).with_name("manual_intake.py");s=importlib.util.spec_from_file_location("manual_intake",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
sources=[{"id":"bkn","url":"https://www.bkn.go.id/"}]
class Tests(unittest.TestCase):
 def test_valid_and_dedupe(self):
  a=m.prepare("bkn","https://www.bkn.go.id/berita","2026-10-08","Verified excerpt "+"x"*50,sources)
  b=m.prepare("bkn","https://www.bkn.go.id/berita","2026-10-08","Verified excerpt "+"x"*50,sources)
  self.assertEqual(a["key"],b["key"]);self.assertFalse(a["approved"])
 def test_reject_spoofing(self):
  for url in ["http://www.bkn.go.id/","https://www.bkn.go.id.evil.test/","https://u@www.bkn.go.id/","https://www.bkn.go.id:999/"]:
   with self.assertRaises(ValueError):m.prepare("bkn",url,"2026-10-08","x"*50,sources)
 def test_reject_short(self):
  with self.assertRaises(ValueError):m.prepare("bkn","https://www.bkn.go.id/","2026-10-08","short",sources)
if __name__=="__main__":unittest.main()
