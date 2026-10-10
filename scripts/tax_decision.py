#!/usr/bin/env python3
"""Fail-closed ASN Pemda tax verification engine. No rates, no computation."""
import json
from datetime import date
from pathlib import Path
MATRIX=Path(__file__).resolve().parents[1]/"data/tax/decision-matrix.v0.1.json"
CHANNELS={"UP/GU","LS","KKPD","Marketplace","Lainnya"}
KINDS={"Belanja barang","Jasa katering","Makan-minum restoran","Jasa lainnya"}
SELLERS={"Orang pribadi","Badan usaha","Belum diketahui"}
DOCUMENTS={"Sudah diperiksa","Belum diperiksa","Tidak diketahui"}
def decide(payload, matrix_path=MATRIX):
    matrix=json.loads(Path(matrix_path).read_text(encoding="utf-8"))
    if matrix.get("status")!="PRE_RELEASE_NOT_AUTHORIZED":
        raise ValueError("UNEXPECTED_MATRIX_STATUS")
    rules=matrix.get("rules",[])
    if (not isinstance(rules,list) or len(rules)!=4 or
        any(not isinstance(r,dict) or r.get("autoCalculation") is not False for r in rules)):
        raise ValueError("UNSAFE_MATRIX")
    expected={"SPJ-GENERAL":("PERLU_VERIFIKASI",True),"MARKETPLACE-2026":("PERLU_VERIFIKASI",True),"NON-APPLICABLE":("TIDAK_BERLAKU",False),"READY":("DAPAT_DIHITUNG",False)}
    ids=[r.get("id") for r in rules]
    if any(not isinstance(item,str) for item in ids) or len(set(ids))!=4 or set(ids)!=set(expected):
        raise ValueError("UNEXPECTED_RULE_SET")
    if any((r.get("state"),r.get("enabled",True))!=expected[r["id"]] for r in rules):
        raise ValueError("UNSAFE_RULE_CONFIGURATION")
    if any(r.get("enabled",True) and r.get("state")!="PERLU_VERIFIKASI" for r in rules):
        raise ValueError("UNSAFE_ENABLED_STATE")
    if not isinstance(payload,dict):
        return {"state":"INPUT_ERROR","reason":"Payload must be an object."}
    amount=payload.get("amount")
    if isinstance(amount,bool) or not isinstance(amount,int) or amount<0 or amount>9007199254740991:
        return {"state":"INPUT_ERROR","reason":"Amount must be a safe nonnegative integer."}
    if (payload.get("channel") not in CHANNELS or payload.get("kind") not in KINDS
        or payload.get("seller") not in SELLERS or payload.get("documents") not in DOCUMENTS):
        return {"state":"INPUT_ERROR","reason":"Missing or unsupported classification field."}
    raw_date=payload.get("transactionDate")
    if raw_date is not None:
        if not isinstance(raw_date,str) or len(raw_date)!=10:
            return {"state":"INPUT_ERROR","reason":"Transaction date must be YYYY-MM-DD."}
        try:
            parsed=date.fromisoformat(raw_date)
        except ValueError:
            return {"state":"INPUT_ERROR","reason":"Invalid transaction date."}
        if parsed.isoformat()!=raw_date:
            return {"state":"INPUT_ERROR","reason":"Transaction date must be YYYY-MM-DD."}
    marketplace=payload["channel"]=="Marketplace"
    rule=next((r for r in rules if r.get("id")==("MARKETPLACE-2026" if marketplace else "SPJ-GENERAL")),None)
    if rule is None or rule.get("state")!="PERLU_VERIFIKASI":
        raise ValueError("MISSING_SAFE_RULE")
    checks=["Verify transaction date and goods/service classification",
            "Verify supplier tax status and documentary exemptions",
            "Verify applicable rules, collector, tax base, and rounding"]
    if raw_date is None:
        checks.insert(0,"Record transaction date before applying effective-date rules")
    if payload["channel"]=="KKPD":
        checks.insert(0,"Verify KKPD issuer, payment evidence, and legally responsible tax collector")
    if marketplace:
        checks.insert(0,"Verify designated platform, date, invoice, and proof of platform withholding")
        if raw_date is not None and parsed<date(2026,10,1):
            checks.insert(0,"Review historical marketplace rules: transaction predates 1 October 2026 announcement")
    return {"state":"PERLU_VERIFIKASI","ruleId":rule["id"],"reason":rule["reason"],
            "checks":checks,"taxAmount":None,"source":rule.get("source")}
