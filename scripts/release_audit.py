#!/usr/bin/env python3
"""Offline release blocker audit. Exit 0 for accurate HOLD state; never grants GO."""
import json,pathlib
r=pathlib.Path(__file__).resolve().parents[1]
c=json.loads((r/"site-config.json").read_text(encoding="utf8"))
checks={"auto_publish_disabled":c.get("autoPublish") is False,
"pre_release_mode":c.get("publicationMode")=="PRE_RELEASE",
"draft_noindex":'noindex,follow' in (r/"artikel/gaji-asn-melalui-koperasi.html").read_text(encoding="utf8"),
"security_policy_present":(r/"docs/NETWORK_FETCH_POLICY.md").exists(),
"human_release_approval":False,
"production_deploy_configured":False,
"primary_evidence_verified":False}
print(json.dumps({"checks":checks,"decision":"HOLD" if not all(checks.values()) else "GO"},indent=2))
