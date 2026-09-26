"""
tools/molecular_invariants.py

Relationship-based validators for the molecular artifacts (MOLECULAR_AUDIT_ROUND4.md section 6).

Every check compares one artifact against another artifact or against a recomputation from the
same records. No function here knows an expected result count; totals are only ever compared with
the records they summarise. Each check returns a list of human-readable violations (empty = ok),
so the same code validates real data in tests/molecular_validation.py and is proven to *fail*
on deliberately corrupted copies in tests/test_molecular_model.py.
"""

import json
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

import molecular_model as mm  # noqa: E402
from vag_class_semantics import CLASS_SEMANTICS  # noqa: E402
from vag_ecu_addressing import (  # noqa: E402
    VAG_CAN_ECU_ADDRESSES, VAG_UDS_ECU_ADDRESSES, resolve_ecu_transport)

TP2_ADAPTATION_SEQUENCE = ["31B9", "31BA", None, "31BB", "31BA"]  # None = local decode/modify step
FORBIDDEN_SYNTHETIC_ADAPTATION_SERVICES = ("21", "27")


def _flat(variants_by_key):
    return [v for lst in variants_by_key.values() for v in lst]


# ---------------------------------------------------------------------------
# 1. Evidence provenance / reproducibility relationships
# ---------------------------------------------------------------------------

def check_provenance_chain(callsites_doc, factories_doc, raw_doc, index_docs=()):
    out = []
    sha = {callsites_doc["metadata"]["binary_sha256"], factories_doc["metadata"]["binary_sha256"],
           raw_doc["metadata"]["binary_sha256"]}
    sha.update(d["metadata"]["binary_sha256"] for d in index_docs)
    if len(sha) != 1:
        out.append(f"artifacts pin different binaries: {sorted(sha)}")
    ver = {callsites_doc["metadata"]["extractor_version"], factories_doc["metadata"]["extractor_version"],
           raw_doc["metadata"]["extractor_version"]}
    if len(ver) != 1:
        out.append(f"artifacts come from different extractor versions: {sorted(ver)}")
    for fname, fn in callsites_doc["metadata"]["source_functions"].items():
        if not fn.get("address") or not fn.get("size"):
            out.append(f"source function {fname} has no pinned address/size")

    factories = factories_doc["factories"]
    for addr, f in factories.items():
        if f["helper_address"] != addr:
            out.append(f"factory {addr} is keyed by something other than its BL target ({f['helper_address']})")
        if f["helper_address"] == f["emplace_got_slot"] or f["helper_address"] == f["emplace_plt"]:
            out.append(f"factory {addr}: BL target conflated with PLT/GOT slot")
        if not f.get("emplace_symbol"):
            out.append(f"factory {addr} has no emplace symbol evidence")

    cs_keys = {}
    for cs in callsites_doc["callsites"]:
        k = (cs["source_function"], cs["callsite"])
        if k in cs_keys:
            out.append(f"duplicate callsite {k}")
        cs_keys[k] = cs
    raw_keys = {}
    for v in raw_doc["variants"]:
        k = (v["source_function"], v["callsite"])
        if k in raw_keys:
            out.append(f"duplicate raw variant for callsite {k}")
        raw_keys[k] = v
    if set(cs_keys) != set(raw_keys):
        out.append(f"raw variants and callsites differ: only-callsite={len(set(cs_keys) - set(raw_keys))} "
                   f"only-variant={len(set(raw_keys) - set(cs_keys))}")
    if raw_doc["metadata"]["total_variants"] != len(raw_doc["variants"]):
        out.append("raw metadata total_variants disagrees with the variant list")

    for k, v in raw_keys.items():
        cs = cs_keys.get(k)
        if cs is None:
            continue
        f = factories.get(v["factory_helper_address"])
        if f is None:
            out.append(f"{v['variant_id']}: factory {v['factory_helper_address']} absent from committed map")
        elif f["concrete_class"] != v["concrete_class"] or v["concrete_class"] != cs["concrete_class"]:
            out.append(f"{v['variant_id']}: class {v['concrete_class']} != factory class {f['concrete_class']}")
        if v["factory_helper_address"] != cs["helper_address"]:
            out.append(f"{v['variant_id']}: factory address differs from the callsite BL target")
        cs_args = {a["index"]: a for a in cs["args"]}
        for a in v["args"]:
            src = cs_args.get(a["index"])
            if src is None or src["status"] != a["status"] or src.get("value") != a.get("value") \
                    or src.get("def_chain") != a.get("def_chain"):
                out.append(f"{v['variant_id']}: arg {a['index']} differs from the dataflow callsite")
        for field, prov in v["field_provenance"].items():
            if prov["source"] == "constructor_arg":
                a = next((x for x in v["args"] if x["index"] == prov["arg_index"]), None)
                if a is None or a["status"] != "PROVEN" or v[field] != a.get("value") or not prov["def_chain"]:
                    out.append(f"{v['variant_id']}: {field} not backed by its PROVEN constructor argument")
            elif prov["source"] == "class_fixed_id":
                if CLASS_SEMANTICS.get(v["concrete_class"], {}).get("fixed_id") != v[field]:
                    out.append(f"{v['variant_id']}: {field} claims a class fixed id the class does not have")
            elif prov["source"] == "UNPROVEN":
                if v[field] is not None:
                    out.append(f"{v['variant_id']}: {field} populated although UNPROVEN")
    return out


