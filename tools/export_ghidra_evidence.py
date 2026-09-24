import os
import re
import json
from elftools.elf.elffile import ELFFile
import itanium_demangler

SO_PATH = r"d:\ghidracarista\extracted\arm64\lib\arm64-v8a\libCarista.so"
C_PATH = r"d:\ghidracarista\libCarista.so.c"
OUT_DIR = r"d:\ghidracarista\research\ghidra_export"

def extract_elf_symbols():
    print("[1/3] Extracting dynamic symbols from libCarista.so...")
    symbols = []
    with open(SO_PATH, "rb") as f:
        elf = ELFFile(f)
        dynsym = elf.get_section_by_name('.dynsym')
        for s in dynsym.iter_symbols():
            raw_name = s.name
            if not raw_name:
                continue
            addr = s['st_value']
            sym_type = s['st_info']['type']
            
            # Check relevance
            lower = raw_name.lower()
            if any(k in lower for k in ['vag', 'uds', 'kwp', 'elm', 'stn', 'can', 'isotp', 'troublecode',
                                        'coding', 'adaptation', 'basicsetting', 'routine', 'dpf',
                                        'parkingbrake', 'batteryreg', 'livedata', 'session', 'ecu']):
                demangled = raw_name
                if raw_name.startswith('_Z'):
                    try:
                        parsed = itanium_demangler.parse(raw_name)
                        if parsed:
                            demangled = str(parsed)
                    except Exception:
                        pass
                
                symbols.append({
                    "virtual_address": hex(addr),
                    "raw_symbol": raw_name,
                    "demangled": demangled,
                    "type": sym_type
                })
    print(f"Extracted {len(symbols)} relevant protocol symbols.")
    return symbols

def parse_decompiled_c():
    print("[2/3] Parsing decompiled C constructs from libCarista.so.c (52MB)...")
    commands = {}
    current_func = None
    func_lines = []
    
    # We will stream through libCarista.so.c line by line
    with open(C_PATH, "r", encoding="utf-8", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            # Check for function headers comments or definitions
            # Ghidra emits lines like: // WriteVagCanBasicSettingCommand::getRequest() const
            # or void __thiscall WriteVagCanBasicSettingCommand::getRequest(WriteVagCanBasicSettingCommand *this)
            if "::" in line and "(" in line and not line.startswith("typedef") and not line.startswith("struct"):
                match = re.search(r'([A-Za-z0-9_<>]+)::([A-Za-z0-9_~]+)\(', line)
                if match:
                    cls_name, method_name = match.group(1), match.group(2)
                    full_name = f"{cls_name}::{method_name}"
                    
                    # Store previous function if relevant
                    if current_func and func_lines:
                        analyze_func_body(current_func, func_lines, commands)
                    
                    current_func = {
                        "class": cls_name,
                        "method": method_name,
                        "line_start": line_num,
                        "full_name": full_name
                    }
                    func_lines = [line]
                    continue
            
            if current_func:
                func_lines.append(line)
                if line.startswith("}"):
                    analyze_func_body(current_func, func_lines, commands)
                    current_func = None
                    func_lines = []

    print(f"Parsed {len(commands)} distinct diagnostic command classes.")
    return commands

def analyze_func_body(func_info, lines, commands):
    cls = func_info["class"]
    method = func_info["method"]
    body = "".join(lines)
    
    # Check if this class is diagnostic relevant
    lower_cls = cls.lower()
    if not any(k in lower_cls for k in ['vag', 'uds', 'kwp', 'can', 'elm', 'stn', 'troublecode', 'command', 'setting', 'routine', 'operation']):
        return
        
    if cls not in commands:
        commands[cls] = {
            "class_name": cls,
            "methods": {},
            "hex_literals": set(),
            "routine_ids": set(),
            "dids": set(),
            "log_strings": set(),
            "addresses": set()
        }
    
    entry = commands[cls]
    entry["methods"][method] = {
        "line_start": func_info["line_start"],
        "lines_count": len(lines)
    }
    
    # Extract hex string literals (e.g., operator____b("1802FF00", 8))
    hex_strs = re.findall(r'operator____b\("([0-9A-Fa-f]+)"', body)
    for h in hex_strs:
        entry["hex_literals"].add(h.upper())
        
    # Extract routine IDs (e.g. RoutineControlCommand(..., 0x3a1, ...) or uVar4 = 0x53d)
    routines = re.findall(r'RoutineControlCommand\([^,]+,[^,]+,[^,]+,(0x[0-9a-fA-F]+)', body)
    for r in routines:
        entry["routine_ids"].add(r)
    routines2 = re.findall(r'uVar\d+ = (0x[0-9a-fA-F]{3,4});', body)
    for r in routines2:
        entry["routine_ids"].add(r)
        
    # Extract DIDs (e.g. ReadDataByIdentifierCommand or *(ushort *)(this + 0x1c) = 0x... or 0x22 / 0x2e)
    dids = re.findall(r'ReadVagUdsStatusCommand\([^,]+,[^,]+,(0x[0-9a-fA-F]+)\)', body)
    for d in dids:
        entry["dids"].add(d)
        
    # Extract Log strings
    logs = re.findall(r'Log::[dewi]\("([^"]+)"', body)
    for l in logs:
        entry["log_strings"].add(l)
        
    # Extract pointer references (e.g. PTR__WriteVagCanBasicSettingCommand_01b565e8)
    ptrs = re.findall(r'PTR__([A-Za-z0-9_]+)_([0-9a-fA-F]{8})', body)
    for p_name, p_addr in ptrs:
        entry["addresses"].add(f"0x{p_addr}")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    symbols = extract_elf_symbols()
    sym_out = os.path.join(OUT_DIR, "symbols_vag.json")
    with open(sym_out, "w", encoding="utf-8") as f:
        json.dump(symbols, f, indent=2)
    print(f"Saved {sym_out}")
    
    cmd_data = parse_decompiled_c()
    # Serialize set to list for JSON
    serializable = {}
    for k, v in cmd_data.items():
        if v["hex_literals"] or v["routine_ids"] or v["dids"] or v["log_strings"] or "Command" in k or "Setting" in k or "Operation" in k:
            serializable[k] = {
                "class_name": v["class_name"],
                "methods": v["methods"],
                "hex_literals": sorted(list(v["hex_literals"])),
                "routine_ids": sorted(list(v["routine_ids"])),
                "dids": sorted(list(v["dids"])),
                "log_strings": sorted(list(v["log_strings"])),
                "addresses": sorted(list(v["addresses"]))
            }
            
    cmd_out = os.path.join(OUT_DIR, "commands_evidence.json")
    with open(cmd_out, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)
    print(f"Saved {cmd_out} with {len(serializable)} verified diagnostic classes.")

if __name__ == "__main__":
    main()
