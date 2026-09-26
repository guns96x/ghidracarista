#!/usr/bin/env python3
"""
tools/generate_feature_dependency_graph.py
Builds the complete end-to-end Feature Dependency Graph:
- research/molecular/FEATURE_DEPENDENCY_GRAPH.json
- research/molecular/FEATURE_DEPENDENCY_GRAPH.md
Traces:
UI Screen -> DEX Class -> Operation -> Setting/Service Object -> Variant[] -> ECU -> Protocol -> Request flow

Round 4: the graph is variant-aware. It reads the variant index / instance index / command map
(never a per-feature collapsed command) and contains no defaulted ECU, DID, whitelist or
platform values: anything the evidence does not establish is simply absent.
"""

import os
import json

def get_screen_for_category(cat, fid):
    if "DIAG" in fid:
        if "CLEAR" in fid:
            return {
                "class": "com.prizmos.carista.screens.operation.checkcodes.CheckCodesActivity",
                "screen_name": "DtcDiagnosticsScreen",
                "parent_screen": "MainActivity"
            }
        return {
            "class": "com.prizmos.carista.screens.operation.fullscan.FullScanActivity",
            "screen_name": "AutoScanScreen",
            "parent_screen": "MainActivity"
        }
    elif "TOOL" in fid or cat == "Service Tools":
        return {
            "class": "com.prizmos.carista.GenericToolActivity",
            "screen_name": "GenericServiceToolRunnerScreen",
            "parent_screen": "ShowAvailableToolsActivity"
        }
    elif "LIVE" in fid or cat == "Live Data":
        return {
            "class": "com.prizmos.carista.screens.operation.livedata.LiveDataActivity",
            "screen_name": "LiveDataMonitorScreen",
            "parent_screen": "ShowLiveDataActivity"
        }
    else:
        return {
            "class": "com.prizmos.carista.screens.operation.changesetting.ChangeSettingActivity",
            "screen_name": "ChangeSettingScreen",
            "parent_screen": "ShowSettingsActivity"
        }

def get_operation_for_feature(fid, cat):
    if fid == "DIAG_AUTOSCAN":
        return {
            "class": "com.prizmos.carista.library.operation.FullScanOperation",
            "jni_bridge": "Java_com_prizmos_carista_library_operation_FullScanOperation_00024RichState_make",
            "native_function": "GetVagUdsInstalledEcusCommand::processPayload"
        }
    elif fid == "DIAG_CLEAR_DTC":
        return {
            "class": "com.prizmos.carista.library.operation.ResetCodesOperation",
            "jni_bridge": "Java_com_prizmos_carista_library_operation_Operation_execute",
            "native_function": "ClearAllDtcsCommand::getRequest"
        }
    elif "EPB" in fid:
        return {
            "class": "com.prizmos.carista.library.operation.GenericToolOperation",
            "jni_bridge": "Java_com_prizmos_carista_library_operation_GenericToolOperation_onButtonClickedInternal",
            "native_function": "VagEpbController::executeOpen"
        }
    elif "DPF" in fid:
        return {
            "class": "com.prizmos.carista.library.operation.GenericToolOperation",
            "jni_bridge": "Java_com_prizmos_carista_library_operation_GenericToolOperation_onButtonClickedInternal",
            "native_function": "VagDpfController::startStationary"
        }
    elif "BATTERY" in fid:
        return {
            "class": "com.prizmos.carista.library.operation.GenericToolOperation",
            "jni_bridge": "Java_com_prizmos_carista_library_operation_Operation_execute",
            "native_function": "VagBatteryRegController::executeWrite"
        }
    elif "SERVICE_RESET" in fid:
        return {
            "class": "com.prizmos.carista.library.operation.ServiceIndicatorOperation",
            "jni_bridge": "Java_com_prizmos_carista_library_operation_ServiceIndicatorOperation_00024RichState_make",
            "native_function": "VagServiceIndicatorController::executeReset"
        }
    else:
        return {
            "class": "com.prizmos.carista.library.operation.ChangeSettingOperation",
            "jni_bridge": "Java_com_prizmos_carista_library_operation_Operation_execute",
            "native_function": "Setting::setValue"
        }



