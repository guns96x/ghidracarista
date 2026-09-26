"""
tools/molecular_model.py

Variant-first molecular model (MOLECULAR_AUDIT_ROUND4.md).

Canonical shape:  Feature -> Variant[].

* A variant is one constructor callsite (tools/extract_all_variants_ground_truth.py).
* A variant is EXACT_VERIFIED only when every constructor argument is dataflow-PROVEN, its class
  semantics are verified, its factory is reproducible from the committed factory map, its ECU
  resolves, class / ECU object / ECU table / request builder agree on one protocol, and a
  request builder exists in committed evidence for that class.
* A feature is executable (EXACT_RESOLVED) only if it has exactly one variant and that variant is
  EXACT_VERIFIED. Any feature with several variants is AMBIGUOUS_MULTI_VARIANT: the runtime command
  map is variant-specific and carries the applicability identity a selector must match. Nothing
  here ever picks "the first" variant.

This module holds no result counts; every count is computed from the records it is given.
"""

import json
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from vag_class_semantics import CLASS_SEMANTICS  # noqa: E402
from vag_ecu_addressing import resolve_ecu_transport  # noqa: E402

BASE_DIR = os.path.abspath(os.path.join(TOOLS_DIR, ".."))

UDS = "UDS"
TP2 = "TP2.0/KWP2000"

ST_EXACT = "EXACT_VERIFIED"
ST_PARTIAL = "PARTIAL"
ST_CONFLICT = "PROTOCOL_CONFLICT"

FS_EXACT = "EXACT_RESOLVED"
FS_AMBIGUOUS = "AMBIGUOUS_MULTI_VARIANT"
FS_PARTIAL = "PARTIAL"
FS_UNRESOLVED = "UNRESOLVED"
FS_REJECTED = "REJECTED_TEMPLATE"

EVIDENCE_PATH = os.path.join("research", "db", "diagnostic_evidence.json")
FEATURE_CATALOG_PATH = os.path.join("research", "features", "FEATURE_CATALOG.json")

# Diagnostic / service operations that must never be represented as coding settings.
NOT_A_SETTING = {
    "DIAG_AUTOSCAN": "AutoScan is an ECU discovery diagnostic operation (22 04 A1), not a coding setting.",
    "DIAG_CLEAR_DTC": "ClearDiagnosticInformation is an atomic UDS service (14 FF FF FF), not a coding setting.",
    "TOOL_EPB_SERVICE": "EPB is a service tool with RoutineControl 0x03A1/0x03A0, not a coding setting.",
    "TOOL_DPF_REGENERATION": "DPF is a service tool with RoutineControl 0x053D, not a coding setting.",
    "TOOL_BATTERY_REGISTRATION": "Battery registration is a service routine, not a normal customization setting.",
    "TOOL_SERVICE_RESET": "Service reset is a service routine, not a normal customization setting.",
}

# Class -> the request builder committed evidence supports. `id_role` says which constructor
# field supplies the DID/channel; the builder refuses a variant whose id came from anywhere else.
REQUEST_BUILDERS = {
    "VagCanShortAdaptationSetting": {"protocol": TP2, "flow": "tp2_adaptation_channel_flow", "id_role": "channel"},
    "VagCanLongCodingSetting": {"protocol": TP2, "flow": "tp2_long_coding_rmw", "id_role": "class_fixed_id"},
    "VagUdsCodingSetting": {"protocol": UDS, "flow": "uds_did_rmw", "id_role": "class_fixed_id"},
    "VagUdsAdaptationSetting": {"protocol": UDS, "flow": "uds_did_rmw", "id_role": "did"},
}

SECURITY_NOTE = ("Security Access / SFD requirements are not established by committed evidence. "
                 "No unlock or bypass is performed or modelled; an ECU that refuses the request keeps the "
                 "setting non-writable.")


class ModelError(Exception):
    pass


# ---------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------

def load_request_evidence(base_dir=BASE_DIR):
    with open(os.path.join(base_dir, EVIDENCE_PATH), encoding="utf-8") as fh:
        entries = json.load(fh)["entries"]
    return {e["id"]: e for e in entries}


