#!/usr/bin/env python3
"""Release safety gate: block public release while unreviewed network fetch and editorial content remain."""
import json,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1]
config=json.loads((root/"site-config.json").read_text(encoding="utf8"))
issues=[]
if config.get("autoPublish") is not False:issues.append("autoPublish must be false")
if config.get("publicationMode")!="PRE_RELEASE":issues.append("publicationMode must remain PRE_RELEASE until approval")
if not (root/"docs/RELEASE_DECISION.md").exists():issues.append("release decision missing")
for f in (root/"data/articles").glob("*.json"):
 a=json.loads(f.read_text(encoding="utf8"))
 if a.get("publicationState")=="PUBLISHED" and a.get("approved") is not True:issues.append(str(f)+": unapproved published record")
if issues:
 print("SECURITY GATE FAIL: "+"; ".join(issues));sys.exit(1)
print("SECURITY GATE PASS: publication is disabled pending release approval")
