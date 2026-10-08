#!/usr/bin/env python3
"""Fail-closed official-source intake; no autonomous publication."""
import argparse,datetime,email.utils,hashlib,json,pathlib,re,time,urllib.error,urllib.parse,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(p,default):
    f=ROOT/p
    return json.loads(f.read_text(encoding="utf8")) if f.exists() else default
def save(p,obj):
    f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
def sha(s):return hashlib.sha256(s.encode("utf8")).hexdigest()
def host(url):return urllib.parse.urlsplit(url).hostname or ""
def allowed(url,domain):
    u=urllib.parse.urlsplit(url)
    return u.scheme=="https" and u.username is None and u.password is None and u.port in (None,443) and u.hostname==domain
def fetch(url,domain,previous=None,opener=None):
    if not allowed(url,domain):raise ValueError("URL is outside exact official domain")
    headers={"User-Agent":"ASNPemdaResearch/0.4 (+public editorial project)","Accept":"text/html,application/json,text/plain"}
    if previous:
        if previous.get("etag"):headers["If-None-Match"]=previous["etag"]
        if previous.get("last_modified"):headers["If-Modified-Since"]=previous["last_modified"]
    req=urllib.request.Request(url,headers=headers)
    opener=opener or urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(req,timeout=12) as res:
            if res.status==304:return None,previous
            if res.status!=200:raise ValueError("HTTP "+str(res.status))
            kind=res.headers.get("Content-Type","").split(";")[0].lower()
            if kind not in ("text/html","text/plain","application/json"):raise ValueError("unsupported content type")
            raw=res.read(512001)
            if len(raw)>512000:raise ValueError("oversized response")
            body=raw.decode("utf8",errors="replace")
            return body,{"etag":res.headers.get("ETag"),"last_modified":res.headers.get("Last-Modified")}
    except urllib.error.HTTPError as e:
        if e.code==304:return None,previous
        raise
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise ValueError("redirect requires manual source review")
def discover(dry_run=True):
    sources=load("data/sources.json",[])
    state=load("data/candidates/source-state.json",{})
    candidates=load("data/candidates/queue.json",[])
    seen={x["key"] for x in candidates}
    results=[]
    for s in sources:
        sid=s["id"];url=s["url"];domain=host(url)
        if not allowed(url,domain):results.append({"id":sid,"status":"BLOCKED_URL"});continue
        if dry_run:results.append({"id":sid,"status":"DRY_RUN"});continue
        try:
            body,meta=fetch(url,domain,state.get(sid))
            if body is None:results.append({"id":sid,"status":"NOT_MODIFIED"});continue
            fingerprint=sha(body)
            if fingerprint==state.get(sid,{}).get("fingerprint"):
                results.append({"id":sid,"status":"UNCHANGED"});continue
            key=sha(sid+"|"+fingerprint)
            now=datetime.datetime.now(datetime.timezone.utc).isoformat()
            if key not in seen:
                candidates.append({"key":key,"sourceId":sid,"sourceUrl":url,"fingerprint":fingerprint,"discoveredAt":now,"status":"EVIDENCE_PENDING","materiality":"UNASSESSED","approved":False})
                seen.add(key)
            state[sid]={"fingerprint":fingerprint,**meta,"lastChecked":now}
            results.append({"id":sid,"status":"CANDIDATE_QUEUED"})
        except Exception as e:
            results.append({"id":sid,"status":"FETCH_ERROR","reason":type(e).__name__})
        time.sleep(1)
    if not dry_run:
        save("data/candidates/source-state.json",state)
        save("data/candidates/queue.json",candidates)
    return results
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--fetch",action="store_true",help="explicit network discovery, never publishes")
    args=p.parse_args();print(json.dumps(discover(not args.fetch),indent=2))
