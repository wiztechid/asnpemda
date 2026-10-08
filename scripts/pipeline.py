#!/usr/bin/env python3
"""Offline-only candidate pipeline. Remote fetch deliberately unavailable."""
import argparse,datetime,hashlib,json,pathlib,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(p,default):
 f=ROOT/p
 return json.loads(f.read_text(encoding="utf8")) if f.exists() else default
def sha(s):return hashlib.sha256(s.encode("utf8")).hexdigest()
def host(url):return urllib.parse.urlsplit(url).hostname or ""
def allowed(url,domain):
 try:
  u=urllib.parse.urlsplit(url)
  return u.scheme=="https" and u.hostname==domain and u.port in (None,443) and not u.username and not u.password and not u.fragment
 except ValueError:return False
def fetch(*args,**kwargs):raise RuntimeError("NETWORK_FETCH_DISABLED")
class NoRedirect:
 def redirect_request(self,*args,**kwargs):raise ValueError("redirect forbidden")
def discover(dry_run=True):
 if not dry_run:raise RuntimeError("NETWORK_FETCH_DISABLED: use reviewed manual evidence intake")
 return [{"id":s["id"],"status":"DRY_RUN"} for s in load("data/sources.json",[])]
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--fetch",action="store_true")
 args=p.parse_args()
 if args.fetch:p.error("network fetch is disabled pending transport security review")
 print(json.dumps(discover(),indent=2))