# ---------------------------------------------------------------------------
# 2. Per-variant invariants
# ---------------------------------------------------------------------------

def check_flow(flow, protocol, evidence):
    out = []
    steps = flow["steps"]
    if [s["order"] for s in steps] != list(range(1, len(steps) + 1)):
        out.append("flow steps are not ordered 1..n")
    if flow["protocol"] != protocol:
        out.append(f"flow protocol {flow['protocol']} != variant protocol {protocol}")
    prefixes = [(s.get("request_prefix_hex") or s.get("request_hex")) for s in steps]
    for s in steps:
        if s.get("local"):
            continue
        p = s.get("request_prefix_hex") or s.get("request_hex")
        if not p:
            out.append(f"step {s['order']} has no request bytes")
            continue
        svc = p[:2]
        if protocol == mm.TP2 and svc in ("22", "2E"):
            out.append(f"TP2/KWP flow step {s['order']} uses UDS service {svc}")
        if protocol == mm.UDS and svc in ("1A", "3B", "21", "27"):
            out.append(f"UDS flow step {s['order']} uses KWP service {svc}")
        ev = evidence.get(s.get("evidence_id"))
        if ev is not None and "".join(ev["request"]).upper() != p[:len("".join(ev["request"]))]:
            out.append(f"step {s['order']} bytes {p} deviate from evidence {s['evidence_id']}")
    if flow["flow_id"] == "tp2_adaptation_channel_flow":
        if [p if not s.get("local") else None for p, s in zip(prefixes, steps)] != TP2_ADAPTATION_SEQUENCE:
            out.append(f"TP2 adaptation flow is not 31 B9 / 31 BA / modify / 31 BB / 31 BA read-back: {prefixes}")
        for s in steps:
            if not s.get("local") and (s.get("request_prefix_hex") or "")[:2] in FORBIDDEN_SYNTHETIC_ADAPTATION_SERVICES:
                out.append("synthetic 0x21/0x27 adaptation service present")
        if steps and steps[-1]["op"] != "read_back_verify":
            out.append("adaptation flow lacks a final read-back verification")
    else:
        if steps and steps[-1]["op"] != "read_back_verify":
            out.append("flow lacks a final read-back verification")
    return out


