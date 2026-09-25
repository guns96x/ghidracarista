#!/usr/bin/env python3
"""
Strict Carista feature catalog validator.

Purpose:
- prevent generated/template metadata from being treated as implementation evidence;
- separate feature-name existence from implementation readiness;
- require per-feature provenance before any customization can be enabled for writes.

This validator intentionally fails closed.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

CATALOG = ROOT / "research/features/FEATURE_CATALOG.json"
DIAG = ROOT / "research/db/diagnostic_evidence.json"
COMMANDS = ROOT / "research/ghidra_export/commands_evidence.json"

CORE_STATUS = {
    "DIAG_AUTOSCAN": "CORE_CONFIRMED",
    "DIAG_CLEAR_DTC": "CORE_CONFIRMED",
    "TOOL_EPB_SERVICE": "COMMAND_CONFIRMED_FLOW_PARTIAL",
    "TOOL_DPF_REGENERATION": "COMMAND_CONFIRMED_FLOW_PARTIAL",
    "TOOL_BATTERY_REGISTRATION": "CLASS_CONFIRMED_MAPPING_INCOMPLETE",
    "TOOL_SERVICE_RESET": "CLASS_CONFIRMED_MAPPING_INCOMPLETE",
}

REQUIRED_PER_FEATURE_FIELDS = {
    "ecu_address",
    "protocol",
    "read_op",
    "write_op",
}

def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    catalog = load(CATALOG)
    diag = load(DIAG)
    commands_text = COMMANDS.read_text(encoding="utf-8", errors="ignore").lower()

    features = catalog.get("features", [])
    evidence = diag.get("entries", diag.get("evidence", []))

    result = {
        "catalog_total": len(features),
        "direct_protocol_evidence_count": sum(
            1 for e in evidence if str(e.get("confidence", "")).upper() == "VERIFIED"
        ),
        "core": [],
        "customizations": [],
        "errors": [],
    }

    seen = set()
    for f in features:
        fid = f.get("id")
        if not fid:
            result["errors"].append({"type": "MISSING_ID"})
            continue
        if fid in seen:
            result["errors"].append({"type": "DUPLICATE_ID", "id": fid})
        seen.add(fid)

        if fid in CORE_STATUS:
            result["core"].append({
                "id": fid,
                "status": CORE_STATUS[fid],
                "catalog_claim": f.get("confidence"),
            })
            continue

        name = str(f.get("internal_name", ""))
        exact_export_hit = bool(name) and name.lower() in commands_text

        # Generated feature records are NOT implementation-ready unless an
        # independently extracted per-feature evidence object is attached.
        ev = f.get("evidence")
        direct_ev = False
        if isinstance(ev, list):
            direct_ev = any(
                isinstance(x, dict)
                and str(x.get("strength", "")).upper() == "DIRECT"
                and x.get("source")
                and x.get("location")
                for x in ev
            )

        exact_mapping = bool(f.get("exact_mapping")) or direct_ev

        status = "NAME_CONFIRMED_IMPLEMENTATION_UNCONFIRMED"
        if exact_mapping:
            missing = [
                k for k in REQUIRED_PER_FEATURE_FIELDS
                if f.get(k) in (None, "", "UNKNOWN")
            ]
            status = "MAPPING_PARTIAL" if missing else "MAPPING_EVIDENCED"
        else:
            missing = sorted(REQUIRED_PER_FEATURE_FIELDS)

        result["customizations"].append({
            "id": fid,
            "internal_name": name,
            "status": status,
            "exact_name_in_committed_ghidra_export": exact_export_hit,
            "catalog_claim": f.get("confidence"),
            "missing_or_unproven": missing,
        })

        if str(f.get("confidence", "")).upper() == "VERIFIED" and not exact_mapping:
            result["errors"].append({
                "type": "UNSUPPORTED_VERIFIED_CLAIM",
                "id": fid,
                "reason": "No direct per-feature provenance/mapping attached.",
            })

    summary = {
        "catalog_total": result["catalog_total"],
        "core_count": len(result["core"]),
        "customization_count": len(result["customizations"]),
        "mapping_evidenced": sum(
            x["status"] == "MAPPING_EVIDENCED"
            for x in result["customizations"]
        ),
        "mapping_partial": sum(
            x["status"] == "MAPPING_PARTIAL"
            for x in result["customizations"]
        ),
        "name_only_unconfirmed": sum(
            x["status"] == "NAME_CONFIRMED_IMPLEMENTATION_UNCONFIRMED"
            for x in result["customizations"]
        ),
        "direct_protocol_evidence_count": result["direct_protocol_evidence_count"],
        "unsupported_verified_claims": sum(
            e["type"] == "UNSUPPORTED_VERIFIED_CLAIM"
            for e in result["errors"]
        ),
    }

    out = ROOT / "research/strict_catalog_validation.json"
    out.write_text(
        json.dumps({"summary": summary, **result}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))

    # Fail while generated/template VERIFIED claims remain.
    return 1 if summary["unsupported_verified_claims"] else 0

if __name__ == "__main__":
    sys.exit(main())
