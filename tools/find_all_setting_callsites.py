import re
import json

def find_all():
    with open("libCarista.so.c", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    target_classes = [
        "VagUdsCodingSetting",
        "VagUdsAdaptationSetting",
        "FullByteVagCanShortAdaptationSetting",
        "VagCanShortAdaptationSetting",
        "FullByteVagUdsAdaptationSetting",
        "VagCanLongCodingSetting",
        "VagCanShortCodingSetting",
        "VagUdsSubmoduleCodingSetting",
        "VagUdsOverCanSubmoduleCodingSetting",
        "VagCanCodingSetting"
    ]

    factory_funcs = {}
    func_pattern = re.compile(r'^(?:void|undefined[0-9* ]+)\s+(FUN_[0-9a-fA-F_]+|[A-Za-z0-9_:]+)\(')

    for idx, line in enumerate(lines):
        m = func_pattern.match(line)
        if m:
            fn = m.group(1)
            chunk = "".join(lines[idx:idx+45])
            for tc in target_classes:
                if tc in chunk:
                    factory_funcs[fn] = {
                        "class": tc,
                        "line": idx + 1
                    }
                    break

    print(f"Found {len(factory_funcs)} factory functions defining target VAG setting classes.")

    # Compile regex of all factory names
    fact_regex = re.compile(r'\b(' + '|'.join(re.escape(k) for k in factory_funcs.keys()) + r')\(')
    
    callsites = []
    for idx, line in enumerate(lines):
        lno = idx + 1
        m_fn = fact_regex.search(line)
        if m_fn:
            fn = m_fn.group(1)
            stmt = line.strip()
            j = idx
            while ";" not in lines[j] and j < min(len(lines), idx + 15):
                j += 1
                stmt += " " + lines[j].strip()
            
            m_key = re.search(r'"(car_setting_[a-zA-Z0-9_]+)"', stmt)
            key = m_key.group(1) if m_key else None
            
            callsites.append({
                "line": lno,
                "factory": fn,
                "class": factory_funcs[fn]["class"],
                "key": key,
                "statement": stmt[:220]
            })

    print(f"Total callsites found across libCarista.so.c: {len(callsites)}")
    with_key = [c for c in callsites if c["key"]]
    print(f"Callsites with explicit car_setting_* key: {len(with_key)}")
    without_key = [c for c in callsites if not c["key"]]
    print(f"Callsites without explicit car_setting_* key: {len(without_key)}")

    unique_keys = set(c["key"] for c in with_key)
    print(f"Unique setting keys from ALL callsites: {len(unique_keys)}")

    outside = [c for c in callsites if c["line"] < 519000 or c["line"] > 529000]
    print(f"Callsites OUTSIDE lines 519000-529000: {len(outside)}")
    for c in outside[:25]:
        print(f"  Line {c['line']}: {c['factory']} ({c['class']}) key={c['key']} stmt={c['statement'][:80]}")

if __name__ == "__main__":
    find_all()
