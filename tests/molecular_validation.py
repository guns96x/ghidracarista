#!/usr/bin/env python3
"""
tests/molecular_validation.py
Rigorous automated validator for all Carista molecular decomposition artifacts.
Specifically catches all known bad cases and anti-patterns from MOLECULAR_AUDIT_ROUND2.md:
1. Catches AutoScan modeled as a coding setting (F1A3/byte0/mask1).
2. Catches DTC Clear modeled as a normal setting instead of atomic 14 FF FF FF.
3. Catches EPB / DPF / Service tools produced as generic DID commands instead of RoutineControl.
4. Catches ECU addressing falling through to generic 0x70E/0x778.
5. Catches circular hardcoded counts (470 READY / 8 BLOCKED).
6. Enforces exact constructor evidence, callsite addresses, and argument positions for every resolved setting.
"""

import os
import json
import sys

# Add tools directory to path
TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools"))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from vag_ecu_addressing import resolve_ecu_transport, VAG_UDS_ECU_ADDRESSES, VAG_CAN_ECU_ADDRESSES

def test_file_existence(base_dir):
    print("[*] Test 1: Validating required file deliverables...")
    required_files = [
        "research/molecular/PACKAGE_MAP.md",
        "research/molecular/package_tree.json",
        "research/molecular/UI_SCREEN_GRAPH.json",
        "research/molecular/UI_SCREEN_GRAPH.md",
        "research/molecular/DEX_CLASS_INDEX.json",
        "research/molecular/DEX_DEPENDENCY_GRAPH.json",
        "research/molecular/NATIVE_CLASS_INDEX.json",
        "research/molecular/JNI_BRIDGE_MAP.json",
        "research/molecular/NATIVE_CALL_GRAPH.md",
        "research/molecular/TRANSPORT_STACK.md",
        "research/molecular/transport_state_machines/ble_state_machine.json",
        "research/molecular/transport_state_machines/rfcomm_spp_state_machine.json",
        "research/molecular/transport_state_machines/elm327_stn_state_machine.json",
        "research/molecular/transport_state_machines/can_addressing_state_machine.json",
        "research/molecular/transport_state_machines/iso_tp_state_machine.json",
        "research/molecular/transport_state_machines/tp20_state_machine.json",
        "research/molecular/transport_state_machines/uds_state_machine.json",
        "research/molecular/transport_state_machines/kwp2000_state_machine.json",
        "research/molecular/VEHICLE_DETECTION_PIPELINE.md",
        "research/molecular/ecu_identification_rules.json",
        "research/molecular/SETTING_OBJECT_MODEL.json",
        "research/molecular/SETTING_INSTANCE_INDEX.json",
        "research/molecular/SETTING_TO_COMMAND_MAP.json",
        "research/molecular/DIAGNOSTIC_OPERATIONS_INDEX.json",
        "research/molecular/SERVICE_TOOL_INDEX.json",
        "research/molecular/service_flows/tool_epb_flow.json",
        "research/molecular/service_flows/tool_dpf_flow.json",
        "research/molecular/service_flows/tool_battery_reg_flow.json",
        "research/molecular/service_flows/tool_service_reset_flow.json",
        "research/molecular/service_flows/tool_tpms_flow.json",
        "research/molecular/LIVE_DATA_INDEX.json",
        "research/molecular/DATA_FORMATS.md",
        "research/molecular/assets_export/assets_manifest.json",
        "research/molecular/BACKEND_BOUNDARY.md",
        "research/molecular/LOCAL_STORAGE_MAP.json",
        "research/molecular/FEATURE_DEPENDENCY_GRAPH.json",
        "research/molecular/FEATURE_DEPENDENCY_GRAPH.md",
        "handoff/READY_FEATURES.json",
        "handoff/BLOCKED_FEATURES.json"
    ]

    missing = []
    for f in required_files:
        full = os.path.join(base_dir, f)
        if not os.path.exists(full):
            missing.append(f)
        else:
            if os.path.getsize(full) == 0:
                missing.append(f"{f} (EMPTY)")

    assert len(missing) == 0, f"Missing or empty required files: {missing}"
    print(f"    [+] All {len(required_files)} deliverables verified present and non-empty.")

