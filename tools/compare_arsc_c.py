#!/usr/bin/env python3
import os
import re
from loguru import logger
logger.disable("androguard")
from androguard.core.apk import APK

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    apk_path = os.path.join(base_dir, "extracted", "com.prizmos.carista.apk")
    apk = APK(apk_path)
    res = apk.get_android_resources()

    setting_strings = {}
    for pkg in res.get_packages_names():
        for res_type in res.get_types(pkg):
            if res_type == "string":
                for item in res.get_strings_resources():
                    # item format
                    pass

    # Alternative direct arsc inspection
    with open(os.path.join(base_dir, "extracted", "base", "resources.arsc"), "rb") as f:
        data = f.read()

    # Search for all car_setting_ strings in UTF-8 / ASCII in arsc
    arsc_keys = set(re.findall(b'car_setting_[a-zA-Z0-9_]+', data))
    arsc_keys_clean = sorted([k.decode('ascii') for k in arsc_keys])
    print(f"Total car_setting_* keys in resources.arsc: {len(arsc_keys_clean)}")

    import json
    with open(os.path.join(base_dir, "research", "molecular", "c_setting_occurrences.json")) as f:
        c_keys = json.load(f)

    in_c = set(c_keys.keys())
    in_arsc = set(arsc_keys_clean)

    common = in_c.intersection(in_arsc)
    arsc_only = in_arsc - in_c
    c_only = in_c - in_arsc

    print(f"Keys present in BOTH C++ and resources.arsc: {len(common)}")
    print(f"Keys present in resources.arsc ONLY (Unresolved in C++): {len(arsc_only)}")
    print(f"Keys present in C++ ONLY: {len(c_only)}")
    if arsc_only:
        print("Sample arsc_only:", sorted(list(arsc_only))[:15])

if __name__ == "__main__":
    main()
