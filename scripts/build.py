#!/usr/bin/env python3
"""Generate sitemap only from approved published article records; never index drafts."""
import json,pathlib,sys,xml.etree.ElementTree as ET
root=pathlib.Path(__file__).resolve().parents[1]
config=json.loads((root/"site-config.json").read_text(encoding="utf8"))
origin=config.get("siteUrl","").rstrip("/")
if not origin.startswith("https://") or "example" in origin:sys.exit("ERROR: configure production siteUrl before release")
urls=[origin+"/"]
for f in sorted((root/"data/articles").glob("*.json")):
    a=json.loads(f.read_text(encoding="utf8"))
    if a.get("approved") is True and a.get("publicationState")=="PUBLISHED":
        urls.append(origin+"/artikel/"+a["slug"]+".html")
ET.register_namespace("","http://www.sitemaps.org/schemas/sitemap/0.9")
node=ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
for url in urls:ET.SubElement(ET.SubElement(node,"{http://www.sitemaps.org/schemas/sitemap/0.9}url"),"{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text=url
ET.ElementTree(node).write(root/"sitemap.xml",encoding="unicode",xml_declaration=True)
print("sitemap URLs:",len(urls))
