import re

c_file = r"D:\ghidracarista\libCarista.so.c"

print("Searching for EPB, ServiceReset and Oil in libCarista.so.c...")

matches = []
with open(c_file, "r", encoding="latin1", errors="ignore") as f:
    for line_num, line in enumerate(f):
        if any(w in line for w in ["Epb", "ServiceIndicator", "OilReset", "BrakePad", "BatteryReg"]):
            matches.append((line_num, line.strip()))
            if len(matches) >= 30:
                break

for ln, text in matches:
    print(f"Line {ln}: {text[:130]}")