def evidence_prefix(evidence, evidence_id, protocol):
    """Request bytes come from committed VERIFIED evidence, never from literals in this module."""
    e = evidence.get(evidence_id)
    if e is None:
        raise ModelError(f"evidence entry {evidence_id} is not committed")
    if e["confidence"] != "VERIFIED":
        raise ModelError(f"evidence entry {evidence_id} is {e['confidence']}, not VERIFIED")
    if e["protocol"] != ("TP2.0" if protocol == TP2 else "UDS"):
        raise ModelError(f"evidence entry {evidence_id} is protocol {e['protocol']}, not {protocol}")
    return "".join(e["request"]).upper(), "".join(e["response_prefix"]).upper()


def load_protocol_docs(base_dir=BASE_DIR):
    docs = {}
    for name in ("uds.md", "coding.md", "adaptation.md"):
        with open(os.path.join(base_dir, "research", "protocols", name), encoding="utf-8") as fh:
            docs[name] = fh.read()
    return docs


def uds_services(docs):
    """UDS 22/2E are documented (not tabulated) evidence; confirm the docs still say so."""
    uds = docs["uds.md"]
    if "22 <DID_High> <DID_Low>" not in uds or "2E <DID_High> <DID_Low>" not in uds:
        raise ModelError("research/protocols/uds.md no longer documents 22/2E <DID>")
    return {"read": "22", "write": "2E", "read_response": "62", "write_response": "6E"}


# ---------------------------------------------------------------------------
# Protocol model
# ---------------------------------------------------------------------------

def class_protocol(cls):
    """Protocol implied by the setting class family; None when the class is not one of them."""
    if not cls:
        return None
    if cls.startswith("VagUds"):
        return UDS
    if cls.startswith("VagCan") or cls.startswith("FullByteVagCan"):
        return TP2
    return None


def ecu_object_protocol(ecu_object_class):
    return {"VagUdsEcu": UDS, "VagCanEcu": TP2}.get(ecu_object_class)


def _table_protocol(trans):
    if not trans:
        return None
    return UDS if trans["protocol"].startswith("UDS") else TP2


def protocol_model(raw, ecu_trans, builder):
    m = {
        "class": class_protocol(raw["concrete_class"]),
        "ecu_object": ecu_object_protocol(raw.get("ecu_object_class")),
        "ecu_table": _table_protocol(ecu_trans),
        "request_builder": builder["protocol"] if builder else None,
    }
    present = {k: v for k, v in m.items() if v}
    m["conflict"] = len(set(present.values())) > 1
    m["conflict_detail"] = present if m["conflict"] else None
    m["runtime_protocol"] = next(iter(set(present.values()))) if present and not m["conflict"] else None
    return m


# ---------------------------------------------------------------------------
# Request flows
# ---------------------------------------------------------------------------

def _operand(name, source, value=None):
    op = {"name": name, "source": source}
    if value is not None:
        op["value"] = value
    return op


def _modify_step(order, raw):
    return {"order": order, "op": "decode_modify", "local": True,
            "byte_offset": raw["byte_offset"], "bit_mask": raw["bit_mask"],
            "interpretation": raw["interpretation"]}


