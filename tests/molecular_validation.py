#!/usr/bin/env python3
"""
tests/molecular_validation.py

Relationship-based validator for the Carista molecular decomposition artifacts
(MOLECULAR_AUDIT_ROUND2/3/4). It contains NO hard-coded expected result counts: every total is
compared with the records it summarises (tools/molecular_invariants.py), and states such as
EXACT/PARTIAL/UNRESOLVED are recomputed from variant evidence rather than asserted.

Known bad cases it must reject are exercised on corrupted copies in tests/test_molecular_model.py.

Run:  python tests/molecular_validation.py
"""

import ast
import json
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

import molecular_invariants as mi  # noqa: E402
import molecular_model as mm  # noqa: E402
from vag_ecu_addressing import VAG_UDS_ECU_ADDRESSES, resolve_ecu_transport  # noqa: E402

REQUIRED_FILES = [
    "research/molecular/PACKAGE_MAP.md", "research/molecular/package_tree.json",
    "research/molecular/UI_SCREEN_GRAPH.json", "research/molecular/UI_SCREEN_GRAPH.md",
    "research/molecular/DEX_CLASS_INDEX.json", "research/molecular/DEX_DEPENDENCY_GRAPH.json",
    "research/molecular/NATIVE_CLASS_INDEX.json", "research/molecular/JNI_BRIDGE_MAP.json",
    "research/molecular/NATIVE_CALL_GRAPH.md", "research/molecular/TRANSPORT_STACK.md",
    "research/molecular/transport_state_machines/ble_state_machine.json",
    "research/molecular/transport_state_machines/rfcomm_spp_state_machine.json",
    "research/molecular/transport_state_machines/elm327_stn_state_machine.json",
    "research/molecular/transport_state_machines/can_addressing_state_machine.json",
    "research/molecular/transport_state_machines/iso_tp_state_machine.json",
    "research/molecular/transport_state_machines/tp20_state_machine.json",
    "research/molecular/transport_state_machines/uds_state_machine.json",
    "research/molecular/transport_state_machines/kwp2000_state_machine.json",
    "research/molecular/VEHICLE_DETECTION_PIPELINE.md", "research/molecular/ecu_identification_rules.json",
    "research/molecular/SETTING_OBJECT_MODEL.json", "research/molecular/DIAGNOSTIC_OPERATIONS_INDEX.json",
    "research/molecular/SERVICE_TOOL_INDEX.json",
    "research/molecular/service_flows/tool_epb_flow.json", "research/molecular/service_flows/tool_dpf_flow.json",
    "research/molecular/service_flows/tool_battery_reg_flow.json",
    "research/molecular/service_flows/tool_service_reset_flow.json",
    "research/molecular/service_flows/tool_tpms_flow.json",
    "research/molecular/LIVE_DATA_INDEX.json", "research/molecular/DATA_FORMATS.md",
    "research/molecular/assets_export/assets_manifest.json", "research/molecular/BACKEND_BOUNDARY.md",
    "research/molecular/LOCAL_STORAGE_MAP.json", "research/molecular/FEATURE_DEPENDENCY_GRAPH.json",
    "research/molecular/FEATURE_DEPENDENCY_GRAPH.md",
    # Round 4 evidence-provenance chain
    "research/molecular/vag_setting_callsites.json", "research/molecular/resolved_factories_map.json",
    "research/molecular/all_binary_variants_ground_truth.json", "research/molecular/SETTING_VARIANTS_INDEX.json",
    "research/molecular/SETTING_INSTANCE_INDEX.json", "research/molecular/SETTING_TO_COMMAND_MAP.json",
    "research/molecular/REPRODUCIBILITY_REPORT.json", "handoff/READY_FEATURES.json", "handoff/BLOCKED_FEATURES.json",
]


def _j(rel):
    with open(os.path.join(BASE_DIR, rel), encoding="utf-8") as fh:
        return json.load(fh)


def test_file_existence():
    print("[*] Test 1: required deliverables exist and are non-empty...")
    bad = [f for f in REQUIRED_FILES
           if not os.path.exists(os.path.join(BASE_DIR, f)) or os.path.getsize(os.path.join(BASE_DIR, f)) == 0]
    assert not bad, f"Missing or empty required files: {bad}"


def test_relationships_hold():
    print("[*] Test 2: provenance, variant, protocol, feature and command-map relationships...")
    L = mi.load_all(BASE_DIR)
    vs = mi.check_all(BASE_DIR, L)
    assert not vs, f"{len(vs)} relationship violation(s):\n  " + "\n  ".join(vs[:30])


def test_no_hardcoded_result_counts_in_validators():
    print("[*] Test 3: validators contain no hard-coded expected result counts...")
    targets = [os.path.join(BASE_DIR, "tests", n) for n in
               ("molecular_validation.py", "test_molecular_model.py", "molecular_reproducibility.py")]
    targets += [os.path.join(BASE_DIR, "tools", n) for n in ("molecular_invariants.py", "molecular_model.py")]
    offenders = []
    for path in targets:
        tree = ast.parse(open(path, encoding="utf-8").read())
        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare):
                continue
            consts = [c.value for c in [node.left] + node.comparators
                      if isinstance(c, ast.Constant) and isinstance(c.value, int) and not isinstance(c.value, bool)]
            others = [c for c in [node.left] + node.comparators if not isinstance(c, ast.Constant)]
            if any(v > 1 for v in consts) and others:
                text = ast.unparse(node)
                if any(w in text for w in ("len(", "count", "total", "EXACT", "PARTIAL", "UNRESOLVED", "REJECTED")):
                    offenders.append(f"{os.path.basename(path)}:{node.lineno}: {text}")
    assert not offenders, "hard-coded count comparisons:\n  " + "\n  ".join(offenders)


