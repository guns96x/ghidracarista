import re

so_path = r"D:\ghidracarista\extracted\arm64\lib\arm64-v8a\libCarista.so"

with open(so_path, "rb") as f:
    data = f.read()

# Look for State enum / state machine names
states = set(re.findall(rb"STATE_[A-Z0-9_]+", data))
print(f"--- Connection / Protocol States ({len(states)}) ---")
for s in sorted(states)[:30]:
    print(" ", s.decode('latin1', errors='ignore'))

# Look for VAG protocols and classes
vag_classes = set(re.findall(rb"_ZTS[0-9A-Za-z_]*Vag[0-9A-Za-z_]*", data))
print(f"\n--- VAG Classes in SO ({len(vag_classes)}) ---")
for vc in sorted(vag_classes)[:30]:
    print(" ", vc.decode('latin1', errors='ignore'))

# Look for UDS / CAN commands and services
uds_services = set(re.findall(rb"UDS_[A-Z0-9_]+", data))
print(f"\n--- UDS Services ({len(uds_services)}) ---")
for us in sorted(uds_services)[:25]:
    print(" ", us.decode('latin1', errors='ignore'))

# Look for ELM initialization commands in order
elm_init = set(re.findall(rb"AT[A-Z0-9 ]+", data))
print(f"\n--- ELM / AT Sequence Strings ({len(elm_init)}) ---")
for cmd in [c for c in sorted(elm_init) if 2 <= len(c) <= 12][:25]:
    print(" ", cmd.decode('latin1', errors='ignore'))