def build_request_flow(raw, evidence, docs):
    """Ordered read -> modify -> write -> read-back flow for one variant, or ModelError."""
    builder = REQUEST_BUILDERS.get(raw["concrete_class"])
    if builder is None:
        raise ModelError(f"no committed request-builder evidence for {raw['concrete_class']}")
    if raw.get("id_role") != builder["id_role"]:
        raise ModelError(f"{raw['concrete_class']} expects id_role {builder['id_role']}, got {raw.get('id_role')}")
    ident = raw["did_or_channel"]
    if not isinstance(ident, int) or ident < 0:
        raise ModelError("DID/channel is not a proven non-negative integer")
    flow = builder["flow"]

    if flow == "tp2_adaptation_channel_flow":
        if ident > 0xFF:
            raise ModelError(f"adaptation channel {ident} does not fit one byte")
        sel, sel_r = evidence_prefix(evidence, "vag_tp20_set_adaptation_channel", TP2)
        rd, rd_r = evidence_prefix(evidence, "vag_tp20_read_adaptation_data", TP2)
        wr, wr_r = evidence_prefix(evidence, "vag_tp20_write_adaptation_data", TP2)
        steps = [
            {"order": 1, "op": "select_channel", "request_prefix_hex": sel, "expect_response_prefix_hex": sel_r,
             "operands": [_operand("channel", "constructor_arg", ident)],
             "evidence_id": "vag_tp20_set_adaptation_channel"},
            {"order": 2, "op": "read_adaptation_data", "request_prefix_hex": rd, "expect_response_prefix_hex": rd_r,
             "operands": [], "evidence_id": "vag_tp20_read_adaptation_data",
             "note": "research/protocols/adaptation.md documents a <Channel> operand for this request; "
                     "committed VERIFIED evidence only asserts the 31 BA prefix, so none is emitted."},
            _modify_step(3, raw),
            {"order": 4, "op": "write_adaptation_data", "request_prefix_hex": wr, "expect_response_prefix_hex": wr_r,
             "operands": [_operand("modified_value", "step_3")], "evidence_id": "vag_tp20_write_adaptation_data"},
            {"order": 5, "op": "read_back_verify", "request_prefix_hex": rd, "expect_response_prefix_hex": rd_r,
             "operands": [], "evidence_id": "vag_tp20_read_adaptation_data",
             "compare": {"against": "step_3", "byte_offset": raw["byte_offset"], "bit_mask": raw["bit_mask"]}},
        ]
        evidence_ids = ["vag_tp20_set_adaptation_channel", "vag_tp20_read_adaptation_data",
                        "vag_tp20_write_adaptation_data"]
    elif flow == "tp2_long_coding_rmw":
        rd, rd_r = evidence_prefix(evidence, "vag_tp20_read_long_coding", TP2)
        wr, wr_r = evidence_prefix(evidence, "vag_tp20_write_coding", TP2)
        steps = [
            {"order": 1, "op": "read_long_coding", "request_prefix_hex": rd, "expect_response_prefix_hex": rd_r,
             "operands": [], "evidence_id": "vag_tp20_read_long_coding"},
            _modify_step(2, raw),
            {"order": 3, "op": "write_coding", "request_prefix_hex": wr, "expect_response_prefix_hex": wr_r,
             "operands": [_operand("coding_bytes", "step_2")], "evidence_id": "vag_tp20_write_coding"},
            {"order": 4, "op": "read_back_verify", "request_prefix_hex": rd, "expect_response_prefix_hex": rd_r,
             "operands": [], "evidence_id": "vag_tp20_read_long_coding",
             "compare": {"against": "step_2", "byte_offset": raw["byte_offset"], "bit_mask": raw["bit_mask"]}},
        ]
        evidence_ids = ["vag_tp20_read_long_coding", "vag_tp20_write_coding"]
    elif flow == "uds_did_rmw":
        if ident > 0xFFFF:
            raise ModelError(f"DID {ident:#x} does not fit two bytes")
        svc = uds_services(docs)
        if raw["id_role"] == "class_fixed_id" and (ident != 0x600 or "22 06 00" not in docs["coding.md"]):
            raise ModelError("UDS coding DID must equal the constructor's fixed id and match "
                             "research/protocols/coding.md (22 06 00)")
        did_hex = f"{ident:04X}"
        steps = [
            {"order": 1, "op": "read_data_by_identifier", "request_hex": svc["read"] + did_hex,
             "expect_response_prefix_hex": svc["read_response"] + did_hex,
             "operands": [_operand("did", "constructor_arg" if raw["id_role"] == "did" else "class_fixed_id", ident)],
             "evidence_id": "research/protocols/uds.md#3-read-data-by-identifier"},
            _modify_step(2, raw),
            {"order": 3, "op": "write_data_by_identifier", "request_prefix_hex": svc["write"] + did_hex,
             "expect_response_prefix_hex": svc["write_response"] + did_hex,
             "operands": [_operand("modified_value", "step_2")],
             "evidence_id": "research/protocols/uds.md#4-write-data-by-identifier"},
            {"order": 4, "op": "read_back_verify", "request_hex": svc["read"] + did_hex,
             "expect_response_prefix_hex": svc["read_response"] + did_hex, "operands": [],
             "evidence_id": "research/protocols/uds.md#3-read-data-by-identifier",
             "compare": {"against": "step_2", "byte_offset": raw["byte_offset"], "bit_mask": raw["bit_mask"]}},
        ]
        evidence_ids = ["research/protocols/uds.md", "research/protocols/coding.md"
                        if raw["id_role"] == "class_fixed_id" else "research/protocols/adaptation.md"]
    else:
        raise ModelError(f"unknown flow {flow}")

    return {"flow_id": flow, "protocol": builder["protocol"], "steps": steps,
            "evidence_ids": evidence_ids, "security_note": SECURITY_NOTE}


