import sys
import re

so_path = r"D:\ghidracarista\extracted\arm64\lib\arm64-v8a\libCarista.so"

with open(so_path, "rb") as f:
    data = f.read()

print(f"Total binary size: {len(data) / 1024 / 1024:.2f} MB")

# Extract JNI functions
jni_matches = set(re.findall(rb"Java_com_[a-zA-Z0-9_]+", data))
print(f"\n--- Found {len(jni_matches)} JNI Exported Functions ---")
for m in sorted(jni_matches)[:40]:
    print(m.decode('latin1', errors='ignore'))

# Extract OBD / CAN / AT commands
at_cmds = set(re.findall(rb"AT[A-Z0-9]{2,8}", data))
print(f"\n--- Found {len(at_cmds)} AT / ELM commands ---")
for m in sorted(at_cmds)[:25]:
    print(m.decode('latin1', errors='ignore'))

# Extract C++ typeinfo symbols (_ZTS or _ZTI)
typeinfos = set(re.findall(rb"_ZTS[0-9A-Za-z_]+", data))
print(f"\n--- Found {len(typeinfos)} C++ TypeInfo Symbols ---")
for m in sorted(typeinfos)[:30]:
    print(m.decode('latin1', errors='ignore'))

# Search for interesting string patterns: "ECU", "diagnostic", "protocol", "security", "seed", "vin"
keywords = [b"VIN", b"OBD", b"ECU", b"ISO14229", b"UDS", b"KWP", b"CAN", b"Carista"]
for kw in keywords:
    matches = set(re.findall(rb"[A-Za-z0-9_/\.:-]{0,20}" + kw + rb"[A-Za-z0-9_/\.:-]{0,20}", data))
    print(f"\nMatches for keyword '{kw.decode()}': {len(matches)} found. Sample:")
    for sm in list(matches)[:10]:
        print("  ", sm.decode('latin1', errors='ignore'))
