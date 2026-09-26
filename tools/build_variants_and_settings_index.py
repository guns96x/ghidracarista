#!/usr/bin/env python3
"""
tools/build_variants_and_settings_index.py

Round 4 builder: derives every downstream molecular artifact from committed inputs only

    research/molecular/all_binary_variants_ground_truth.json   (per-callsite variants)
    research/molecular/resolved_factories_map.json             (factory reproducibility map)
    research/db/diagnostic_evidence.json + research/protocols/*.md   (request evidence)
    research/features/FEATURE_CATALOG.json                     (feature list; read-only)

and writes

    research/molecular/SETTING_VARIANTS_INDEX.json     all variants, grouped by key (never collapsed)
    research/molecular/SETTING_INSTANCE_INDEX.json     one record per catalog feature, with its state
    research/molecular/SETTING_TO_COMMAND_MAP.json     VARIANT-specific commands (schema_version 2)
    handoff/READY_FEATURES.json / BLOCKED_FEATURES.json

The previous version read READY/BLOCKED_FEATURES.json as its own catalog input (circular) and
published `exact_v[0]` as the feature's command. Neither survives here. Output is deterministic:
no timestamps, sorted keys, stable ordering.
"""

import json
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

import molecular_model as mm  # noqa: E402

BASE_DIR = mm.BASE_DIR
MOL = os.path.join("research", "molecular")
OUTPUTS = {
    "variants": os.path.join(MOL, "SETTING_VARIANTS_INDEX.json"),
    "instances": os.path.join(MOL, "SETTING_INSTANCE_INDEX.json"),
    "commands": os.path.join(MOL, "SETTING_TO_COMMAND_MAP.json"),
    "ready": os.path.join("handoff", "READY_FEATURES.json"),
    "blocked": os.path.join("handoff", "BLOCKED_FEATURES.json"),
}
SCHEMA_VERSION = 2


def render_json(obj):
    return json.dumps(obj, indent=1, sort_keys=True) + "\n"


def is_option_alias(key):
    if key in ("car_setting_yes", "car_setting_no", "car_setting_enabled", "car_setting_disabled",
               "car_setting_on", "car_setting_off", "car_setting_open", "car_setting_closed",
               "car_setting_none"):
        return True, "car_setting_general"
    if "_cca_" in key or "_ah_" in key:
        return True, "car_setting_battery_capacity_and_type"
    if key.startswith("car_setting_battery_technology_"):
        return True, "car_setting_battery_technology"
    return False, None


def _load(base_dir, rel):
    with open(os.path.join(base_dir, rel), encoding="utf-8") as fh:
        return json.load(fh)


