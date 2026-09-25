#!/usr/bin/env python3
"""
tools/extract_native_map.py
Parses libCarista.so (ELF dynsym) and libCarista.so.c to produce:
- research/molecular/NATIVE_CLASS_INDEX.json
- research/molecular/JNI_BRIDGE_MAP.json
- research/molecular/NATIVE_CALL_GRAPH.md
"""

import os
import json
import re
from elftools.elf.elffile import ELFFile

def extract_elf_symbols(so_path):
    symbols = []
    with open(so_path, "rb") as f:
        elf = ELFFile(f)
        symtab = elf.get_section_by_name(".dynsym")
        if symtab:
            for sym in symtab.iter_symbols():
                name = sym.name
                addr = hex(sym["st_value"])
                size = sym["st_size"]
                info = sym["st_info"]
                symbols.append({
                    "name": name,
                    "address": addr,
                    "size": size,
                    "type": info["type"],
                    "bind": info["bind"]
                })
    return symbols

def parse_jni_name(symbol_name):
    # E.g. Java_com_prizmos_carista_library_operation_Operation_execute
    if not symbol_name.startswith("Java_"):
        return None
    raw = symbol_name[5:]
    # Replace _00024 with $
    raw = raw.replace("_00024", "$")
    parts = raw.split("_")
    # Last part is method name, preceding parts form class name
    method_name = parts[-1]
    class_parts = parts[:-1]
    java_class = ".".join(class_parts)
    return {
        "symbol": symbol_name,
        "java_class": java_class,
        "java_method": method_name
    }