def check_variant_records(variants_by_key, raw_doc, factories_doc, evidence):
    out = []
    raw_by_id = {v["variant_id"]: v for v in raw_doc["variants"]}
    factories = factories_doc["factories"]
    for key, lst in variants_by_key.items():
        for v in lst:
            vid = v["variant_id"]
            if v["setting_key"] != key:
                out.append(f"{vid}: filed under key {key}")
            raw = raw_by_id.get(vid)
            if raw is None:
                out.append(f"{vid}: not present in raw variants")
                continue
            pm = v["protocol_model"]
            status = v["variant_status"]
            if pm["conflict"] and status != mm.ST_CONFLICT:
                out.append(f"{vid}: protocol conflict {pm['conflict_detail']} not rejected (status {status})")
            if status == mm.ST_CONFLICT and not pm["conflict"]:
                out.append(f"{vid}: marked conflict without a conflict")
            if v["executable"] != (status == mm.ST_EXACT):
                out.append(f"{vid}: executable flag disagrees with status {status}")
            if status != mm.ST_EXACT:
                if v["executable"]:
                    out.append(f"{vid}: non-exact variant is executable")
                if not v["blockers"]:
                    out.append(f"{vid}: non-exact variant has no blocker reason")
                continue

            # ---- EXACT invariants ------------------------------------------------
            if v["blockers"]:
                out.append(f"{vid}: EXACT variant carries blockers {v['blockers']}")
            for a in raw["args"]:
                if a["status"] != "PROVEN":
                    out.append(f"{vid}: EXACT with UNPROVEN argument {a['index']} ({a['kind']})")
                elif not a.get("def_chain"):
                    out.append(f"{vid}: EXACT argument {a['index']} has no definition chain (heuristic provenance)")
            fac = factories.get(v["factory_helper_address"])
            if fac is None or fac["concrete_class"] != v["concrete_class"]:
                out.append(f"{vid}: EXACT but factory not reproducible from the committed map")
            sem = CLASS_SEMANTICS.get(v["concrete_class"])
            if sem is None or v["semantics_status"] != "VERIFIED":
                out.append(f"{vid}: EXACT with unverified class semantics")
            if not isinstance(v["byte_offset"], int) or not isinstance(v["bit_mask"], int) or v["bit_mask"] <= 0:
                out.append(f"{vid}: EXACT with invalid byte_offset/bit_mask")
            for f in ("did_or_channel", "byte_offset", "bit_mask"):
                if v["field_provenance"].get(f, {}).get("source") not in ("constructor_arg", "class_fixed_id"):
                    out.append(f"{vid}: EXACT field {f} has no constructor/class provenance")
            if not v["whitelist"] or not v["interpretation"]:
                out.append(f"{vid}: EXACT without whitelist/interpretation")

            # ---- ECU: real table entry, protocol consistent, no borrowed IDs -------------
            ecu = v["ecu"]
            trans = resolve_ecu_transport(ecu.get("object"))
            if trans is None:
                out.append(f"{vid}: EXACT with ECU {ecu.get('object')} absent from the ECU tables (fabricated fallback?)")
            else:
                table_proto = mm.UDS if trans["protocol"].startswith("UDS") else mm.TP2
                if ecu["protocol"] != table_proto:
                    out.append(f"{vid}: ECU protocol {ecu['protocol']} != table protocol {table_proto}")
                if table_proto == mm.UDS and not (ecu.get("uds_tx_id") and ecu.get("uds_rx_id")):
                    out.append(f"{vid}: UDS ECU without TX/RX IDs")
                if table_proto == mm.TP2 and (ecu.get("uds_tx_id") or ecu.get("uds_rx_id")):
                    out.append(f"{vid}: KWP/TP2.0 ECU carries UDS CAN IDs borrowed from a same-named UDS ECU")
                if ecu["logical_address"] in (None, "UNKNOWN"):
                    out.append(f"{vid}: ECU without logical address")
                obj = ecu["object"] or ""
                if obj.startswith("VagUdsEcu::") and obj not in VAG_UDS_ECU_ADDRESSES:
                    out.append(f"{vid}: unknown UDS ECU object {obj}")
                if obj.startswith("VagCanEcu::") and obj not in VAG_CAN_ECU_ADDRESSES:
                    out.append(f"{vid}: unknown CAN ECU object {obj}")

            # ---- protocol agreement: class / ECU object / ECU table / request builder --------
            values = {k: pm[k] for k in ("class", "ecu_object", "ecu_table", "request_builder")}
            if any(x is None for x in values.values()) or len(set(values.values())) != 1:
                out.append(f"{vid}: protocol disagreement {values}")
            flow = v["request_flow"]
            if not flow:
                out.append(f"{vid}: EXACT without request flow")
                continue
            if flow["protocol"] != pm["runtime_protocol"] or flow["protocol"] != ecu["protocol"]:
                out.append(f"{vid}: request-builder protocol {flow['protocol']} != runtime transport "
                           f"{pm['runtime_protocol']} / ECU {ecu['protocol']}")
            out.extend(f"{vid}: {m}" for m in check_flow(flow, pm["runtime_protocol"], evidence))

            # ---- DID provenance: no defaulted F1A3 -----------------------------------------
            if v["concrete_class"] == "VagUdsAdaptationSetting" and \
                    v["field_provenance"]["did_or_channel"]["source"] != "constructor_arg":
                out.append(f"{vid}: UDS adaptation DID not taken from the constructor")
            if v["did_or_channel"] == 0xF1A3 and v["field_provenance"]["did_or_channel"]["source"] != "constructor_arg":
                out.append(f"{vid}: DID 0xF1A3 without constructor provenance")
    return out


