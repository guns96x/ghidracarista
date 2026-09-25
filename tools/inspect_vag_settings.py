import re
import json

def inspect():
    with open("libCarista.so.c", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    print(f"Total lines: {len(lines)}")
    
    # Track all occurrences of car_setting_ in VagCanSettingsBanned (519330 - 527137)
    settings_found = []
    current_vars = {}
    
    # We want to inspect the C++ structure
    for idx in range(519330, min(len(lines), 527137)):
        line = lines[idx]
        lno = idx + 1
        
        # Look for setting string
        m = re.search(r'"(car_setting_[a-zA-Z0-9_]+)"', line)
        if m:
            key = m.group(1)
            # Grab context 20 lines back and 5 lines forward
            context_start = max(519330, idx - 20)
            context_end = min(len(lines), idx + 6)
            context = "".join(lines[context_start:context_end])
            settings_found.append({
                "line": lno,
                "key": key,
                "context": lines[context_start:context_end]
            })

    print(f"Total car_setting_* occurrences in VagCanSettingsBanned: {len(settings_found)}")
    
    # Let's inspect unique keys
    unique_keys = set(s["key"] for s in settings_found)
    print(f"Unique keys: {len(unique_keys)}")
    
    # Sample first 20 keys
    for s in settings_found[:20]:
        print(f"L{s['line']}: {s['key']}")

if __name__ == "__main__":
    inspect()
