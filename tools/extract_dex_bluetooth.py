import os
from androguard.core.dex import DEX

dex_paths = [
    r"d:\ghidracarista\extracted\base\classes.dex",
    r"d:\ghidracarista\extracted\base\classes2.dex"
]

print("Scanning DEX files for Bluetooth, UUID, and Adapter detection...")

for path in dex_paths:
    print(f"\n--- Checking {os.path.basename(path)} ---")
    with open(path, "rb") as f:
        d = DEX(f.read())
        
        # Search strings
        found_strings = set()
        for s in d.get_strings():
            s_str = str(s)
            if any(k in s_str.lower() for k in ["00001101", "carista", "vgate", "obdlink", "elm327", "stn", "vlinker"]):
                if len(s_str) < 80 and not s_str.startswith("http") and not s_str.startswith("com."):
                    found_strings.add(s_str)
                    
        for fs in sorted(found_strings)[:30]:
            print(f"  String: {fs}")
                    
        # Search classes
        for c in d.get_classes():
            c_name = c.get_name()
            if any(k in c_name for k in ["Bluetooth", "Adapter", "Elm", "ConnectionManager", "Ble"]):
                if "prizmos" in c_name:
                    print(f"\n  Class: {c_name}")
                    for m in c.get_methods():
                        m_name = m.get_name()
                        if not m_name.startswith("$") and not m_name == "<init>":
                            print(f"    Method: {m_name}")
