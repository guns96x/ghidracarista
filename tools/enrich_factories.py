import re
import json

def enrich_factories():
    with open('research/molecular/resolved_factories_map.json', 'r') as f:
        factories = json.load(f)

    print(f"Loaded {len(factories)} existing factories.")

    # Scan libCarista.so.c for all FUN_015xxxxx definitions
    c_path = 'libCarista.so.c'
    with open(c_path, 'r', encoding='utf-8', errors='ignore') as f:
        c_lines = f.readlines()

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
        "VagCanCodingSetting",
        "VagUdsVimSetting"
    ]

    added = 0
    func_pattern = re.compile(r'^(?:void|undefined[0-9* ]+)\s+(FUN_015[0-9a-f]{5})\(')
    for idx, line in enumerate(c_lines):
        m = func_pattern.match(line)
        if m:
            fun = m.group(1)
            fun_addr_hex = hex(int(fun[4:], 16) - 0x100000)
            chunk = "".join(c_lines[idx:idx+45])
            for tc in target_classes:
                if tc in chunk:
                    if fun_addr_hex not in factories:
                        factories[fun_addr_hex] = tc
                        added += 1
                    break

    print(f"Added {added} new factory mappings from libCarista.so.c! Total: {len(factories)}")
    
    with open('research/molecular/resolved_factories_map.json', 'w', encoding='utf-8') as f:
        json.dump(factories, f, indent=2)

if __name__ == '__main__':
    enrich_factories()
