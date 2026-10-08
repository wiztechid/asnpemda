#!/usr/bin/env python3
"""Offline editorial review: verify candidate and produce an approval proposal, never publish."""
import argparse,datetime,hashlib,json,pathlib
def sha(s):return hashlib.sha256(s.encode("utf8")).hexdigest()
def review(candidate,decision):
 if candidate.get("verification")!="UNVERIFIED" or candidate.get("approved") is not False:raise ValueError("candidate must be unverified and unapproved")
 for key in ("reviewer","reviewedAt","primaryDocumentUrl","documentIdentity","verificationNotes","decision"):
  if not isinstance(decision.get(key),str) or not decision[key].strip():raise ValueError("missing "+key)
 dt=datetime.datetime.fromisoformat(decision["reviewedAt"].replace("Z","+00:00"))
 if dt.tzinfo is None:raise ValueError("reviewedAt needs timezone")
 if decision["decision"] not in ("VERIFY","REJECT"):raise ValueError("invalid decision")
 if decision["primaryDocumentUrl"]!=candidate["url"]:raise ValueError("source URL mismatch")
 if decision["decision"]=="REJECT":state="REJECTED"
 else:state="REVIEW_PENDING"
 evidence={"candidateId":candidate["id"],"fingerprint":candidate["fingerprint"],"reviewer":decision["reviewer"],"reviewedAt":decision["reviewedAt"],"documentIdentity":decision["documentIdentity"],"verificationNotes":decision["verificationNotes"],"decision":decision["decision"]}
 return {"candidateId":candidate["id"],"sourceFingerprint":candidate["fingerprint"],"state":state,"verification":"HUMAN_REVIEW_RECORDED","approved":False,"review":evidence,"reviewFingerprint":sha(json.dumps(evidence,sort_keys=True))}
def main():
 p=argparse.ArgumentParser();p.add_argument("candidate");p.add_argument("decision");args=p.parse_args()
 a=json.loads(pathlib.Path(args.candidate).read_text(encoding="utf8"))
 d=json.loads(pathlib.Path(args.decision).read_text(encoding="utf8"))
 print(json.dumps(review(a,d),indent=2,ensure_ascii=False))
if __name__=="__main__":main()
