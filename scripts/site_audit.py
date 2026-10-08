#!/usr/bin/env python3
from pathlib import Path
import re,sys
root=Path(__file__).resolve().parents[1]
errors=[]
for p in sorted(root.rglob("*.html")):
    txt=p.read_text(encoding="utf-8")
    for tag in ("<html","<title>","<meta name=\"viewport\"","</html>"):
        if tag not in txt: errors.append(f"{p.relative_to(root)} missing {tag}")
    if p.parts[-2:-1]==("artikel",) and 'noindex' not in txt:
        errors.append(f"{p.relative_to(root)} draft missing noindex")
    for link in re.findall(r'href="([^"]+)"',txt):
        if link.startswith(("https:","http:","mailto:","#")): continue
        target=(p.parent/link.split("#")[0].split("?")[0]).resolve()
        if not target.is_relative_to(root) or not target.exists():
            errors.append(f"{p.relative_to(root)} broken local link: {link}")
if errors:
    print("\n".join(errors));sys.exit(1)
print("SITE AUDIT PASS")
