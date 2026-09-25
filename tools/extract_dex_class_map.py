#!/usr/bin/env python3
"""
tools/extract_dex_class_map.py
Parses classes.dex and classes2.dex to produce:
- research/molecular/DEX_CLASS_INDEX.json
- research/molecular/DEX_DEPENDENCY_GRAPH.json
"""

import os
import json
from loguru import logger
logger.disable("androguard")
from androguard.core.dex import DEX

def categorize_class(pkg, name):
    full = f"{pkg}.{name}".lower()
    if "connection" in full or "connector" in full or "bluetooth" in full or "elm" in full or "device" in full or "scanner" in full or "communication" in full:
        return "transport"
    elif "protocol" in full or "isotp" in full or "uds" in full or "kwp" in full or "tp20" in full:
        return "protocol"
    elif "vehid" in full or "vehicle" in full or "confirmvehicle" in full or "selectvehicle" in full:
        return "vehicle detection"
    elif "discovery" in full or "geteculist" in full or "fullscan" in full or "showecu" in full:
        return "ECU discovery"
    elif "checkcodes" in full or "dtc" in full or "fault" in full or "freezeframe" in full or "troublecode" in full:
        return "DTC"
    elif "livedata" in full or "sensor" in full or "voltage" in full:
        return "live data"
    elif "setting" in full or "customiz" in full or "multiplechoice" in full or "numerical" in full or "textinterpretation" in full:
        return "settings/customizations"
    elif "coding" in full or "rawvalue" in full or "bitwise" in full:
        return "coding"
    elif "adaptation" in full or "channel" in full:
        return "adaptation"
    elif "basicsetting" in full or "calibrate" in full:
        return "basic settings"
    elif "serviceindicator" in full or "generictool" in full or "tpms" in full or "epb" in full or "dpf" in full or "batteryhealth" in full or "emission" in full:
        return "service tools"
    elif "screen" in full or "activity" in full or "dialog" in full or "fragment" in full or "ui" in full:
        return "UI"
    elif "networking" in full or "network" in full or "http" in full or "account" in full or "auth" in full or "login" in full or "register" in full:
        return "account/network"
    elif "persistence" in full or "realm" in full or "room" in full or "storage" in full or "history" in full or "garage" in full or "restore" in full:
        return "storage/cache"
    elif "analytics" in full or "mixpanel" in full or "onesignal" in full or "firebase" in full or "crashlytics" in full or "log" in full or "telemetry" in full:
        return "telemetry/logging"
    else:
        return "UI"

def clean_type(t):
    if not t:
        return ""
    if t.startswith("L") and t.endswith(";"):
        return t[1:-1].replace("/", ".")
    return t

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dex_files = [
        os.path.join(base_dir, "extracted", "base", "classes.dex"),
        os.path.join(base_dir, "extracted", "base", "classes2.dex")
    ]

    all_classes = []
    edges = []

    print("[*] Processing DEX files...")
    for dex_path in dex_files:
        print(f"[*] Reading {os.path.basename(dex_path)}...")
        with open(dex_path, "rb") as fp:
            d = DEX(fp.read())

        for c in d.get_classes():
            raw_name = c.get_name()
            cls_name_clean = clean_type(raw_name)

            if not ("com.prizmos" in cls_name_clean or "prizmos" in raw_name.lower()):
                continue

            parts = cls_name_clean.split(".")
            pkg = ".".join(parts[:-1]) if len(parts) > 1 else ""
            simple_name = parts[-1]

            superclass = clean_type(c.get_superclassname())
            interfaces = [clean_type(i) for i in c.get_interfaces()]

            methods = []
            jni_calls = []
            deps = set()

            for m in c.get_methods():
                m_name = m.get_name()
                m_desc = m.get_descriptor()
                access = m.get_access_flags()
                is_native = bool(access & 0x0100)
                if is_native:
                    jni_calls.append(f"{cls_name_clean}.{m_name}")

                methods.append({
                    "name": m_name,
                    "descriptor": m_desc,
                    "is_native": is_native
                })

                # Scan instructions for references
                if m.get_code():
                    for inst in m.get_instructions():
                        s = str(inst.get_output())
                        if "Lcom/prizmos/" in s:
                            for word in s.split():
                                if word.startswith("Lcom/prizmos/") and ";" in word:
                                    target = clean_type(word.split(";")[0] + ";")
                                    if target != cls_name_clean:
                                        deps.add(target)

            fields = []
            for f in c.get_fields():
                fields.append({
                    "name": f.get_name(),
                    "type": clean_type(f.get_descriptor())
                })

            category = categorize_class(pkg, simple_name)

            class_entry = {
                "class_name": cls_name_clean,
                "package": pkg,
                "simple_name": simple_name,
                "superclass": superclass,
                "interfaces": interfaces,
                "category": category,
                "confidence": "VERIFIED",
                "methods_count": len(methods),
                "fields_count": len(fields),
                "is_jni_bridge": len(jni_calls) > 0,
                "jni_methods": jni_calls,
                "methods": methods[:30], # Top 30 methods
                "fields": fields[:30],   # Top 30 fields
                "dependencies": sorted(list(deps))
            }
            all_classes.append(class_entry)

            for dep in deps:
                edges.append({
                    "source": cls_name_clean,
                    "target": dep,
                    "type": "references"
                })

    print(f"[+] Total relevant classes indexed: {len(all_classes)}")
    print(f"[+] Total dependency edges: {len(edges)}")

    # Category breakdown
    cat_counts = {}
    for c in all_classes:
        cat_counts[c["category"]] = cat_counts.get(c["category"], 0) + 1

    dex_index = {
        "metadata": {
            "title": "Carista Molecular DEX Class Index",
            "date": "2026-09-25",
            "total_classes": len(all_classes),
            "category_summary": cat_counts
        },
        "classes": all_classes
    }

    dep_graph = {
        "metadata": {
            "title": "Carista DEX Class Dependency Graph",
            "total_nodes": len(all_classes),
            "total_edges": len(edges)
        },
        "nodes": [{"id": c["class_name"], "category": c["category"]} for c in all_classes],
        "edges": edges
    }

    out_index = os.path.join(base_dir, "research", "molecular", "DEX_CLASS_INDEX.json")
    with open(out_index, "w", encoding="utf-8") as f:
        json.dump(dex_index, f, indent=2)
    print(f"[+] Wrote {out_index}")

    out_graph = os.path.join(base_dir, "research", "molecular", "DEX_DEPENDENCY_GRAPH.json")
    with open(out_graph, "w", encoding="utf-8") as f:
        json.dump(dep_graph, f, indent=2)
    print(f"[+] Wrote {out_graph}")

if __name__ == "__main__":
    main()
