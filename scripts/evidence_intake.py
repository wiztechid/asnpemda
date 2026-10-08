#!/usr/bin/env python3
"""Offline, auditable primary-source candidate intake. Never auto-approves or publishes."""
import argparse,datetime,hashlib,json,pathlib,re,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
def digest(s):return hashlib.sha256(s.encode("utf-8")).hexdigest()
def check(row,registry):
 required=("sourceId","url","issuer","documentDate","retrievedAt","title","evidenceText")
 missing=[k for k in required if not isinstance(row.get(k),str) or not row[k].strip()]
 if missing:raise ValueError("missing: "+",".join(missing))
 s=registry.get(row["sourceId"])
 if s is None:raise ValueError("unknown sourceId")
 u=urllib.parse.urlsplit(row["url"]);r=urllib.parse.urlsplit(s["url"])
 if u.scheme!="https" or u.hostname!=r.hostname or u.username or u.password or u.port not in (None,443) or u.fragment:raise ValueError("source host mismatch")
 datetime.date.fromisoformat(row["documentDate"])
 dt=datetime.datetime.fromisoformat(row["retrievedAt"].replace("Z","+00:00"))
 if dt.tzinfo is None:raise ValueError("retrievedAt must include timezone")
 if len(row["evidenceText"])>100000:raise ValueError("evidence too large")
 if len(row["title"])>400:raise ValueError("title too long")
 return {"id":digest(row["sourceId"]+"|"+row["url"]+"|"+digest(row["evidenceText"]))[:24],
         "sourceId":row["sourceId"],"url":row["url"],"issuer":row["issuer"],
         "documentDate":row["documentDate"],"retrievedAt":row["retrievedAt"],
         "title":row["title"],"fingerprint":digest(row["evidenceText"]),
         "status":"EVIDENCE_PENDING","approved":False,"verification":"UNVERIFIED",
         "note":"Human verification required; source domain does not prove legal validity."}
def intake(rows):
 registry={x["id"]:x for x in json.loads((ROOT/"data/sources.json").read_text(encoding="utf8"))}
 return [check(x,registry) for x in rows]
def main():
 p=argparse.ArgumentParser();p.add_argument("input",help="local JSON array of manually collected evidence")
 p.add_argument("--output",help="optional candidate JSON output file");a=p.parse_args()
 inp=pathlib.Path(a.input).resolve()
 if not inp.is_file():p.error("input missing")
 rows=json.loads(inp.read_text(encoding="utf8"))
 if not isinstance(rows,list):p.error("expected JSON array")
 result=intake(rows)
 payload=json.dumps(result,indent=2,ensure_ascii=False)+"\n"
 if a.output:pathlib.Path(a.output).write_text(payload,encoding="utf8")
 else:print(payload)
if __name__=="__main__":main()
