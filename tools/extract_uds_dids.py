import re

with open(r"d:\ghidracarista\libCarista.so.c", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Pattern 1: classes with getRequest
matches = re.findall(r'// (([A-Za-z0-9_<>]+)::getRequest\(\)[^\n]*)\n(.*?)(?=\n//|\Z)', text, re.DOTALL)
print(f"Total getRequest methods found: {len(matches)}")
for header, cls, body in matches:
    if "Vag" in cls:
        hexes = re.findall(r'operator____b\("([0-9A-Fa-f]+)"', body)
        byte_utils = re.findall(r'ByteUtils::getBytesFromShort\([^,]+,\s*(0x[0-9A-Fa-f]+|\d+)\)', body)
        short_consts = re.findall(r'\*(?:ushort|undefined2)\s*\*\)\s*[^=]+=\s*(0x[0-9A-Fa-f]+|\d+);', body)
        single_bytes = re.findall(r'\*(?:undefined1|byte)\s*\*\)\s*[^=]+=\s*(0x[0-9A-Fa-f]+|\d+);', body)
        print(f"\n{cls}::getRequest():")
        if hexes:
            print(f"  Hex literals: {hexes}")
        if byte_utils:
            print(f"  getBytesFromShort: {byte_utils}")
        if short_consts:
            print(f"  Short constants: {short_consts}")
        if single_bytes:
            print(f"  Byte constants: {single_bytes}")
