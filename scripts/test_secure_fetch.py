#!/usr/bin/env python3
import importlib.util,pathlib,unittest,socket
p=pathlib.Path(__file__).with_name("secure_fetch.py");spec=importlib.util.spec_from_file_location("secure_fetch",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def fake(ip):
 return lambda *args,**kwargs:[(socket.AF_INET,socket.SOCK_STREAM,6,"",(ip,443))]
class Security(unittest.TestCase):
 def test_public_dns(self):
  self.assertEqual(m.public_addresses("official.test",fake("8.8.8.8")),{"8.8.8.8"})
 def test_reject_non_public(self):
  for ip in ["127.0.0.1","10.0.0.1","169.254.169.254","192.168.1.1","0.0.0.0"]:
   with self.assertRaises(ValueError):m.public_addresses("official.test",fake(ip))
 def test_reject_host_spoofing(self):
  for url in ["http://official.test","https://official.test.evil.org","https://user@official.test","https://official.test:444","https://official.test/#fragment"]:
   with self.assertRaises(ValueError):m.check_url(url,"official.test",fake("8.8.8.8"))
 def test_fail_closed_network(self):
  with self.assertRaisesRegex(RuntimeError,"NETWORK_FETCH_DISABLED"):m.safe_fetch("https://official.test","official.test")
if __name__=="__main__":unittest.main()