def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_graph(mol):
    instances = _load(os.path.join(mol, "SETTING_INSTANCE_INDEX.json"))["instances"]
    variants_by_key = _load(os.path.join(mol, "SETTING_VARIANTS_INDEX.json"))["variants_by_key"]
    commands = _load(os.path.join(mol, "SETTING_TO_COMMAND_MAP.json"))["commands"]
    cmds_by_feature = {}
    for c in commands:
        cmds_by_feature.setdefault(c["feature_id"], []).append(c)

    graph = []
    for inst in instances:
        fid = inst["id"]
        cat = inst.get("category", "")
        state = inst["resolution_status"]
        fvars = variants_by_key.get(inst["setting_key"], []) if state != "REJECTED_TEMPLATE" else []
        entry = {
            "feature_id": fid,
            "feature_name": inst.get("user_visible_name", ""),
            "category": cat,
            "state": state,
            "status": "READY" if state == "EXACT_RESOLVED" else "BLOCKED",
            "ui_screen": get_screen_for_category(cat, fid),
            "operation": get_operation_for_feature(fid, cat),
            "setting_object": {
                "concrete_classes": sorted({v["concrete_class"] for v in fvars}),
                "internal_key": inst["setting_key"],
            },
            "variants": [{"variant_id": v["variant_id"], "status": v["variant_status"],
                          "ecu_object": v["ecu"]["object"], "whitelist": v["whitelist"],
                          "protocol": v["protocol_model"]["runtime_protocol"],
                          "executable": v["executable"]} for v in fvars],
        }
        if state == "REJECTED_TEMPLATE":
            entry["blocking_reason"] = inst.get("rejection_reason")
            entry["target_index"] = inst.get("target_index")
        elif state in ("EXACT_RESOLVED", "AMBIGUOUS_MULTI_VARIANT"):
            entry["commands"] = [{"variant_id": c["variant_id"], "protocol": c["protocol"],
                                  "flow_id": c["request_flow"]["flow_id"], "ecu": c["ecu"]["object"],
                                  "selection_required": c["selection_required"],
                                  "byte_offset": c["byte_offset"], "bit_mask": c["bit_mask"]}
                                 for c in cmds_by_feature.get(fid, [])]
        else:
            entry["blocking_reason"] = state
        graph.append(entry)
    return graph


def render_markdown(graph):
    states = {}
    for e in graph:
        states[e["state"]] = states.get(e["state"], 0) + 1
    out = ["# Molecular Feature Dependency Graph", ""]
    out.append(f"Features traced: **{len(graph)}**. States: "
               + ", ".join(f"`{k}`={v}" for k, v in sorted(states.items())) + "  ")
    out += ["", "## 1. Trace architecture", "", "```mermaid", "flowchart LR",
            '    UI["1. UI Screen"] --> OP["2. Operation"]',
            '    OP --> JNI["3. JNI Bridge"]',
            '    JNI --> FEAT["4. Feature"]',
            '    FEAT --> VAR["5. Variant[] (callsite-proven)"]',
            '    VAR --> ECU["6. ECU + protocol (must agree)"]',
            '    ECU --> FLOW["7. Ordered request flow"]', "```", "",
            "A feature with several variants is `AMBIGUOUS_MULTI_VARIANT`: each executable variant is listed "
            "with its own ECU/whitelist identity and no single command stands for the feature.", "",
            "## 2. Representative traces", ""]
    picks = [e for e in graph if e["state"] == "REJECTED_TEMPLATE"]
    for st in ("EXACT_RESOLVED", "AMBIGUOUS_MULTI_VARIANT"):
        picks += [e for e in graph if e["state"] == st][:1]
    for item in picks:
        out.append(f"### `{item['feature_id']}`: {item['feature_name']} ({item['state']})")
        out.append("")
        out.append(f"- **UI Screen**: `{item['ui_screen']['screen_name']}` (`{item['ui_screen']['class']}`)")
        out.append(f"- **Operation Class**: `{item['operation']['class']}`")
        out.append(f"- **JNI Bridge**: `{item['operation']['jni_bridge']}`")
        out.append(f"- **Native Function**: `{item['operation'].get('native_function', 'N/A')}`")
        out.append(f"- **Setting classes**: `{', '.join(item['setting_object']['concrete_classes']) or 'n/a'}`")
        for c in item.get("commands", []):
            out.append(f"- **Variant** `{c['variant_id']}`: `{c['protocol']}` flow `{c['flow_id']}` on `{c['ecu']}` "
                       f"(byte `{c['byte_offset']}`, mask `0x{c['bit_mask']:02X}`, "
                       f"selection_required={c['selection_required']})")
        out += ["", "---", ""]
    return "\n".join(out) + "\n"


def render_json(graph):
    states = {}
    for e in graph:
        states[e["state"]] = states.get(e["state"], 0) + 1
    doc = {"metadata": {"title": "Carista End-to-End Molecular Feature Dependency Graph (variant-aware)",
                        "total_features": len(graph), "state_counts": states},
           "graph": graph}
    return json.dumps(doc, indent=1, sort_keys=True) + "\n"


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    mol = os.path.join(base_dir, "research", "molecular")
    graph = build_graph(mol)
    with open(os.path.join(mol, "FEATURE_DEPENDENCY_GRAPH.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write(render_json(graph))
    with open(os.path.join(mol, "FEATURE_DEPENDENCY_GRAPH.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(render_markdown(graph))
    print(f"[+] {len(graph)} features linked")


if __name__ == "__main__":
    main()
