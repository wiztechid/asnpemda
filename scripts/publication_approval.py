#!/usr/bin/env python3
"""Bind human publication authorization to exact article bytes and evidence fingerprints."""
import argparse,datetime,hashlib,json,pathlib
def sha(data):return hashlib.sha256(data).hexdigest()
def authorize(article_bytes,evidence,decision):
 article=json.loads(article_bytes)
 for key in ("reviewer","approvedAt","articleId","evidenceFingerprint","decision"):
  if not isinstance(decision.get(key),str) or not decision[key].strip():raise ValueError("missing "+key)
 dt=datetime.datetime.fromisoformat(decision["approvedAt"].replace("Z","+00:00"))
 if dt.tzinfo is None:raise ValueError("timezone required")
 if decision["decision"]!="APPROVE":raise ValueError("explicit APPROVE required")
 if article.get("id")!=decision["articleId"]:raise ValueError("article mismatch")
 if evidence.get("state")!="REVIEW_PENDING" or evidence.get("approved") is not False:raise ValueError("evidence not reviewed")
 if evidence.get("sourceFingerprint")!=decision["evidenceFingerprint"]:raise ValueError("evidence changed")
 return {"articleId":article["id"],"articleSha256":sha(article_bytes),"evidenceFingerprint":evidence["sourceFingerprint"],"reviewFingerprint":evidence["reviewFingerprint"],"reviewer":decision["reviewer"],"approvedAt":decision["approvedAt"],"authorization":"APPROVED"}
def check(article_bytes,evidence,approval):
 try:
  return approval["authorization"]=="APPROVED" and approval["articleSha256"]==sha(article_bytes) and approval["articleId"]==json.loads(article_bytes)["id"] and approval["evidenceFingerprint"]==evidence["sourceFingerprint"] and approval["reviewFingerprint"]==evidence["reviewFingerprint"]
 except (KeyError,ValueError,TypeError):return False
def main():
 p=argparse.ArgumentParser();p.add_argument("article");p.add_argument("evidence");p.add_argument("decision");args=p.parse_args()
 a=pathlib.Path(args.article).read_bytes()
 e=json.loads(pathlib.Path(args.evidence).read_text(encoding="utf8"))
 d=json.loads(pathlib.Path(args.decision).read_text(encoding="utf8"))
 print(json.dumps(authorize(a,e,d),indent=2))
if __name__=="__main__":main()