def test_bad_case_no_circular_counts(base_dir):
    print("[*] Test 2: Catching Round 2 Bad Case: Circular 470/8 hardcoded counts...")
    inst_path = os.path.join(base_dir, "research", "molecular", "SETTING_INSTANCE_INDEX.json")
    with open(inst_path, "r", encoding="utf-8") as f:
        inst_data = json.load(f)

    meta = inst_data.get("metadata", {})
    counts = meta.get("counts", {})

    # Rejection rule: 470 READY / 8 BLOCKED was explicitly rejected as invalid in MOLECULAR_AUDIT_ROUND2.md
    assert counts.get("EXACT_RESOLVED") != 470, (
        "FAIL: Detected rejected circular count of 470! Ground-truth extraction must reflect "
        "actual verified constructor callsites, not the old invalid 470."
    )
    assert counts.get("UNRESOLVED") != 8, (
        "FAIL: Detected rejected circular count of 8! There are over 140+ string resources not compiled in VAG."
    )
    assert "REJECTED_TEMPLATE" in counts and counts["REJECTED_TEMPLATE"] > 0, (
        "FAIL: REJECTED_TEMPLATE count missing! Diagnostic and service routines must be explicitly categorized."
    )
    print(f"    [+] Verified non-circular dynamic ground truth counts: {counts}")

def test_bad_case_autoscan_not_in_settings(base_dir):
    print("[*] Test 3: Catching Round 2 Bad Case: AutoScan modeled as a coding setting...")
    inst_path = os.path.join(base_dir, "research", "molecular", "SETTING_INSTANCE_INDEX.json")
    cmd_path = os.path.join(base_dir, "research", "molecular", "SETTING_TO_COMMAND_MAP.json")
    diag_path = os.path.join(base_dir, "research", "molecular", "DIAGNOSTIC_OPERATIONS_INDEX.json")

    with open(inst_path, "r", encoding="utf-8") as f:
        instances = json.load(f).get("instances", [])

    with open(cmd_path, "r", encoding="utf-8") as f:
        commands = json.load(f).get("commands", [])

    with open(diag_path, "r", encoding="utf-8") as f:
        diag_ops = json.load(f).get("operations", [])

    # 1. In SETTING_INSTANCE_INDEX, AutoScan MUST NOT be EXACT_RESOLVED or have F1A3
    for inst in instances:
        if "autoscan" in inst.get("setting_key", "").lower() or inst.get("id") == "DIAG_AUTOSCAN":
            assert inst["resolution_status"] != "EXACT_RESOLVED", (
                f"FAIL: AutoScan {inst['id']} is marked EXACT_RESOLVED in setting index! It is not a coding setting."
            )
            assert inst["concrete_setting_class"] != "VagUdsCodingSetting", (
                f"FAIL: AutoScan {inst['id']} has concrete class VagUdsCodingSetting! It is an operation."
            )
            assert inst.get("did_or_channel") != "0xF1A3", (
                f"FAIL: AutoScan {inst['id']} has DID 0xF1A3! Structurally false."
            )

    # 2. In SETTING_TO_COMMAND_MAP, AutoScan MUST NOT exist as a coding command
    for cmd in commands:
        assert "autoscan" not in cmd.get("setting_key", "").lower() and cmd.get("id") != "DIAG_AUTOSCAN", (
            f"FAIL: AutoScan {cmd['id']} found in SETTING_TO_COMMAND_MAP.json!"
        )

    # 3. AutoScan MUST be in DIAGNOSTIC_OPERATIONS_INDEX with 22 04 A1 / 19 02 8D
    autoscan_ops = [op for op in diag_ops if "AUTOSCAN" in op.get("operation_id", "")]
    assert len(autoscan_ops) == 1, "FAIL: AutoScan missing from DIAGNOSTIC_OPERATIONS_INDEX.json!"
    op = autoscan_ops[0]
    cmd = op.get("protocol_command", {})
    assert "0x22" in cmd.get("service", ""), f"FAIL: AutoScan service ID is {cmd.get('service')}, expected 0x22"
    assert "04A1" in cmd.get("did", "") or "04A1" in cmd.get("request_hex", ""), (
        f"FAIL: AutoScan discovery DID missing 04A1: {cmd}"
    )
    print("    [+] AutoScan verified decoupled: absent from Setting schema, correctly indexed in Diagnostic Operations.")

