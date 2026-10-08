#!/usr/bin/env python3
"""Deterministic local source delta check; does not crawl external websites."""
import hashlib,json,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1]
path=root/"data/candidates/source-snapshots.json"
if not path.exists():
    print("NO_SNAPSHOTS: nothing to process");sys.exit(0)
rows=json.loads(path.read_text(encoding="utf-8"))
changed=[]
for row in rows:
    digest=hashlib.sha256(row["content"].encode("utf-8")).hexdigest()
    if digest!=row.get("previousFingerprint"): changed.append({"id":row["id"],"fingerprint":digest})
print(json.dumps({"changed":changed,"count":len(changed)},ensure_ascii=False))
