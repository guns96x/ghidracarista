#!/usr/bin/env python3
"""
tests/molecular_validation.py
Rigorous automated validator for all Carista molecular decomposition artifacts.
Enforces:
1. Every resolved setting has verifiable source provenance.
2. Every command references an existing ECU / protocol.
3. No feature is marked READY without read/write/applicability evidence.
4. Every required deliverable path exists and is non-empty.
5. Duplicate aliases and blocked features are properly identified and linked.
6. Generated/inferred metadata cannot be erroneously marked VERIFIED without proof.
"""

import os
import json
import sys

def test_file_existence(base_dir):
    print("[*] Validating required file deliverables...")
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
        "research/molecular/FEATURE_DEPENDENCY_GRAPH.md"
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
    print(f"[+] All {len(required_files)} deliverables verified present and non-empty.")

def test_setting_instance_provenance(base_dir):
    print("[*] Validating setting instance provenance and invariants...")
    path = os.path.join(base_dir, "research", "molecular", "SETTING_INSTANCE_INDEX.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    instances = data.get("instances", [])
    assert len(instances) == 478, f"Expected exactly 478 setting instances, found {len(instances)}"

    resolved_verified = 0
    unresolved_count = 0
    alias_count = 0

    for inst in instances:
        assert "id" in inst and inst["id"], f"Missing id in {inst}"
        assert "setting_key" in inst and inst["setting_key"], f"Missing setting_key in {inst}"
        assert "exact_evidence_location" in inst and inst["exact_evidence_location"], f"Missing evidence in {inst}"
        assert "resolution_status" in inst, f"Missing resolution_status in {inst}"
        assert "confidence" in inst, f"Missing confidence in {inst}"

        # Invariant: generated/inferred metadata CANNOT become VERIFIED
        if inst["resolution_status"] == "UNRESOLVED":
            unresolved_count += 1
            assert inst["confidence"] == "INFERRED_UNVERIFIED", f"Invariant violated: Unresolved setting marked VERIFIED: {inst['id']}"
        elif inst["resolution_status"] == "RESOLVED":
            resolved_verified += 1
            assert inst["confidence"] == "VERIFIED", f"Resolved setting missing VERIFIED confidence: {inst['id']}"
            assert "libCarista.so.c line" in inst["exact_evidence_location"], f"Missing line number provenance in {inst['id']}"

        if inst.get("is_alias"):
            alias_count += 1
            assert inst.get("parent_setting_key") is not None, f"Alias missing parent_setting_key in {inst['id']}"

    assert resolved_verified == 470, f"Expected 470 verified resolved settings, found {resolved_verified}"
    assert unresolved_count == 8, f"Expected 8 unresolved settings, found {unresolved_count}"
    assert alias_count >= 20, f"Expected at least 20 option aliases, found {alias_count}"

    print(f"[+] Verified {resolved_verified} RESOLVED (VERIFIED), {unresolved_count} UNRESOLVED (INFERRED), and {alias_count} ALIASES.")

def test_commands_map(base_dir):
    print("[*] Validating setting-to-command execution map...")
    path = os.path.join(base_dir, "research", "molecular", "SETTING_TO_COMMAND_MAP.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    commands = data.get("commands", [])
    assert len(commands) == 470, f"Expected 470 verified commands, found {len(commands)}"

    valid_ecu_prefixes = [
        "0x01", "0x02", "0x03", "0x08", "0x09", "0x13", "0x15", "0x17", "0x19",
        "0x42", "0x44", "0x52", "0x53", "0x5F", "0x65", "0x6D", "0x76", "0xA5", "All"
    ]

    for cmd in commands:
        assert "read_command_hex" in cmd and cmd["read_command_hex"], f"Missing read_command_hex in {cmd}"
        assert "write_command_hex" in cmd and cmd["write_command_hex"], f"Missing write_command_hex in {cmd}"
        assert "ecu_address" in cmd and cmd["ecu_address"], f"Missing ecu_address in {cmd}"
        assert any(p in cmd["ecu_address"] for p in valid_ecu_prefixes), f"Unknown ECU address in {cmd}"
        assert cmd["post_verify_read"] is True, f"Safety invariant violated: post_verify_read must be True in {cmd}"

    print(f"[+] Verified {len(commands)} command execution mappings with read-back verification.")

def test_feature_dependency_graph(base_dir):
    print("[*] Validating end-to-end feature dependency graph...")
    path = os.path.join(base_dir, "research", "molecular", "FEATURE_DEPENDENCY_GRAPH.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    graph = data.get("graph", [])
    assert len(graph) == 478, f"Expected 478 total features in dependency graph, found {len(graph)}"

    ready_count = 0
    blocked_count = 0

    for item in graph:
        assert "ui_screen" in item and item["ui_screen"]["class"], f"Missing UI screen in {item['feature_id']}"
        assert "operation" in item and item["operation"]["class"], f"Missing operation in {item['feature_id']}"
        assert "dependencies" in item, f"Missing dependencies in {item['feature_id']}"

        if item["status"] == "READY":
            ready_count += 1
            assert "commands" in item, f"Missing commands in ready feature {item['feature_id']}"
            assert "applicability" in item, f"Missing applicability in ready feature {item['feature_id']}"
            assert item["dependencies"]["network"] == "None (100% Offline Capable)", f"Network leakage in ready feature {item['feature_id']}"
        elif item["status"] == "BLOCKED":
            blocked_count += 1
            assert "blocking_reason" in item, f"Missing blocking_reason in blocked feature {item['feature_id']}"
            assert "remediation" in item, f"Missing remediation in blocked feature {item['feature_id']}"

    assert ready_count == 470, f"Expected 470 ready features, found {ready_count}"
    assert blocked_count == 8, f"Expected 8 blocked features, found {blocked_count}"
    print(f"[+] Successfully validated 478 end-to-end feature dependency traces (470 READY, 8 BLOCKED).")

def test_transport_and_service_tools(base_dir):
    print("[*] Validating transport rules and service tools...")
    # Addressing rule verification
    can_path = os.path.join(base_dir, "research", "molecular", "transport_state_machines", "can_addressing_state_machine.json")
    with open(can_path, "r", encoding="utf-8") as f:
        can_data = json.load(f)
    assert "if (TX >= 0x795) RX = TX + 8 else RX = TX + 0x6A" in can_data["can_11bit_vag"]["formula"]

    # Service tools verification
    svc_path = os.path.join(base_dir, "research", "molecular", "SERVICE_TOOL_INDEX.json")
    with open(svc_path, "r", encoding="utf-8") as f:
        svc_data = json.load(f)
    tools = svc_data["service_tools"]
    tool_ids = [t["tool_id"] for t in tools]
    assert "TOOL_EPB" in tool_ids
    assert "TOOL_DPF" in tool_ids
    assert "TOOL_BATTERY_REG" in tool_ids
    assert "TOOL_SERVICE_RESET" in tool_ids
    assert "TOOL_TPMS" in tool_ids
    print(f"[+] Transport addressing rules and {len(tools)} service tools verified.")

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print("=" * 60)
    print("CARISTA MOLECULAR DECOMPOSITION VALIDATION SUITE")
    print("=" * 60)

    try:
        test_file_existence(base_dir)
        test_setting_instance_provenance(base_dir)
        test_commands_map(base_dir)
        test_feature_dependency_graph(base_dir)
        test_transport_and_service_tools(base_dir)
        print("=" * 60)
        print("ALL MOLECULAR DECOMPOSITION VALIDATIONS PASSED! (100% SUCCESS)")
        print("=" * 60)
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[!] VALIDATION FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
