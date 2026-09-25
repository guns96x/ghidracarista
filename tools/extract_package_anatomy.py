#!/usr/bin/env python3
"""
tools/extract_package_anatomy.py
Extracts full package anatomy, manifest components, split APK responsibilities,
assets, libraries, permissions, and maps them to feature areas.
"""

import os
import json
from loguru import logger
logger.disable("androguard")
from androguard.core.apk import APK

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

def get_attr(element, name, default=""):
    return element.attrib.get(ANDROID_NS + name, element.attrib.get(name, default))

def extract_manifest_details(apk_path):
    apk = APK(apk_path)
    root = apk.get_android_manifest_xml()

    package_name = root.attrib.get("package", "com.prizmos.carista")
    version_name = get_attr(root, "versionName", "")
    version_code = get_attr(root, "versionCode", "")

    uses_sdk = root.find("uses-sdk")
    min_sdk = get_attr(uses_sdk, "minSdkVersion", "21") if uses_sdk is not None else "21"
    target_sdk = get_attr(uses_sdk, "targetSdkVersion", "34") if uses_sdk is not None else "34"

    # Permissions
    permissions = []
    for elem in root.findall(".//uses-permission"):
        p_name = get_attr(elem, "name")
        if p_name:
            permissions.append({
                "name": p_name,
                "protection_level": "signature" if "signature" in p_name.lower() else "normal"
            })

    def parse_component(elem):
        c_name = get_attr(elem, "name")
        exported = get_attr(elem, "exported", "false")
        filters = []
        deep_links = []
        for ifilter in elem.findall("intent-filter"):
            actions = [get_attr(a, "name") for a in ifilter.findall("action")]
            categories = [get_attr(c, "name") for c in ifilter.findall("category")]
            data_tags = ifilter.findall("data")
            f_obj = {"actions": actions, "categories": categories}
            if data_tags:
                f_obj["data"] = []
                for d in data_tags:
                    scheme = get_attr(d, "scheme")
                    host = get_attr(d, "host")
                    path = get_attr(d, "path") or get_attr(d, "pathPrefix") or get_attr(d, "pathPattern")
                    f_obj["data"].append({"scheme": scheme, "host": host, "path": path})
                    if scheme:
                        dl = f"{scheme}://"
                        if host:
                            dl += host
                        if path:
                            dl += path
                        deep_links.append(dl)
            filters.append(f_obj)
        return {
            "name": c_name,
            "exported": exported,
            "intent_filters": filters,
            "deep_links": deep_links
        }

    activities = [parse_component(e) for e in root.findall(".//activity")]
    services = [parse_component(e) for e in root.findall(".//service")]
    receivers = [parse_component(e) for e in root.findall(".//receiver")]
    providers = []
    for e in root.findall(".//provider"):
        p_data = parse_component(e)
        p_data["authorities"] = get_attr(e, "authorities", "")
        providers.append(p_data)

    return {
        "package_name": package_name,
        "version_name": version_name,
        "version_code": version_code,
        "min_sdk": min_sdk,
        "target_sdk": target_sdk,
        "permissions": permissions,
        "activities": activities,
        "services": services,
        "receivers": receivers,
        "providers": providers
    }

def inspect_assets(base_dir):
    assets_dir = os.path.join(base_dir, "extracted", "base", "assets")
    assets = []
    if os.path.exists(assets_dir):
        for root, _, files in os.walk(assets_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, assets_dir).replace("\\", "/")
                size = os.path.getsize(full_path)
                with open(full_path, "rb") as fp:
                    header = fp.read(16)
                magic = header.hex()
                assets.append({
                    "path": rel_path,
                    "size_bytes": size,
                    "header_hex": magic[:16]
                })
    return assets

def inspect_native_libs(base_dir):
    libs = []
    arm64_dir = os.path.join(base_dir, "extracted", "arm64")
    if os.path.exists(arm64_dir):
        for root, _, files in os.walk(arm64_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, arm64_dir).replace("\\", "/")
                size = os.path.getsize(full_path)
                libs.append({
                    "abi": "arm64-v8a",
                    "filename": f,
                    "path": rel_path,
                    "size_bytes": size
                })
    return libs