def test_not_a_setting_operations_are_decoupled():
    print("[*] Test 4: AutoScan / DTC clear / EPB / DPF / battery / service reset are not settings...")
    L = mi.load_all(BASE_DIR)
    inst = {i["id"]: i for i in L["instances"]["instances"]}
    cmd_features = {c["feature_id"] for c in L["commands"]["commands"]}
    keys_in_variants = set(L["variants"]["variants_by_key"])
    for fid in mm.NOT_A_SETTING:
        assert inst[fid]["resolution_status"] == mm.FS_REJECTED, fid
        assert fid not in cmd_features, f"{fid} leaked into the setting command map"
        assert inst[fid]["setting_key"] not in keys_in_variants, f"{fid} key has coding-setting variants"

    diag = _j("research/molecular/DIAGNOSTIC_OPERATIONS_INDEX.json")["operations"]
    autoscan = [op for op in diag if "AUTOSCAN" in op.get("operation_id", "")]
    assert len(autoscan) >= 1, "AutoScan missing from DIAGNOSTIC_OPERATIONS_INDEX.json"
    cmd = autoscan[0]["protocol_command"]
    assert "04A1" in cmd.get("did", "") or "04A1" in cmd.get("request_hex", "")
    clear = [op for op in diag if "CLEAR" in op.get("operation_id", "")]
    assert clear and "14FFFFFF" in clear[0]["protocol_command"].get("request_hex", "").replace(" ", "")
    tools = _j("research/molecular/SERVICE_TOOL_INDEX.json")["service_tools"]
    epb = next(t for t in tools if t.get("tool_id") == "TOOL_EPB")["routines"]
    assert "310103A1" in epb["open_calipers"]["start_command"] and "310103A0" in epb["close_calipers"]["start_command"]


def test_ecu_addressing_has_no_fallback_and_matches_tables():
    print("[*] Test 5: ECU transport comes from the verified tables, never a generic fallback...")
    assert resolve_ecu_transport("UNKNOWN_NONEXISTENT_ECU") is None
    assert resolve_ecu_transport("") is None and resolve_ecu_transport(None) is None
    for name, exp in (("VagUdsEcu::ENGINE", ("0x7E0", "0x7E8")), ("VagUdsEcu::TRANSMISSION", ("0x7E1", "0x7E9")),
                      ("VagUdsEcu::ABS", ("0x713", "0x77D")), ("VagUdsEcu::INSTRUMENT_CLUSTER", ("0x714", "0x77E"))):
        t = resolve_ecu_transport(name)
        assert (t["uds_tx_id"], t["uds_rx_id"]) == exp, name
    kwp = resolve_ecu_transport("VagCanEcu::ENGINE")
    assert kwp["uds_tx_id"] is None and kwp["uds_rx_id"] is None, "KWP ECU must not borrow UDS CAN IDs"
    for c in _j("research/molecular/SETTING_TO_COMMAND_MAP.json")["commands"]:
        ecu = c["ecu"]
        if c["protocol"] == mm.UDS:
            table = VAG_UDS_ECU_ADDRESSES[ecu["object"]]
            assert (ecu["uds_tx_id"], ecu["uds_rx_id"]) == (table["tx"], table["rx"]), c["variant_id"]
        else:
            assert ecu["uds_tx_id"] is None and ecu["uds_rx_id"] is None, c["variant_id"]


def test_command_map_is_variant_specific():
    print("[*] Test 6: command map is variant-keyed, schema v2, and never a per-feature collapse...")
    doc = _j("research/molecular/SETTING_TO_COMMAND_MAP.json")
    assert doc["metadata"]["schema_version"] == 2
    seen = set()
    for c in doc["commands"]:
        assert c["variant_id"] and (c["feature_id"], c["variant_id"]) not in seen
        seen.add((c["feature_id"], c["variant_id"]))
        assert "read_command_hex" not in c and "write_command_hex" not in c, "v1 flattened command keys present"
        assert c["request_flow"]["steps"], c["variant_id"]
        assert c["post_verify_read"] is True and c["request_flow"]["steps"][-1]["op"] == "read_back_verify"
        assert c["applicability_identity"]["whitelist"], c["variant_id"]


TESTS = [test_file_existence, test_relationships_hold, test_no_hardcoded_result_counts_in_validators,
         test_not_a_setting_operations_are_decoupled, test_ecu_addressing_has_no_fallback_and_matches_tables,
         test_command_map_is_variant_specific]


def main():
    print("=" * 70)
    print("CARISTA MOLECULAR VALIDATION (relationship-based, Round 4)")
    print("=" * 70)
    failed = 0
    for t in TESTS:
        try:
            t()
            print("    PASS")
        except AssertionError as exc:
            failed += 1
            print(f"    FAIL {t.__name__}: {exc}")
    print("=" * 70)
    print("ALL VALIDATION TESTS PASSED" if not failed else f"{failed} VALIDATION TEST(S) FAILED")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
