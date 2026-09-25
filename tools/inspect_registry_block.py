#!/usr/bin/env python3
import os
import re
import json

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    so_c = os.path.join(base_dir, "libCarista.so.c")
    pattern = re.compile(r'"(car_setting_[a-zA-Z0-9_]+)"')

    occurrences = {}
    with open(so_c, "r", encoding="utf-8", errors="ignore") as f:
        for line_no, line in enumerate(f, 1):
            if "car_setting_" in line and not line.strip().startswith("//"):
                matches = pattern.findall(line)
                for m in matches:
                    occurrences.setdefault(m, []).append((line_no, line.strip()[:120]))

    print(f"Total distinct car_setting_* keys in C code: {len(occurrences)}")
    
    # Save to JSON for exact provenance mapping
    out_path = os.path.join(base_dir, "research", "molecular", "c_setting_occurrences.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(occurrences, f, indent=2)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    main()
