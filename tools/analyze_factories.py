import re

def analyze_factories():
    with open("libCarista.so.c", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    fun_calls = set()
    for idx in range(519330, 527137):
        matches = re.findall(r'\b(FUN_015[0-9a-f]{5})\b', lines[idx])
        for m in matches:
            fun_calls.add(m)

    print(f"Total distinct factory candidate functions in block: {len(fun_calls)}")

    # Fast single pass over lines
    def_pattern = re.compile(r'^(?:void|undefined[0-9* ]+)\s+(FUN_015[0-9a-f]{5})\(')
    factory_map = {}
    
    for idx, line in enumerate(lines):
        m = def_pattern.match(line)
        if m:
            fun = m.group(1)
            if fun in fun_calls:
                def_chunk = "".join(lines[idx:idx+40])
                m_class = re.search(r'__shared_ptr_emplaceI([0-9A-Za-z_]+)', def_chunk)
                direct_class = re.search(r'([A-Za-z0-9_]+Setting) \*this', def_chunk)
                direct_class2 = re.search(r'([A-Za-z0-9_]+Setting)::\1', def_chunk)
                
                class_name = None
                if m_class:
                    raw_cls = m_class.group(1)
                    class_name = re.sub(r'^[0-9]+', '', raw_cls)
                elif direct_class:
                    class_name = direct_class.group(1)
                elif direct_class2:
                    class_name = direct_class2.group(1)

                factory_map[fun] = {
                    "defined_line": idx + 1,
                    "class_name": class_name,
                    "raw_symbol": m_class.group(0) if m_class else None
                }

    print(f"Mapped {len(factory_map)} factories:")
    for fn, info in sorted(factory_map.items()):
        print(f"  {fn} at line {info['defined_line']}: class={info['class_name']}")

if __name__ == "__main__":
    analyze_factories()