# ---------------------------------------------------------------------------
# 3. Variant index and feature-level relationships
# ---------------------------------------------------------------------------

def check_variant_index(variants_index, raw_doc):
    out = []
    by_key = variants_index["variants_by_key"]
    flat = _flat(by_key)
    meta = variants_index["metadata"]
    if meta["total_binary_variants"] != len(flat):
        out.append("metadata.total_binary_variants disagrees with the indexed variants")
    if meta["total_unique_keys"] != len(by_key):
        out.append("metadata.total_unique_keys disagrees with the indexed keys")
    if meta["variant_status_counts"] != mm.status_counts(flat, "variant_status"):
        out.append("metadata.variant_status_counts disagrees with the indexed variants")
    raw_ids = [v["variant_id"] for v in raw_doc["variants"]]
    idx_ids = [v["variant_id"] for v in flat]
    if sorted(raw_ids) != sorted(idx_ids):
        out.append("variant index does not contain exactly the raw variants (collapsed or invented variants)")
    raw_per_key = {}
    for v in raw_doc["variants"]:
        raw_per_key[v["setting_key"]] = raw_per_key.get(v["setting_key"], 0) + 1
    for key, n in raw_per_key.items():
        if len(by_key.get(key, [])) != n:
            out.append(f"key {key}: {len(by_key.get(key, []))} indexed variants but {n} constructor callsites")
    return out