# ---------------------------------------------------------------------------
# Variant evaluation
# ---------------------------------------------------------------------------

def _field_blockers(raw, sem_ok):
    out = []
    bo, mask = raw.get("byte_offset"), raw.get("bit_mask")
    if sem_ok:
        if not isinstance(bo, int) or bo < 0:
            out.append("byte_offset_not_proven")
        if not isinstance(mask, int) or not (0 < mask <= 0xFF):
            out.append("bit_mask_not_proven_or_out_of_byte_range")
        if raw.get("did_or_channel") is None:
            out.append("did_or_channel_not_proven")
    return out


def applicability_identity(raw):
    return {
        "concrete_class": raw["concrete_class"],
        "ecu_object": raw.get("ecu"),
        "whitelist": raw.get("whitelist"),
        "applicability_list": ("ABSENT" if not raw.get("applicability_list_present")
                               else (raw.get("applicability_list") or "UNPROVEN")),
    }


def evaluate_variant(raw, evidence, docs, factories):
    """Turns one raw variant into an evaluated variant record (no args, full verdict)."""
    blockers = []
    unproven = []
    for a in raw["args"]:
        if a["status"] != "PROVEN":
            unproven.append({"arg_index": a["index"], "kind": a["kind"], "reason": a.get("reason", "unspecified")})
            blockers.append(f"unproven_argument[{a['kind']}]: {a.get('reason', 'unspecified')}")
        elif not a.get("def_chain") and a["kind"] != "name":
            blockers.append(f"heuristic_argument[{a['kind']}]: PROVEN without a definition chain")

    fac = factories.get(raw["factory_helper_address"])
    if fac is None or fac.get("concrete_class") != raw["concrete_class"]:
        blockers.append("factory_not_reproducible_from_committed_map")

    sem_ok = raw["semantics_status"] == "VERIFIED"
    if not sem_ok:
        blockers.append(raw["semantics_status"] or "CLASS_SEMANTICS_UNVERIFIED")
    blockers.extend(_field_blockers(raw, sem_ok))
    if raw.get("setting_key") is None:
        blockers.append("setting_key_not_proven")

    trans = resolve_ecu_transport(raw["ecu"]) if raw.get("ecu") else None
    if not trans:
        blockers.append("ecu_transport_unresolved")

    builder = REQUEST_BUILDERS.get(raw["concrete_class"])
    if builder is None:
        blockers.append(f"no_request_builder_evidence[{raw['concrete_class']}]")

    pm = protocol_model(raw, trans, builder)
    if pm["conflict"]:
        blockers.append("protocol_conflict: " + ", ".join(f"{k}={v}" for k, v in sorted(pm["conflict_detail"].items())))

    # The ordered flow depends only on class semantics, proven id/offset/mask and a consistent
    # protocol; it is attached to blocked variants too (as documentation of what the class would
    # do) but only EXACT_VERIFIED variants are executable.
    flow = None
    structural = ("unproven_argument[int]", "byte_offset_not_proven", "bit_mask_not_proven",
                  "did_or_channel_not_proven", "CLASS_SEMANTICS", "ARGUMENT_LAYOUT", "no_request_builder",
                  "protocol_conflict", "ecu_transport_unresolved", "setting_key_not_proven")
    if builder and not pm["conflict"] and sem_ok and trans and not any(
            b.startswith(structural) for b in blockers):
        try:
            flow = build_request_flow(raw, evidence, docs)
        except ModelError as exc:
            blockers.append(f"request_flow_unbuildable: {exc}")

    if pm["conflict"]:
        status = ST_CONFLICT
    elif blockers:
        status = ST_PARTIAL
    else:
        status = ST_EXACT

    ecu = None
    if trans:
        is_uds = trans["protocol"].startswith("UDS")
        ecu = {"object": raw["ecu"], "object_class": raw.get("ecu_object_class"), "name": trans["name"],
               "logical_address": trans["logical_address"], "protocol": _table_protocol(trans),
               "uds_tx_id": trans.get("uds_tx_id") if is_uds else None,
               "uds_rx_id": trans.get("uds_rx_id") if is_uds else None,
               "is_29bit": bool(trans.get("is_29bit"))}

    keep = ("variant_id", "setting_key", "callsite", "asm_address", "source_function", "factory_helper_address",
            "concrete_class", "whitelist", "interpretation", "did_or_channel", "id_role", "byte_offset",
            "bit_mask", "field_provenance", "semantics_status")
    rec = {k: raw.get(k) for k in keep}
    rec.update({
        "ecu": ecu if ecu else {"object": raw.get("ecu"), "object_class": raw.get("ecu_object_class"),
                                "name": None, "logical_address": None, "protocol": None,
                                "uds_tx_id": None, "uds_rx_id": None, "is_29bit": False},
        "protocol_model": pm,
        "applicability_identity": applicability_identity(raw),
        "variant_status": status,
        "executable": status == ST_EXACT and flow is not None,
        "blockers": blockers,
        "unproven_arguments": unproven,
        "request_flow": flow,
    })
    return rec