def build(base_dir=BASE_DIR):
    raw_doc = _load(base_dir, os.path.join(MOL, "all_binary_variants_ground_truth.json"))
    factories = _load(base_dir, os.path.join(MOL, "resolved_factories_map.json"))["factories"]
    evidence = mm.load_request_evidence(base_dir)
    docs = mm.load_protocol_docs(base_dir)
    catalog = mm.load_catalog(base_dir)
    meta = raw_doc["metadata"]

    evaluated = [mm.evaluate_variant(r, evidence, docs, factories) for r in raw_doc["variants"]]
    variants_by_key = {}
    for v in evaluated:
        variants_by_key.setdefault(v["setting_key"], []).append(v)
    for lst in variants_by_key.values():
        lst.sort(key=lambda v: int(v["callsite"], 16))

    # ---- per-feature classification -------------------------------------------------
    instances, commands, ready, blocked = [], [], [], []
    for feat in catalog:
        key = feat["internal_name"]
        fvars = variants_by_key.get(key, [])
        cls = mm.classify_feature(feat, fvars)
        state = cls["state"]
        alias, parent = is_option_alias(key)
        inst = {"id": feat["id"], "setting_key": key, "user_visible_name": feat["user_visible_name"],
                "category": feat["category"], "is_alias": alias, "parent_setting_key": parent,
                "resolution_status": state, "variants_count": len(fvars),
                "exact_variants_count": sum(1 for v in fvars if v["variant_status"] == mm.ST_EXACT),
                "variant_ids": [v["variant_id"] for v in fvars]}
        if state == mm.FS_REJECTED:
            inst["rejection_reason"] = cls["reason"]
            inst["target_index"] = ("DIAGNOSTIC_OPERATIONS_INDEX.json" if feat["id"].startswith("DIAG")
                                    else "SERVICE_TOOL_INDEX.json")
        elif state == mm.FS_EXACT:
            v = fvars[0]
            inst.update({"variant_id": v["variant_id"], "concrete_setting_class": v["concrete_class"],
                         "protocol": v["request_flow"]["protocol"], "ecu": v["ecu"],
                         "did_or_channel": v["did_or_channel"], "byte_offset": v["byte_offset"],
                         "mask": v["bit_mask"], "whitelist": v["whitelist"],
                         "interpretation": v["interpretation"],
                         "exact_evidence_location": f"libCarista.so asm {v['asm_address']} ({v['source_function']})",
                         "field_provenance": v["field_provenance"]})
        elif state == mm.FS_AMBIGUOUS:
            inst.update({"exact_variant_ids": cls["exact_variant_ids"],
                         "identity_collisions": cls["identity_collisions"],
                         "selection_reason": cls["reason"]})
        if fvars and state != mm.FS_EXACT:
            inst["variant_summary"] = [{"variant_id": v["variant_id"], "status": v["variant_status"],
                                        "concrete_class": v["concrete_class"],
                                        "ecu_object": v["ecu"]["object"], "whitelist": v["whitelist"],
                                        "blockers": v["blockers"]} for v in fvars]
        instances.append(inst)

        # command map: every EXACT variant, variant-specific, regardless of feature state
        for v in fvars:
            if v["executable"] and state in (mm.FS_EXACT, mm.FS_AMBIGUOUS):
                commands.append(mm.command_entry(feat, v, state))

        if state == mm.FS_EXACT:
            v = fvars[0]
            ready.append({"id": feat["id"], "internal_name": key, "user_visible_name": feat["user_visible_name"],
                          "category": feat["category"], "variant_id": v["variant_id"],
                          "ecu_object": v["ecu"]["object"], "ecu_address": v["ecu"]["logical_address"],
                          "protocol": v["request_flow"]["protocol"], "request_flow_id": v["request_flow"]["flow_id"]})
        else:
            blocked.append({"id": feat["id"], "internal_name": key, "user_visible_name": feat["user_visible_name"],
                            "category": feat["category"], "state": state,
                            "blocking_class": mm.blocking_class(state, fvars),
                            "blocking_reason": cls.get("reason", ""),
                            "variants_count": len(fvars),
                            "exact_variant_ids": cls.get("exact_variant_ids", []),
                            "blocker_summary": mm.blocker_summary(fvars)})

    commands.sort(key=lambda c: (c["feature_id"], c["variant_id"]))
    counts = mm.status_counts(instances, "resolution_status")
    vcounts = mm.status_counts(evaluated, "variant_status")
    provenance = {"binary_sha256": meta["binary_sha256"], "extractor_version": meta["extractor_version"],
                  "generator": "tools/build_variants_and_settings_index.py"}

    outputs = {
        OUTPUTS["variants"]: {
            "metadata": dict(provenance, schema_version=SCHEMA_VERSION,
                             title="Carista molecular setting variants index (all variants preserved)",
                             total_binary_variants=len(evaluated), total_unique_keys=len(variants_by_key),
                             variant_status_counts=vcounts),
            "variants_by_key": variants_by_key},
        OUTPUTS["instances"]: {
            "metadata": dict(provenance, schema_version=SCHEMA_VERSION,
                             title="Carista molecular setting instance index (Feature -> Variant[])",
                             counts=counts, total_instances=len(instances),
                             total_executable_variants=len(commands)),
            "instances": instances},
        OUTPUTS["commands"]: {
            "metadata": dict(provenance, schema_version=SCHEMA_VERSION,
                             title="Variant-specific verified setting command map",
                             total_commands=len(commands),
                             rule="One entry per EXACT_VERIFIED variant. Entries whose feature has several "
                                  "variants carry selection_required=true and the applicability_identity a "
                                  "runtime selector must match; no entry stands for the whole feature.",
                             deprecated_keys="v1 keys read_command_hex/write_command_hex/ecu_address/ecu_tx_id/"
                                             "ecu_rx_id/service_read/service_write were removed; see request_flow "
                                             "and ecu. v1 entries were keyed by feature id and collapsed variants."),
            "commands": commands},
        OUTPUTS["ready"]: {
            "metadata": dict(provenance, schema_version=SCHEMA_VERSION,
                             title="Features executable without variant selection", total_ready=len(ready)),
            "features": ready},
        OUTPUTS["blocked"]: {
            "metadata": dict(provenance, schema_version=SCHEMA_VERSION,
                             title="Blocked, ambiguous, partial, unresolved and rejected features",
                             total_blocked=len(blocked), state_counts=counts),
            "features": blocked},
    }
    return outputs


def main():
    outputs = build()
    for rel, obj in outputs.items():
        with open(os.path.join(BASE_DIR, rel), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_json(obj))
        print(f"[+] wrote {rel}")
    counts = outputs[OUTPUTS["instances"]]["metadata"]["counts"]
    print("feature states:", counts)
    print("variant statuses:", outputs[OUTPUTS["variants"]]["metadata"]["variant_status_counts"])
    print("executable variants:", outputs[OUTPUTS["instances"]]["metadata"]["total_executable_variants"])


if __name__ == "__main__":
    main()