def check_features(catalog, variants_index, instances_doc, commands_doc, ready_doc, blocked_doc):
    out = []
    by_key = variants_index["variants_by_key"]
    inst = {i["id"]: i for i in instances_doc["instances"]}
    cat_ids = [f["id"] for f in catalog]
    if sorted(inst) != sorted(cat_ids):
        out.append("instance index does not cover exactly the catalog features")
    ready = {f["id"]: f for f in ready_doc["features"]}
    blocked = {f["id"]: f for f in blocked_doc["features"]}
    if set(ready) & set(blocked):
        out.append(f"features both READY and BLOCKED: {sorted(set(ready) & set(blocked))}")
    if set(ready) | set(blocked) != set(cat_ids):
        out.append("READY/BLOCKED do not partition the catalog")
    if instances_doc["metadata"]["counts"] != mm.status_counts(instances_doc["instances"], "resolution_status"):
        out.append("instance metadata.counts disagrees with the instance records")
    if instances_doc["metadata"]["total_instances"] != len(instances_doc["instances"]):
        out.append("instance metadata.total_instances disagrees with the records")
    if ready_doc["metadata"]["total_ready"] != len(ready_doc["features"]):
        out.append("READY metadata total disagrees with its records")
    if blocked_doc["metadata"]["total_blocked"] != len(blocked_doc["features"]):
        out.append("BLOCKED metadata total disagrees with its records")

    cmds_by_variant = {}
    for c in commands_doc["commands"]:
        k = (c["feature_id"], c["variant_id"])
        if k in cmds_by_variant:
            out.append(f"duplicate command entry {k}")
        cmds_by_variant[k] = c
    if commands_doc["metadata"]["total_commands"] != len(commands_doc["commands"]):
        out.append("command metadata.total_commands disagrees with the entries")
    if instances_doc["metadata"]["total_executable_variants"] != len(commands_doc["commands"]):
        out.append("instance metadata.total_executable_variants disagrees with the command entries")

    expected_cmds = set()
    for feat in catalog:
        fid = feat["id"]
        key = feat["internal_name"]
        fvars = by_key.get(key, [])
        cls = mm.classify_feature(feat, fvars)
        i = inst.get(fid)
        if i is None:
            continue
        if i["resolution_status"] != cls["state"]:
            out.append(f"{fid}: stated {i['resolution_status']} but variants imply {cls['state']}")
        if i["variants_count"] != len(fvars) or sorted(i["variant_ids"]) != sorted(v["variant_id"] for v in fvars):
            out.append(f"{fid}: instance variants do not match the variant index")
        exact = [v for v in fvars if v["variant_status"] == mm.ST_EXACT]
        if i["exact_variants_count"] != len(exact):
            out.append(f"{fid}: exact_variants_count disagrees with its variants")
        state = i["resolution_status"]
        in_ready = fid in ready
        if in_ready != (state == mm.FS_EXACT):
            out.append(f"{fid}: READY membership disagrees with state {state}")
        if in_ready and len(fvars) != 1:
            out.append(f"{fid}: READY feature collapses {len(fvars)} variants onto one executable command")
        if state == mm.FS_AMBIGUOUS:
            if fid not in blocked or blocked[fid]["blocking_class"] != "AMBIGUOUS_VARIANT_SELECTION":
                out.append(f"{fid}: ambiguous feature is not blocked as AMBIGUOUS_VARIANT_SELECTION")
            if sorted(i["exact_variant_ids"]) != sorted(v["variant_id"] for v in exact):
                out.append(f"{fid}: ambiguous feature does not list all of its exact variants")
        if state in (mm.FS_EXACT, mm.FS_AMBIGUOUS):
            for v in exact:
                expected_cmds.add((fid, v["variant_id"]))
                c = cmds_by_variant.get((fid, v["variant_id"]))
                if c is None:
                    out.append(f"{fid}: exact variant {v['variant_id']} missing from the command map (first-variant collapse)")
                    continue
                if c["feature_state"] != state or c["selection_required"] != (state != mm.FS_EXACT):
                    out.append(f"{c['variant_id']}: selection flags disagree with feature state {state}")
                if c["applicability_identity"] != v["applicability_identity"]:
                    out.append(f"{c['variant_id']}: command lacks the variant's applicability identity")
                if c["protocol"] != v["request_flow"]["protocol"] or c["request_flow"]["protocol"] != c["protocol"]:
                    out.append(f"{c['variant_id']}: command protocol != request-builder protocol")
                if c["protocol"] != v["protocol_model"]["runtime_protocol"] or c["ecu"]["protocol"] != c["protocol"]:
                    out.append(f"{c['variant_id']}: command protocol != runtime transport protocol")
                if c["request_flow"] != v["request_flow"]:
                    out.append(f"{c['variant_id']}: command flow differs from the variant flow")
        if state == mm.FS_REJECTED:
            if any(k[0] == fid for k in cmds_by_variant):
                out.append(f"{fid}: rejected operation appears in the setting command map")
            if fvars:
                out.append(f"{fid}: rejected operation has setting variants")
    for k in cmds_by_variant:
        if k not in expected_cmds:
            out.append(f"command {k} does not correspond to an exact variant of an executable/ambiguous feature")
    return out


def check_all(base_dir, loaded):
    """Runs every relationship check over loaded artifacts (see tests for the loader)."""
    evidence = mm.load_request_evidence(base_dir)
    out = []
    out += check_provenance_chain(loaded["callsites"], loaded["factories"], loaded["raw"],
                                  [loaded["variants"], loaded["instances"], loaded["commands"]])
    out += check_variant_records(loaded["variants"]["variants_by_key"], loaded["raw"], loaded["factories"], evidence)
    out += check_variant_index(loaded["variants"], loaded["raw"])
    out += check_features(loaded["catalog"], loaded["variants"], loaded["instances"], loaded["commands"],
                          loaded["ready"], loaded["blocked"])
    return out


def load_all(base_dir):
    def j(rel):
        with open(os.path.join(base_dir, rel), encoding="utf-8") as fh:
            return json.load(fh)
    mol = os.path.join("research", "molecular")
    return {
        "callsites": j(os.path.join(mol, "vag_setting_callsites.json")),
        "factories": j(os.path.join(mol, "resolved_factories_map.json")),
        "raw": j(os.path.join(mol, "all_binary_variants_ground_truth.json")),
        "variants": j(os.path.join(mol, "SETTING_VARIANTS_INDEX.json")),
        "instances": j(os.path.join(mol, "SETTING_INSTANCE_INDEX.json")),
        "commands": j(os.path.join(mol, "SETTING_TO_COMMAND_MAP.json")),
        "ready": j(os.path.join("handoff", "READY_FEATURES.json")),
        "blocked": j(os.path.join("handoff", "BLOCKED_FEATURES.json")),
        "catalog": mm.load_catalog(base_dir),
    }