def inspect_splits(base_dir):
    splits = [
        {
            "split_name": "base",
            "file": "com.prizmos.carista.apk",
            "size_bytes": os.path.getsize(os.path.join(base_dir, "extracted", "com.prizmos.carista.apk")),
            "role": "Application core, bytecode (classes.dex, classes2.dex), resources, assets, AndroidManifest.xml"
        },
        {
            "split_name": "config.arm64_v8a",
            "file": "config.arm64_v8a.apk",
            "size_bytes": os.path.getsize(os.path.join(base_dir, "extracted", "config.arm64_v8a.apk")),
            "role": "Native binaries for 64-bit ARM architecture (libCarista.so, librealm-jni.so)"
        },
        {
            "split_name": "config.xxhdpi",
            "file": "config.xxhdpi.apk",
            "size_bytes": os.path.getsize(os.path.join(base_dir, "extracted", "config.xxhdpi.apk")),
            "role": "Device screen density resources (xxhdpi 480dpi drawables and raster assets)"
        }
    ]
    return splits

def categorize_component(name):
    n = name.lower()
    if "connect" in n or "bluetooth" in n or "elm" in n or "adapter" in n or "device" in n:
        return "Connection / Transport"
    elif "checkcodes" in n or "dtc" in n or "fault" in n:
        return "DTC Diagnostics"
    elif "fullscan" in n or "autoscan" in n or "scan" in n:
        return "AutoScan / Discovery"
    elif "livedata" in n or "sensor" in n or "gauge" in n:
        return "Live Data"
    elif "epb" in n or "dpf" in n or "service" in n or "tpms" in n or "battery" in n or "tool" in n:
        return "Service Tools"
    elif "setting" in n or "customiz" in n or "coding" in n or "adaptation" in n:
        return "Customizations / Coding"
    elif "garage" in n or "vehicle" in n or "history" in n or "vin" in n:
        return "Garage & Vehicle Management"
    elif "account" in n or "auth" in n or "user" in n or "login" in n or "profile" in n:
        return "Account & Authentication"
    elif "billing" in n or "purchase" in n or "subscription" in n or "iap" in n or "pay" in n:
        return "Billing & Subscriptions"
    elif "firebase" in n or "analytics" in n or "crashlytics" in n or "mixpanel" in n:
        return "Telemetry & Analytics"
    else:
        return "Core / General UI"

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    apk_path = os.path.join(base_dir, "extracted", "com.prizmos.carista.apk")

    print("[*] Extracting manifest anatomy via ElementTree...")
    manifest_data = extract_manifest_details(apk_path)

    print("[*] Inspecting assets...")
    assets = inspect_assets(base_dir)

    print("[*] Inspecting native libraries...")
    libs = inspect_native_libs(base_dir)

    print("[*] Inspecting splits...")
    splits = inspect_splits(base_dir)

    for act in manifest_data["activities"]:
        act["feature_area"] = categorize_component(act["name"])

    for srv in manifest_data["services"]:
        srv["feature_area"] = categorize_component(srv["name"])

    for rcv in manifest_data["receivers"]:
        rcv["feature_area"] = categorize_component(rcv["name"])

    package_tree = {
        "metadata": {
            "source_package": manifest_data["package_name"],
            "version_name": manifest_data["version_name"],
            "version_code": manifest_data["version_code"],
            "min_sdk": manifest_data["min_sdk"],
            "target_sdk": manifest_data["target_sdk"],
            "total_activities": len(manifest_data["activities"]),
            "total_services": len(manifest_data["services"]),
            "total_receivers": len(manifest_data["receivers"]),
            "total_providers": len(manifest_data["providers"]),
            "total_permissions": len(manifest_data["permissions"]),
            "total_assets": len(assets),
            "total_native_libs": len(libs)
        },
        "splits": splits,
        "permissions": manifest_data["permissions"],
        "activities": manifest_data["activities"],
        "services": manifest_data["services"],
        "receivers": manifest_data["receivers"],
        "providers": manifest_data["providers"],
        "native_libraries": libs,
        "assets": assets
    }

    out_json = os.path.join(base_dir, "research", "molecular", "package_tree.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(package_tree, f, indent=2)
    print(f"[+] Wrote {out_json}")

    out_md = os.path.join(base_dir, "research", "molecular", "PACKAGE_MAP.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Molecular Package Map & Anatomy\n\n")
        f.write(f"**Target Package**: `{manifest_data['package_name']}`  \n")
        f.write(f"**Version**: `{manifest_data['version_name']}` (code `{manifest_data['version_code']}`)  \n")
        f.write(f"**SDK Requirements**: minSdk `{manifest_data['min_sdk']}`, targetSdk `{manifest_data['target_sdk']}`  \n\n")

        f.write("## 1. Split APK Architecture\n\n")
        f.write("| Split Name | File Name | Size (Bytes) | Role / Content Description |\n")
        f.write("|---|---|---|---|\n")
        for s in splits:
            f.write(f"| `{s['split_name']}` | `{s['file']}` | {s['size_bytes']:,} | {s['role']} |\n")
        f.write("\n")

        f.write("## 2. Component Summary by Feature Area\n\n")
        areas = {}
        for act in manifest_data["activities"]:
            fa = act["feature_area"]
            areas.setdefault(fa, {"activities": [], "services": [], "receivers": []})["activities"].append(act["name"])
        for srv in manifest_data["services"]:
            fa = srv["feature_area"]
            areas.setdefault(fa, {"activities": [], "services": [], "receivers": []})["services"].append(srv["name"])
        for rcv in manifest_data["receivers"]:
            fa = rcv["feature_area"]
            areas.setdefault(fa, {"activities": [], "services": [], "receivers": []})["receivers"].append(rcv["name"])

        f.write("| Feature Area | Activities | Services | Receivers | Total Components |\n")
        f.write("|---|---|---|---|---|\n")
        for fa, comps in sorted(areas.items(), key=lambda x: len(x[1]["activities"]) + len(x[1]["services"]) + len(x[1]["receivers"]), reverse=True):
            tot = len(comps["activities"]) + len(comps["services"]) + len(comps["receivers"])
            f.write(f"| **{fa}** | {len(comps['activities'])} | {len(comps['services'])} | {len(comps['receivers'])} | {tot} |\n")
        f.write("\n")

        f.write("## 3. Activities & Entry Points\n\n")
        f.write("| Activity Class | Exported | Feature Area | Deep Links / Actions |\n")
        f.write("|---|---|---|---|\n")
        for act in manifest_data["activities"]:
            links = ", ".join(act["deep_links"]) if act["deep_links"] else "None"
            f.write(f"| `{act['name'].split('.')[-1]}` (`{act['name']}`) | `{act['exported']}` | {act['feature_area']} | `{links}` |\n")
        f.write("\n")

        f.write("## 4. Native Binaries & JNI Libraries\n\n")
        f.write("| Library | Architecture | Size (Bytes) | Role in Diagnostic Stack |\n")
        f.write("|---|---|---|---|\n")
        for lib in libs:
            role = "Core C++ OBD2/UDS/TP2.0 protocol engine, parameter database, routine controllers" if "Carista" in lib["filename"] else "Realm local database persistence engine"
            f.write(f"| `{lib['filename']}` | `{lib['abi']}` | {lib['size_bytes']:,} | {role} |\n")
        f.write("\n")

        f.write("## 5. Assets & Encrypted Bundles\n\n")
        f.write("| Asset Path | Size (Bytes) | Magic Header | Role / Verification |\n")
        f.write("|---|---|---|---|\n")
        for a in assets:
            role = "PairIP tamper-protected encrypted bytecode (VMRunner)" if a["path"].endswith(".iap") else "Static asset"
            f.write(f"| `{a['path']}` | {a['size_bytes']:,} | `0x{a['header_hex']}` | {role} |\n")
        f.write("\n")

        f.write("## 6. Permissions & Hardware Security Profile\n\n")
        f.write("| Permission | Protection Level |\n")
        f.write("|---|---|\n")
        for p in manifest_data["permissions"]:
            f.write(f"| `{p['name']}` | `{p['protection_level']}` |\n")
        f.write("\n")

    print(f"[+] Wrote {out_md}")

if __name__ == "__main__":
    main()