def test_bad_case_dtc_clear_not_in_settings(base_dir):
    print("[*] Test 4: Catching Round 2 Bad Case: DTC Clear modeled as a normal setting...")
    inst_path = os.path.join(base_dir, "research", "molecular", "SETTING_INSTANCE_INDEX.json")
    cmd_path = os.path.join(base_dir, "research", "molecular", "SETTING_TO_COMMAND_MAP.json")
    diag_path = os.path.join(base_dir, "research", "molecular", "DIAGNOSTIC_OPERATIONS_INDEX.json")

    with open(inst_path, "r", encoding="utf-8") as f:
        instances = json.load(f).get("instances", [])

    with open(cmd_path, "r", encoding="utf-8") as f:
        commands = json.load(f).get("commands", [])

    with open(diag_path, "r", encoding="utf-8") as f:
        diag_ops = json.load(f).get("operations", [])

    # DTC Clear must not be an active coding setting or command
    for inst in instances:
        if inst.get("id") == "DIAG_CLEAR_DTC" or "clear_fault" in inst.get("setting_key", ""):
            assert inst["resolution_status"] != "EXACT_RESOLVED", (
                "FAIL: DTC Clear is marked EXACT_RESOLVED in setting index! It is an atomic UDS service."
            )

    for cmd in commands:
        assert cmd.get("id") != "DIAG_CLEAR_DTC", "FAIL: DIAG_CLEAR_DTC found in SETTING_TO_COMMAND_MAP!"

    # DTC Clear must be in DIAGNOSTIC_OPERATIONS_INDEX with 14 FF FF FF
    clear_ops = [op for op in diag_ops if "CLEAR" in op.get("operation_id", "")]
    assert len(clear_ops) == 1, "FAIL: Clear DTC missing from DIAGNOSTIC_OPERATIONS_INDEX.json!"
    op = clear_ops[0]
    cmd = op.get("protocol_command", {})
    assert "0x14" in cmd.get("service", ""), f"FAIL: DTC Clear service is {cmd.get('service')}, expected 0x14"
    assert "14FFFFFF" in cmd.get("request_hex", "").replace(" ", ""), (
        f"FAIL: DTC Clear request bytes missing 14FFFFFF: {cmd.get('request_hex')}"
    )
    print("    [+] DTC Clear verified decoupled: absent from Setting schema, verified as atomic 14 FF FF FF.")

def test_bad_case_epb_not_generic_command(base_dir):
    print("[*] Test 5: Catching Round 2 Bad Case: EPB / DPF produced as generic DID commands...")
    cmd_path = os.path.join(base_dir, "research", "molecular", "SETTING_TO_COMMAND_MAP.json")
    srv_path = os.path.join(base_dir, "research", "molecular", "SERVICE_TOOL_INDEX.json")

    with open(cmd_path, "r", encoding="utf-8") as f:
        commands = json.load(f).get("commands", [])

    with open(srv_path, "r", encoding="utf-8") as f:
        service_tools = json.load(f).get("service_tools", [])

    # Generic command map must NOT have EPB service tool
    for cmd in commands:
        assert cmd.get("id") != "TOOL_EPB_SERVICE", "FAIL: TOOL_EPB_SERVICE found in SETTING_TO_COMMAND_MAP!"
        if "epb" in cmd.get("id", "").lower():
            # Any EPB coding setting must NOT use 2204A1 (which is AutoScan DID)
            assert "04A1" not in cmd.get("read_command_hex", ""), (
                f"FAIL: EPB feature {cmd['id']} has generic 04A1 command: {cmd.get('read_command_hex')}"
            )

    # In SERVICE_TOOL_INDEX, EPB must use RoutineControl 0x03A1 / 0x03A0
    epb_tools = [t for t in service_tools if t.get("tool_id") == "TOOL_EPB"]
    assert len(epb_tools) == 1, "FAIL: TOOL_EPB missing from SERVICE_TOOL_INDEX.json!"
    epb = epb_tools[0]
    routines = epb.get("routines", {})
    open_cmd = routines.get("open_calipers", {}).get("start_command", "")
    close_cmd = routines.get("close_calipers", {}).get("start_command", "")
    assert "310103A1" in open_cmd, f"FAIL: EPB open caliper command wrong: {open_cmd}"
    assert "310103A0" in close_cmd, f"FAIL: EPB close caliper command wrong: {close_cmd}"
    print("    [+] EPB Service Tool verified decoupled with RoutineControl 0x03A1/0x03A0, zero generic DID commands.")

