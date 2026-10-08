#!/usr/bin/env python3
import json, pathlib, re, sys, datetime
root=pathlib.Path(__file__).resolve().parents[1]
errors=[]
def fail(s): errors.append(s)
def read(p): return json.loads((root/p).read_text(encoding="utf-8"))
schema=read("schemas/living-policy.schema.json")
sources=read("data/sources.json")
ids=set()
for s in sources:
    if not isinstance(s,dict) or not s.get("id") or not s.get("url","").startswith("https://"): fail("invalid source")
    elif s["id"] in ids: fail("duplicate source id: "+s["id"])
    else: ids.add(s["id"])
required=set(schema["required"])
for p in sorted((root/"data/articles").glob("*.json")):
    try: a=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: fail(str(p)+": "+str(e));continue
    missing=required-set(a)
    if missing: fail(str(p)+": missing "+str(sorted(missing)))
    if a.get("status") not in schema["properties"]["status"]["enum"]: fail(str(p)+": invalid status")
    if a.get("materiality") not in schema["properties"]["materiality"]["enum"]: fail(str(p)+": invalid materiality")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",a.get("slug","")): fail(str(p)+": invalid slug")
    for k in ("datePublished","dateModified","lastVerified"):
        try: datetime.date.fromisoformat(a[k])
        except (ValueError,KeyError,TypeError): fail(str(p)+": invalid "+k)
    if a.get("datePublished","")>a.get("dateModified",""): fail(str(p)+": publication after modification")
    primary=[s for s in a.get("sources",[]) if s.get("isPrimary") and s.get("url","").startswith("https://")]
    if not primary: fail(str(p)+": no primary evidence")
    if a.get("approved") is not True: fail(str(p)+": not approved; published articles require approval")
if errors:
    print("VALIDATION FAILED\n"+"\n".join(errors));sys.exit(1)
print("VALIDATION PASS; sources:",len(sources),"published article records:",len(list((root/"data/articles").glob("*.json"))))
