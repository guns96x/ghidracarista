import re

so_path = r"D:\ghidracarista\extracted\arm64\lib\arm64-v8a\libCarista.so"

with open(so_path, "rb") as f:
    data = f.read()

# All JNI exports
jni_funcs = sorted(set(re.findall(rb"Java_[a-zA-Z0-9_]+", data)))
print("TOTAL JNI METHODS:", len(jni_funcs))

# Look for OEM subsystems
oems = ["Vag", "Bmw", "Toyota", "Ford", "Nissan", "Renault", "Gm", "Hyundai", "Fiat", "Honda", "Subaru"]
oem_symbols = {}
for oem in oems:
    syms = set(re.findall(rb"[A-Za-z0-9_]*" + oem.encode() + rb"[A-Za-z0-9_]*", data))
    # filter for meaningful identifiers
    meaningful = [s.decode('latin1', errors='ignore') for s in syms if len(s) > len(oem) + 2 and not s.startswith(b"/")]
    oem_symbols[oem] = len(meaningful)
    print(f"OEM: {oem:<10} -> {len(meaningful)} symbols")

# Look for URLs or API endpoints
urls = set(re.findall(rb"https?://[a-zA-Z0-9_\-\./]+", data))
print("\n--- Network Endpoints Found in SO ---")
for u in sorted(urls):
    print("  ", u.decode('latin1', errors='ignore'))

# Look for Api Client methods
api_methods = set(re.findall(rb"_ZN16CaristaApiClient[0-9a-zA-Z_]+", data))
print(f"\n--- CaristaApiClient Methods ({len(api_methods)}) ---")
for m in sorted(api_methods)[:20]:
    print("  ", m.decode('latin1', errors='ignore'))