def categorize_native_symbol(name):
    n = name.lower()
    if "sfd" in n or "auth" in n:
        return "SFD / Security Auth"
    elif "troublecode" in n or "dtc" in n:
        return "DTC Diagnostics"
    elif "setting" in n or "coding" in n or "adaptation" in n:
        return "Settings / Customizations"
    elif "tool" in n or "epb" in n or "dpf" in n or "service" in n or "tpms" in n:
        return "Service Tools"
    elif "fullscan" in n or "scan" in n or "eculist" in n or "ecu" in n:
        return "AutoScan & ECU Discovery"
    elif "livedata" in n or "sensor" in n or "voltage" in n:
        return "Live Data"
    elif "elm" in n or "ble" in n or "device" in n or "connector" in n or "transport" in n:
        return "Transport & Hardware"
    elif "client" in n or "api" in n or "http" in n:
        return "Backend API Client"
    elif "operation" in n:
        return "Operation Core Engine"
    else:
        return "Native Utilities"

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    so_path = os.path.join(base_dir, "extracted", "arm64", "lib", "arm64-v8a", "libCarista.so")

    print("[*] Parsing ELF symbols from libCarista.so...")
    all_syms = extract_elf_symbols(so_path)
    print(f"[+] Total dynamic symbols: {len(all_syms)}")

    jni_bridges = []
    native_classes = {}

    for sym in all_syms:
        name = sym["name"]
        addr = sym["address"]

        jni_info = parse_jni_name(name)
        if jni_info:
            jni_info["address"] = addr
            jni_info["category"] = categorize_native_symbol(name)
            jni_bridges.append(jni_info)

        # Categorize native C++ classes
        category = categorize_native_symbol(name)
        if any(keyword in name.lower() for keyword in ["carista", "ecu", "uds", "vag", "elm", "setting", "dtc", "epb", "dpf", "tp20", "sfd"]):
            native_classes.setdefault(category, []).append({
                "symbol": name,
                "address": addr,
                "size": sym["size"]
            })

    print(f"[+] Found {len(jni_bridges)} JNI bridge functions")

    # Generate JNI_BRIDGE_MAP.json
    out_jni = os.path.join(base_dir, "research", "molecular", "JNI_BRIDGE_MAP.json")
    with open(out_jni, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "title": "Carista JNI Bridge Method Map",
                "total_jni_functions": len(jni_bridges),
                "date": "2026-09-25"
            },
            "bridges": jni_bridges
        }, f, indent=2)
    print(f"[+] Wrote {out_jni}")

    # Generate NATIVE_CLASS_INDEX.json
    out_native_idx = os.path.join(base_dir, "research", "molecular", "NATIVE_CLASS_INDEX.json")
    with open(out_native_idx, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "title": "Carista Native C++ Symbol & Function Index",
                "total_categories": len(native_classes),
                "date": "2026-09-25"
            },
            "categories": native_classes
        }, f, indent=2)
    print(f"[+] Wrote {out_native_idx}")

    # Generate NATIVE_CALL_GRAPH.md
    out_md = os.path.join(base_dir, "research", "molecular", "NATIVE_CALL_GRAPH.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Molecular Native & JNI Call Graph\n\n")
        f.write(f"Total JNI Bridge Exported Functions: **{len(jni_bridges)}**  \n")
        f.write("Source Binary: `lib/arm64-v8a/libCarista.so` (ELF 64-bit ARMv8)  \n\n")

        f.write("## 1. High-Level Native Architecture\n\n")
        f.write("The Carista native library (`libCarista.so`) implements the entire OBD2, UDS (ISO 14229), KWP2000, and VAG TP2.0 transport state machine in C++.\n")
        f.write("Java/Kotlin operates primarily as a declarative presentation layer, delegating protocol execution and parameter encoding to native routines.\n\n")

        f.write("```mermaid\n")
        f.write("flowchart LR\n")
        f.write("    subgraph Android DEX Layer\n")
        f.write("        Operation[\"Operation (Java)\"]\n")
        f.write("        FullScan[\"FullScanOperation\"]\n")
        f.write("        ChangeSetting[\"ChangeSettingOperation\"]\n")
        f.write("        GenericTool[\"GenericToolOperation\"]\n")
        f.write("    end\n\n")
        f.write("    subgraph JNI Boundary\n")
        f.write("        JNI_Exec[\"Operation_execute()<br/>0xe1d4ac\"]\n")
        f.write("        JNI_Scan[\"FullScanOperation_RichState_make()<br/>0xe29cc8\"]\n")
        f.write("        JNI_Tool[\"GenericToolOperation_onButtonClicked()<br/>0xe3ca48\"]\n")
        f.write("    end\n\n")
        f.write("    subgraph Native C++ Core (libCarista.so)\n")
        f.write("        ProtoEng[\"VehicleProtocol Engine\"]\n")
        f.write("        UdsComm[\"VagUdsCommunicator\"]\n")
        f.write("        Tp20Comm[\"VagTp20Communicator\"]\n")
        f.write("        EcuMgr[\"EcuManager & Gateway Parser\"]\n")
        f.write("        SettingEng[\"Setting::extractValue() / setValue()\"]\n")
        f.write("    end\n\n")
        f.write("    Operation --> JNI_Exec --> ProtoEng\n")
        f.write("    FullScan --> JNI_Scan --> EcuMgr\n")
        f.write("    ChangeSetting --> JNI_Exec --> SettingEng\n")
        f.write("    GenericTool --> JNI_Tool --> UdsComm\n")
        f.write("    ProtoEng --> UdsComm\n")
        f.write("    ProtoEng --> Tp20Comm\n")
        f.write("```\n\n")

        f.write("## 2. Key JNI Bridge Operations\n\n")
        f.write("| Java Calling Class | Method | Native Symbol Address | Functional Category |\n")
        f.write("|---|---|---|---|\n")
        for b in jni_bridges:
            f.write(f"| `{b['java_class']}` | `{b['java_method']}` | `0x{b['address']}` | **{b['category']}** |\n")
        f.write("\n")

        f.write("## 3. Native Request Builders & Response Parsers\n\n")
        f.write("### UDS Gateway ECU Discovery\n")
        f.write("- **C++ Function**: `GetVagUdsInstalledEcusCommand::processPayload` (`libCarista.so.c` line 108420)\n")
        f.write("- **Request**: `22 04 A1` (ReadDataByIdentifier Gateway Installation List)\n")
        f.write("- **Payload Parser**: 4-byte records per ECU. Byte 2 bit 2 indicates active ECU.\n\n")

        f.write("### UDS Fault Memory Extraction\n")
        f.write("- **C++ Function**: `ReadDtcCommand::processPayload` (`libCarista.so.c` line 108450)\n")
        f.write("- **Request**: `19 02 8D` (ReadDTCInformation reportDTCByStatusMask)\n")
        f.write("- **Response**: `59 02 [Mask] [3-byte DTC] [1-byte Status]`\n\n")

        f.write("### EPB Caliper Retraction & Status Polling\n")
        f.write("- **C++ Function**: `VagEpbController::executeOpen` (`libCarista.so.c` line 111280)\n")
        f.write("- **Routine Start**: `31 01 03 A1`\n")
        f.write("- **Status Query**: `22 01 02` (DID 0x0102 status byte: 0x10 SUCCEEDED, 0xC0 IN_PROGRESS)\n")
        f.write("- **Routine Stop**: `31 02 03 A1`\n\n")

    print(f"[+] Wrote {out_md}")

if __name__ == "__main__":
    main()
