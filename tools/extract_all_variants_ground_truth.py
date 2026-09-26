#!/usr/bin/env python3
"""
tools/extract_all_variants_ground_truth.py

Round 4 replacement. The previous version re-disassembled the binary with a 50-instruction
textual window and looked classes up by an unpinned factory map; that could not be reproduced
from committed data (MOLECULAR_AUDIT_ROUND4.md section 1) and is gone.

This step is now a pure, deterministic projection of the two committed dataflow artifacts:

    research/molecular/vag_setting_callsites.json     (tools/vag_setting_dataflow.py)
    research/molecular/resolved_factories_map.json    (tools/vag_setting_dataflow.py)

into research/molecular/all_binary_variants_ground_truth.json. It never touches the binary and
never invents a value: a field is populated only from a PROVEN constructor argument or from the
verified class semantics (tools/vag_class_semantics.py); otherwise it is null with the reason
kept in `field_provenance`.

Every callsite yields exactly one variant. Variants are never merged, deduplicated or reordered
by anything other than (source function, callsite address).
"""

import json
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from vag_class_semantics import CLASS_SEMANTICS  # noqa: E402

BASE_DIR = os.path.abspath(os.path.join(TOOLS_DIR, ".."))
CALLSITES_PATH = os.path.join(BASE_DIR, "research", "molecular", "vag_setting_callsites.json")
FACTORIES_PATH = os.path.join(BASE_DIR, "research", "molecular", "resolved_factories_map.json")
OUT_PATH = os.path.join(BASE_DIR, "research", "molecular", "all_binary_variants_ground_truth.json")

SCHEMA_VERSION = 2
ROLE_TO_FIELD = {"did": "did_or_channel", "channel": "did_or_channel",
                 "byte_position": "byte_offset", "mask": "bit_mask"}


def _arg_record(a):
    rec = {"index": a["index"], "kind": a["kind"], "type": a["type"], "status": a["status"]}
    for k in ("value", "def_chain", "reason", "at", "got_slot", "register"):
        if k in a:
            rec[k] = a[k]
    return rec


def _strip_ecu_object(name):
    return name.replace("&", "").strip() if name else None


def build_variant(cs, factories):
    args = [_arg_record(a) for a in cs["args"]]
    by_kind = {}
    for a in args:
        by_kind.setdefault(a["kind"], []).append(a)

    def proven_value(kind):
        lst = by_kind.get(kind, [])
        return lst[0]["value"] if lst and lst[0]["status"] == "PROVEN" else None

    name_arg = by_kind.get("name", [None])[0]
    setting_key = name_arg["value"] if name_arg and name_arg["status"] == "PROVEN" else None
    cls = cs["concrete_class"]
    helper = cs["helper_address"]
    ecu_arg = by_kind.get("ecu", [None])[0]
    ecu_object_class = None
    if ecu_arg:
        ecu_object_class = "VagCanEcu" if "VagCanEcu" in ecu_arg["type"] else (
            "VagUdsEcu" if "VagUdsEcu" in ecu_arg["type"] else None)

    variant = {
        "variant_id": f"{setting_key}@{cs['callsite']}",
        "setting_key": setting_key,
        "callsite": cs["callsite"],
        "asm_address": cs["callsite"],
        "source_function": cs["source_function"],
        "factory_helper_address": helper,
        "emplace_got_slot": cs["emplace_got_slot"],
        "factory_in_committed_map": helper in factories,
        "concrete_class": cls,
        "ecu": _strip_ecu_object(proven_value("ecu")),
        "ecu_object_class": ecu_object_class,
        "whitelist": proven_value("whitelist"),
        "interpretation": proven_value("interpretation"),
        "applicability_list": proven_value("applicability_list"),
        "applicability_list_present": "applicability_list" in by_kind,
        "did_or_channel": None,
        "id_role": None,
        "byte_offset": None,
        "bit_mask": None,
        "field_provenance": {},
        "semantics_status": None,
        "args": args,
    }

    sem = CLASS_SEMANTICS.get(cls)
    if sem is None:
        variant["semantics_status"] = "CLASS_SEMANTICS_UNVERIFIED"
        return variant

    name_pos = next((i for i, a in enumerate(args) if a["kind"] == "name"), None)
    layout_ok = (len(args) >= 3 and args[0]["kind"] == "ecu" and args[1]["kind"] == "whitelist"
                 and name_pos is not None)
    role_args = args[2:name_pos] if layout_ok else []
    if not layout_ok or len(role_args) != len(sem["int_roles"]):
        variant["semantics_status"] = "ARGUMENT_LAYOUT_MISMATCH"
        return variant
    variant["semantics_status"] = "VERIFIED"

    if sem["fixed_id"] is not None:
        variant["did_or_channel"] = sem["fixed_id"]
        variant["id_role"] = "class_fixed_id"
        variant["field_provenance"]["did_or_channel"] = {"source": "class_fixed_id",
                                                         "evidence": sem["evidence"]}
    for role, a in zip(sem["int_roles"], role_args):
        field = ROLE_TO_FIELD[role]
        if a["kind"] == "int" and a["status"] == "PROVEN":
            variant[field] = a["value"]
            if field == "did_or_channel":
                variant["id_role"] = role
            variant["field_provenance"][field] = {"source": "constructor_arg", "arg_index": a["index"],
                                                  "def_chain": a["def_chain"]}
        else:
            variant["field_provenance"][field] = {
                "source": "UNPROVEN", "arg_index": a["index"],
                "reason": a.get("reason") or f"argument kind {a['kind']} is not an integer"}
    return variant


def build(callsites_doc, factories_doc):
    factories = factories_doc["factories"]
    variants = [build_variant(cs, factories) for cs in callsites_doc["callsites"]]
    variants.sort(key=lambda v: (v["source_function"], int(v["callsite"], 16)))
    ids = [v["variant_id"] for v in variants]
    if len(set(ids)) != len(ids):
        raise RuntimeError("variant_id collision: the callsite address must make every id unique")
    meta = callsites_doc["metadata"]
    return {
        "metadata": {
            "schema_version": SCHEMA_VERSION,
            "binary_sha256": meta["binary_sha256"],
            "extractor_version": meta["extractor_version"],
            "source_functions": meta["source_functions"],
            "derived_from": ["research/molecular/vag_setting_callsites.json",
                             "research/molecular/resolved_factories_map.json"],
            "generator": "tools/extract_all_variants_ground_truth.py",
            "total_variants": len(variants),
            "rule": "one variant per constructor callsite; fields are populated only from PROVEN "
                    "constructor arguments or verified class semantics; nothing is merged or defaulted",
        },
        "variants": variants,
    }


def render_json(obj):
    return json.dumps(obj, indent=1, sort_keys=True) + "\n"


def main():
    with open(CALLSITES_PATH, encoding="utf-8") as fh:
        callsites = json.load(fh)
    with open(FACTORIES_PATH, encoding="utf-8") as fh:
        factories = json.load(fh)
    doc = build(callsites, factories)
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_json(doc))
    print(f"[+] {doc['metadata']['total_variants']} variants -> {OUT_PATH}")


if __name__ == "__main__":
    main()