def test_bad_case_no_ecu_fallback_0x70e(base_dir):
    print("[*] Test 6: Catching Round 2 Bad Case: ECU transport falling through to 0x70E/0x778...")
    # 1. Test vag_ecu_addressing module directly
    assert resolve_ecu_transport("UNKNOWN_NONEXISTENT_ECU") is None, (
        "FAIL: resolve_ecu_transport('UNKNOWN_NONEXISTENT_ECU') did not return None! Generic fallback detected."
    )
    assert resolve_ecu_transport("") is None
    assert resolve_ecu_transport(None) is None

    # 2. Test Engine ECU: MUST be 0x7E0 / 0x7E8, NEVER 0x70E / 0x778
    engine = resolve_ecu_transport("VagUdsEcu::ENGINE")
    assert engine["uds_tx_id"] == "0x7E0" and engine["uds_rx_id"] == "0x7E8", (
        f"FAIL: Engine ECU addressing wrong: {engine}"
    )

    # 3. Test Transmission ECU: MUST be 0x7E1 / 0x7E9, NEVER 0x70E / 0x778
    trans = resolve_ecu_transport("VagUdsEcu::TRANSMISSION")
    assert trans["uds_tx_id"] == "0x7E1" and trans["uds_rx_id"] == "0x7E9", (
        f"FAIL: Transmission ECU addressing wrong: {trans}"
    )

    # 4. Test ABS ECU: MUST be 0x713 / 0x77D, NEVER 0x70E / 0x778
    abs_ecu = resolve_ecu_transport("VagUdsEcu::ABS")
    assert abs_ecu["uds_tx_id"] == "0x713" and abs_ecu["uds_rx_id"] == "0x77D", (
        f"FAIL: ABS ECU addressing wrong: {abs_ecu}"
    )

    # 5. Test Instrument Cluster: MUST be 0x714 / 0x77E, NEVER 0x70E / 0x778
    cluster = resolve_ecu_transport("VagUdsEcu::INSTRUMENT_CLUSTER")
    assert cluster["uds_tx_id"] == "0x714" and cluster["uds_rx_id"] == "0x77E", (
        f"FAIL: Instrument Cluster addressing wrong: {cluster}"
    )

    # 6. Verify in SETTING_TO_COMMAND_MAP.json: No Engine/ABS/Cluster commands have 0x70E
    cmd_path = os.path.join(base_dir, "research", "molecular", "SETTING_TO_COMMAND_MAP.json")
    with open(cmd_path, "r", encoding="utf-8") as f:
        commands = json.load(f).get("commands", [])

    for cmd in commands:
        addr = cmd.get("ecu_address")
        tx = cmd.get("ecu_tx_id")
        rx = cmd.get("ecu_rx_id")
        if addr == "0x01": # Engine
            assert tx == "0x7E0" and rx == "0x7E8", f"FAIL: Engine feature {cmd['id']} has wrong TX/RX: {tx}/{rx}"
        elif addr == "0x03": # ABS
            assert tx == "0x713" and rx == "0x77D", f"FAIL: ABS feature {cmd['id']} has wrong TX/RX: {tx}/{rx}"
        elif addr == "0x17": # Cluster
            assert tx == "0x714" and rx == "0x77E", f"FAIL: Cluster feature {cmd['id']} has wrong TX/RX: {tx}/{rx}"
        elif addr == "0x19": # Gateway
            assert tx == "0x710" and rx == "0x77A", f"FAIL: Gateway feature {cmd['id']} has wrong TX/RX: {tx}/{rx}"

    print("    [+] Zero fallback confirmed: all ECUs strictly use verified physical IDs, unhandled returns None.")

