#!/usr/bin/env python3
"""Release safety gate: require human owner authorization for each published article."""
import hashlib
import json
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parents[1]
config = json.loads((root / "site-config.json").read_text(encoding="utf8"))
issues = []
if config.get("autoPublish") is not False:
    issues.append("autoPublish must remain false")

mode = config.get("publicationMode")
if mode not in ("PRE_RELEASE", "PUBLICATION_ACTIVE"):
    issues.append("publicationMode must be PRE_RELEASE or PUBLICATION_ACTIVE")

if not (root / "docs" / "RELEASE_DECISION.md").exists():
    issues.append("release decision missing")

published = 0
for record_path in (root / "data" / "articles").glob("*.json"):
    try:
        record = json.loads(record_path.read_text(encoding="utf8"))
    except (OSError, json.JSONDecodeError) as error:
        issues.append(f"{record_path}: invalid JSON: {error}")
        continue
    if record.get("publicationState") != "PUBLISHED":
        continue
    published += 1
    if record.get("approved") is not True:
        issues.append(f"{record_path}: unapproved published record")
    approval = record.get("humanApproval", {})
    if approval.get("decision") != "GO" or not approval.get("authorizedBy") or not approval.get("approvedAt"):
        issues.append(f"{record_path}: human owner GO authorization missing")
    article_path = root / record.get("articlePath", "")
    if not article_path.is_file():
        issues.append(f"{record_path}: article file missing")
        continue
    article_bytes = article_path.read_bytes()
    article_sha256 = hashlib.sha256(article_bytes).hexdigest()
    if article_sha256 != record.get("articleSha256"):
        issues.append(f"{record_path}: article bytes differ from approved revision")
    if re.search(rb'<meta[^>]+name=["\']robots["\'][^>]+noindex', article_bytes, re.I):
        issues.append(f"{record_path}: published page still has noindex")
    evidence_path = root / record.get("evidencePath", "")
    if not evidence_path.is_file():
        issues.append(f"{record_path}: evidence snapshot missing")
    elif hashlib.sha256(evidence_path.read_bytes()).hexdigest() != record.get("evidenceSha256"):
        issues.append(f"{record_path}: evidence snapshot differs from approved evidence")

if mode == "PUBLICATION_ACTIVE" and published == 0:
    issues.append("PUBLICATION_ACTIVE requires at least one published article with owner GO")

if issues:
    print("SECURITY GATE FAIL: " + "; ".join(issues))
    sys.exit(1)
print(f"SECURITY GATE PASS: {published} published article(s) have exact human owner GO; autoPublish remains disabled")
