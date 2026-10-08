#!/usr/bin/env python3
"""Offline reviewed evidence intake. Never automatically verifies or publishes."""
import argparse,datetime,hashlib,json,pathlib,sys,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
def digest(s):return hashlib.sha256(s.encode("utf8")).hexdigest()
def prepare(source_id,url,document_date,body,sources):
 source=next((s for s in sources if s["id"]==source_id),None)
 if source is None:raise ValueError("unknown source id")
 origin=urllib.parse.urlsplit(source["url"])
 target=urllib.parse.urlsplit(url)
 if target.scheme!="https" or target.hostname!=origin.hostname or target.port not in (None,443) or target.username or target.password or target.fragment:raise ValueError("unapproved source URL")
 datetime.date.fromisoformat(document_date)
 if len(body)<40 or len(body)>200000:raise ValueError("evidence text length outside bounds")
 fingerprint=digest(body)
 return {"key":digest(source_id+"|"+url+"|"+fingerprint),"sourceId":source_id,"sourceUrl":url,"documentDate":document_date,"fingerprint":fingerprint,"evidenceLength":len(body),"status":"EVIDENCE_PENDING","materiality":"UNASSESSED","approved":False}
def main():
 p=argparse.ArgumentParser();p.add_argument("--source-id",required=True);p.add_argument("--url",required=True);p.add_argument("--document-date",required=True);p.add_argument("--text-file",required=True);p.add_argument("--write",action="store_true")
 a=p.parse_args()
 sources=json.loads((ROOT/"data/sources.json").read_text(encoding="utf8"))
 body=pathlib.Path(a.text_file).read_text(encoding="utf8")
 item=prepare(a.source_id,a.url,a.document_date,body,sources)
 if not a.write:
  print(json.dumps({"preview":item,"note":"dry-run; use --write to enqueue"},indent=2));return
 queue_path=ROOT/"data/candidates/queue.json"
 queue=json.loads(queue_path.read_text(encoding="utf8")) if queue_path.exists() else []
 if not any(x["key"]==item["key"] for x in queue):
  item["discoveredAt"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
  queue.append(item)
  queue_path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print("candidate queued; still unverified and not published")
if __name__=="__main__":main()