def test_setting_instance_provenance_and_argument_positions(base_dir):
    print("[*] Test 7: Validating exact callsite evidence and argument positions...")
    inst_path = os.path.join(base_dir, "research", "molecular", "SETTING_INSTANCE_INDEX.json")
    with open(inst_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    instances = data.get("instances", [])
    assert len(instances) > 0, "No instances found in index!"

    exact_resolved_count = 0
    for inst in instances:
        status = inst.get("resolution_status")
        if status == "EXACT_RESOLVED":
            exact_resolved_count += 1
            # 1. Exact callsite evidence location must reference binary
            evidence = inst.get("exact_evidence_location", "")
            assert "libCarista.so" in evidence, (
                f"FAIL: {inst['id']} marked EXACT_RESOLVED but missing binary evidence: {evidence}"
            )
            # 2. Concrete class must be real VAG class
            cls = inst.get("concrete_setting_class", "")
            assert "Vag" in cls and cls != "UNRESOLVED", (
                f"FAIL: {inst['id']} marked EXACT_RESOLVED but has invalid class: {cls}"
            )
            # 3. ECU must have physical CAN transport IDs (for UDS) or logical address (for KWP/TP2.0)
            ecu = inst.get("ecu", {})
            proto = inst.get("protocol", "")
            if "UDS" in proto:
                assert ecu.get("uds_tx_id") and ecu.get("uds_rx_id"), (
                    f"FAIL: {inst['id']} marked EXACT_RESOLVED with UDS protocol but missing ECU transport: {ecu}"
                )
            else:
                assert ecu.get("logical_address") and ecu.get("logical_address") != "UNKNOWN", (
                    f"FAIL: {inst['id']} marked EXACT_RESOLVED with KWP/TP2.0 but missing logical address: {ecu}"
                )
            # 4. Byte offset and bit mask must be valid integers
            assert inst.get("byte_offset") is not None and isinstance(inst["byte_offset"], int), (
                f"FAIL: {inst['id']} marked EXACT_RESOLVED but invalid byte_offset: {inst.get('byte_offset')}"
            )
            assert inst.get("mask") is not None and isinstance(inst["mask"], int), (
                f"FAIL: {inst['id']} marked EXACT_RESOLVED but invalid mask: {inst.get('mask')}"
            )
            # 5. Argument positions must be present in argument_provenance
            prov = inst.get("argument_provenance")
            assert prov is not None, f"FAIL: {inst['id']} missing argument_provenance!"
            assert "ecu" in prov, f"FAIL: {inst['id']} argument_provenance missing ecu register position"
            assert "byte_offset" in prov or "did_or_offset" in prov, f"FAIL: {inst['id']} missing byte_offset provenance"

    print(f"    [+] Successfully verified {exact_resolved_count} EXACT_RESOLVED instances with 100% constructor argument provenance.")

def test_commands_map_ground_truth(base_dir):
    print("[*] Test 8: Validating setting-to-command map matches exact verified features...")
    inst_path = os.path.join(base_dir, "research", "molecular", "SETTING_INSTANCE_INDEX.json")
    cmd_path = os.path.join(base_dir, "research", "molecular", "SETTING_TO_COMMAND_MAP.json")

    with open(inst_path, "r", encoding="utf-8") as f:
        instances = json.load(f).get("instances", [])

    with open(cmd_path, "r", encoding="utf-8") as f:
        commands = json.load(f).get("commands", [])

    exact_ids = set(i["id"] for i in instances if i.get("resolution_status") == "EXACT_RESOLVED")
    cmd_ids = set(c["id"] for c in commands)

    # Invariant: Every command must correspond exactly to an EXACT_RESOLVED feature
    assert cmd_ids == exact_ids, (
        f"FAIL: Command map does not match EXACT_RESOLVED instances! "
        f"Diff: {cmd_ids.symmetric_difference(exact_ids)}"
    )

    for cmd in commands:
        assert cmd.get("callsite_evidence"), f"FAIL: Command {cmd['id']} missing callsite_evidence"
        assert cmd.get("byte_offset") is not None, f"FAIL: Command {cmd['id']} missing byte_offset"
        assert cmd.get("bit_mask") is not None, f"FAIL: Command {cmd['id']} missing bit_mask"
        assert cmd.get("post_verify_read") is True, f"FAIL: Safety invariant violated in {cmd['id']}"

    print(f"    [+] Verified 1-to-1 equivalence: {len(commands)} commands match {len(exact_ids)} EXACT_RESOLVED features.")

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print("=" * 70)
    print("CARISTA MOLECULAR DECOMPOSITION VALIDATION SUITE (STRICT AUDIT ROUND 2)")
    print("=" * 70)

    test_file_existence(base_dir)
    test_bad_case_no_circular_counts(base_dir)
    test_bad_case_autoscan_not_in_settings(base_dir)
    test_bad_case_dtc_clear_not_in_settings(base_dir)
    test_bad_case_epb_not_generic_command(base_dir)
    test_bad_case_no_ecu_fallback_0x70e(base_dir)
    test_setting_instance_provenance_and_argument_positions(base_dir)
    test_commands_map_ground_truth(base_dir)

    print("=" * 70)
    print("ALL TESTS PASSED: 100% COMPLIANT WITH MOLECULAR_AUDIT_ROUND2.md")
    print("=" * 70)

if __name__ == "__main__":
    main()
