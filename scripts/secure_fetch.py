#!/usr/bin/env python3
"""Bounded official-source fetch. Default policy refuses unsafe hosts/IPs and redirects."""
import ipaddress, socket, urllib.parse, urllib.request, urllib.error, urllib.robotparser
MAX_BYTES=512000
def public_addresses(hostname,resolver=socket.getaddrinfo):
    addresses=set()
    for item in resolver(hostname,443,type=socket.SOCK_STREAM):
        ip=ipaddress.ip_address(item[4][0])
        if not ip.is_global:raise ValueError("non-public DNS answer")
        addresses.add(str(ip))
    if not addresses:raise ValueError("no DNS answers")
    return addresses
def check_url(url,expected_host,resolver=socket.getaddrinfo):
    u=urllib.parse.urlsplit(url)
    if u.scheme!="https" or u.hostname!=expected_host or u.port not in (None,443) or u.username or u.password or u.fragment:
        raise ValueError("unapproved URL")
    public_addresses(expected_host,resolver)
    return True
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError("redirect forbidden")
def robots_allowed(url,opener):
    u=urllib.parse.urlsplit(url)
    robots=u.scheme+"://"+u.netloc+"/robots.txt"
    try:
        with opener.open(urllib.request.Request(robots,headers={"User-Agent":"ASNPemdaResearch"}),timeout=10) as r:
            data=r.read(65537)
            if len(data)>65536:raise ValueError("robots too large")
            lines=data.decode("utf8",errors="replace").splitlines()
            rp=urllib.robotparser.RobotFileParser();rp.parse(lines)
            return rp.can_fetch("ASNPemdaResearch",url)
    except Exception:return False
def safe_fetch(url,expected_host,previous=None,resolver=socket.getaddrinfo):
    # NOTE: DNS check before urllib connection does NOT pin the connected IP.
    # This function remains disabled for production until connection-level pinning exists.
    raise RuntimeError("NETWORK_FETCH_DISABLED: DNS rebinding protection requires pinned transport")
