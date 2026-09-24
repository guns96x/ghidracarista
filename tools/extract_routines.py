import re

c_file = r"D:\ghidracarista\libCarista.so.c"

# We want to find DIDs, Routine IDs, Service handlers
keywords = ["0x22", "0x31", "0x10", "0x19", "0x2e", "0x3e", "F190", "F187", "F1A3", "EPB", "Dpf", "Oil"]

print("Analyzing libCarista.so.c for key diagnostic patterns...")

found_patterns = {}
with open(c_file, "r", encoding="latin1", errors="ignore") as f:
    for line_num, line in enumerate(f):
        for kw in ["VagUds", "VagCan", "RoutineControl", "ReadDataByIdentifier", "BasicSetting", "BmwF", "DpfTool"]:
            if kw in line:
                found_patterns.setdefault(kw, []).append((line_num, line.strip()))
                if len(found_patterns[kw]) > 5:
                    break

for k, v in found_patterns.items():
    print(f"\nKeyword {k}: found {len(v)} occurrences (sample):")
    for ln, text in v[:3]:
        print(f"  Line {ln}: {text[:120]}")
