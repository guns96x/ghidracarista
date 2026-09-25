#!/usr/bin/env python3
"""
tools/audit_settings_molecular.py
Deep audit of all setting factory calls and string constants in libCarista.so.c.
Identifies:
1. Exact concrete C++ factory functions
2. Top-level settings vs option value aliases
3. ECU associations and byte/bit masks
"""

import os
import re
import json

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    so_c_path = os.path.join(base_dir, "libCarista.so.c")
    print(f"[*] Reading {so_c_path}...")

    # Pattern for string assignment or function argument
    setting_pattern = re.compile(r'"(car_setting_[a-zA-Z0-9_]+)"')
    ecu_pattern = re.compile(r'&(VagUdsEcu::[A-Za-z0-9_]+|VagCanEcu::[A-Za-z0-9_]+)')
    wl_pattern = re.compile(r'(VagWhitelists::[A-Za-z0-9_]+)')
    interp_pattern = re.compile(r'&(MultipleChoiceInterpretation::[A-Za-z0-9_]+|NumericalInterpretation::[A-Za-z0-9_]+)')

    results = {}
    with open(so_c_path, "r", encoding="utf-8", errors="ignore") as f:
        window = []
        for line_no, line in enumerate(f, 1):
            window.append(line)
            if len(window) > 25:
                window.pop(0)

            if "car_setting_" in line and not line.strip().startswith("//"):
                m = setting_pattern.search(line)
                if m:
                    key = m.group(1)
                    block = "".join(window)
                    ecu_m = ecu_pattern.search(block)
                    wl_m = wl_pattern.search(block)
                    interp_m = interp_pattern.search(block)

                    ecu = ecu_m.group(1) if ecu_m else None
                    wl = wl_m.group(1) if wl_m else None
                    interp = interp_m.group(1) if interp_m else None

                    if key not in results or (ecu and not results[key].get("ecu")):
                        results[key] = {
                            "key": key,
                            "line": line_no,
                            "ecu": ecu,
                            "whitelist": wl,
                            "interpretation": interp,
                            "sample_line": line.strip()[:100]
                        }

    print(f"[+] Total distinct setting keys located: {len(results)}")
    with_ecu = [k for k, v in results.items() if v["ecu"]]
    print(f"[+] Setting keys with direct ECU reference: {len(with_ecu)}")

    out_file = os.path.join(base_dir, "research", "molecular", "raw_extracted_settings.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"[+] Saved {out_file}")

if __name__ == "__main__":
    main()