# ---------------------------------------------------------------------------
# Feature classification
# ---------------------------------------------------------------------------

def _identity_key(v):
    return json.dumps(v["applicability_identity"], sort_keys=True)


def classify_feature(feature, variants):
    """State of one catalog feature given ALL its evaluated variants."""
    fid = feature["id"]
    if fid in NOT_A_SETTING or fid.startswith("DIAG_") or fid.startswith("TOOL_"):
        return {"state": FS_REJECTED, "reason": NOT_A_SETTING.get(
            fid, "Operation belongs in the dedicated diagnostic or service index.")}
    if not variants:
        return {"state": FS_UNRESOLVED, "reason": "no dataflow-proven factory callsite for this key in the analysed getSettings() functions (absence of proof, not proof of absence)"}
    exact = [v for v in variants if v["variant_status"] == ST_EXACT]
    if len(variants) == 1 and exact:
        return {"state": FS_EXACT, "variant_id": exact[0]["variant_id"]}
    if len(variants) > 1 and exact:
        idents = {}
        for v in exact:
            idents.setdefault(_identity_key(v), []).append(v["variant_id"])
        return {"state": FS_AMBIGUOUS,
                "reason": "multiple variants; no runtime selector resolves exactly one applicable variant",
                "exact_variant_ids": [v["variant_id"] for v in exact],
                "identity_collisions": sorted(ids for ids in idents.values() if len(ids) > 1)}
    return {"state": FS_PARTIAL, "reason": "no variant is EXACT_VERIFIED"}


def blocking_class(state, variants):
    if state == FS_REJECTED:
        return "NOT_A_SETTING"
    if state == FS_UNRESOLVED:
        return "NO_PROVEN_CALLSITE"
    if state == FS_AMBIGUOUS:
        return "AMBIGUOUS_VARIANT_SELECTION"
    if state == FS_PARTIAL:
        if variants and all(v["variant_status"] == ST_CONFLICT for v in variants):
            return "PROTOCOL_CONFLICT_REJECTED"
        return "BLOCKED_EVIDENCE"
    return None


def blocker_summary(variants):
    codes = {}
    for v in variants:
        for b in v["blockers"]:
            code = b.split(":")[0]
            codes[code] = codes.get(code, 0) + 1
    return dict(sorted(codes.items()))


def status_counts(items, key):
    out = {}
    for it in items:
        out[it[key]] = out.get(it[key], 0) + 1
    return dict(sorted(out.items()))


def command_entry(feature, variant, feature_state):
    flow = variant["request_flow"]
    ecu = variant["ecu"]
    return {
        "variant_id": variant["variant_id"],
        "feature_id": feature["id"],
        "setting_key": variant["setting_key"],
        "feature_state": feature_state,
        "selection_required": feature_state != FS_EXACT,
        "concrete_class": variant["concrete_class"],
        "protocol": flow["protocol"],
        "ecu": ecu,
        "applicability_identity": variant["applicability_identity"],
        "did_or_channel": variant["did_or_channel"],
        "byte_offset": variant["byte_offset"],
        "bit_mask": variant["bit_mask"],
        "interpretation": variant["interpretation"],
        "request_flow": flow,
        "post_verify_read": True,
        "callsite_evidence": f"libCarista.so asm {variant['asm_address']} ({variant['source_function']})",
    }


def load_catalog(base_dir=BASE_DIR):
    with open(os.path.join(base_dir, FEATURE_CATALOG_PATH), encoding="utf-8") as fh:
        feats = json.load(fh)["features"]
    return [{"id": f["id"], "internal_name": f.get("internal_name") or f.get("setting_key", ""),
             "user_visible_name": f.get("user_visible_name", ""), "category": f.get("category", "")}
            for f in feats]
