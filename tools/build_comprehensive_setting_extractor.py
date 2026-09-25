import os
import re
import json
import capstone
from elftools.elf.elffile import ELFFile

def parse_imm(s):
    s = s.strip()
    try:
        return int(s, 0)
    except ValueError:
        return 0

def demangle(name):
    if not name.startswith('_ZN'):
        return name
    s = name[3:]
    if s.endswith('E'):
        s = s[:-1]
    parts = []
    i = 0
    while i < len(s):
        m = re.match(r'(\d+)', s[i:])
        if not m:
            parts.append(s[i:])
            break
        num = int(m.group(1))
        start = i + len(m.group(1))
        parts.append(s[start:start+num])
        i = start + num
    return '::'.join(parts)

def build_extractor():
    base_dir = "d:\\ghidracarista"
    so_path = os.path.join(base_dir, "extracted", "arm64", "lib", "arm64-v8a", "libCarista.so")
    c_path = os.path.join(base_dir, "libCarista.so.c")
    
    # 1. Load pre-resolved factory classes
    print("[*] Loading resolved factory classes...")
    factories_map_path = os.path.join(base_dir, "research", "molecular", "resolved_factories_map.json")
    with open(factories_map_path, "r", encoding="utf-8") as f:
        factories_raw = json.load(f)
    factory_classes = {int(k, 16): v for k, v in factories_raw.items()}
    print(f"[+] Loaded {len(factory_classes)} factory classes.")

    # 2. Load ELF metadata
    print("[*] Loading ELF relocations and rodata strings...")
    with open(so_path, 'rb') as f:
        elf = ELFFile(f)
        
        rodata = elf.get_section_by_name('.rodata')
        rodata_data = rodata.data()
        rodata_addr = rodata['sh_addr']
        
        def read_string(addr):
            if rodata_addr <= addr < rodata_addr + len(rodata_data):
                offset = addr - rodata_addr
                end = rodata_data.find(b'\x00', offset)
                if end != -1:
                    return rodata_data[offset:end].decode('utf-8', errors='ignore')
            return None

        got_map = {}
        for sec in elf.iter_sections():
            if 'rela' in sec.name.lower():
                symtab = elf.get_section(sec['sh_link'])
                for rel in sec.iter_relocations():
                    sym = symtab.get_symbol(rel['r_info_sym'])
                    if sym.name:
                        got_map[rel['r_offset']] = demangle(sym.name)

        func_addr = 0x1402f68
        func_size = 502868
        f.seek(func_addr)
        code = f.read(func_size)

    print(f"[+] Read {len(code)} bytes of ARM64 machine code.")
    cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    cs.detail = True

    instructions = list(cs.disasm(code, func_addr))
    print(f"[+] Disassembled {len(instructions)} instructions.")

    # 3. Precise register & argument tracking
    regs = {}
    regs_meta = {}
    extracted = []
    
    for idx, ins in enumerate(instructions):
        if ins.mnemonic == 'adrp':
            reg = ins.op_str.split(',')[0].strip()
            imm = parse_imm(ins.op_str.split('#')[1])
            regs[reg] = imm
        elif ins.mnemonic == 'add':
            parts = [p.strip() for p in ins.op_str.split(',')]
            dst = parts[0]
            src = parts[1]
            if src in regs and isinstance(regs[src], int) and len(parts) >= 3 and '#' in parts[2]:
                imm = parse_imm(parts[2].split('#')[1])
                full_addr = regs[src] + imm
                regs[dst] = full_addr
                s = read_string(full_addr)
                if s and s.startswith('car_setting_'):
                    regs_meta[dst + '_str'] = (s, hex(ins.address), "add " + ins.op_str)
        elif ins.mnemonic == 'ldr':
            parts = [p.strip() for p in ins.op_str.split(',')]
            dst = parts[0]
            m_mem = re.search(r'\[\s*([a-zA-Z0-9]+)(?:,\s*#([0-9a-fx\-]+))?\s*\]', ins.op_str)
            if m_mem:
                base_reg = m_mem.group(1)
                offset = parse_imm(m_mem.group(2)) if m_mem.group(2) else 0
                if base_reg in regs and isinstance(regs[base_reg], int):
                    target_addr = regs[base_reg] + offset
                    if target_addr in got_map:
                        sym = got_map[target_addr]
                        regs_meta[dst + '_sym'] = (sym, hex(ins.address), f"ldr {dst}, [GOT {hex(target_addr)}]")
        elif ins.mnemonic == 'mov':
            parts = [p.strip() for p in ins.op_str.split(',')]
            dst = parts[0]
            if len(parts) >= 2 and '#' in parts[1]:
                val = parse_imm(parts[1].split('#')[1])
                regs[dst] = val
                regs_meta[dst] = (val, hex(ins.address), ins.op_str)
        elif ins.mnemonic == 'bl':
            target_str = ins.op_str.strip()
            target_addr = parse_imm(target_str.replace("#", ""))
            
            setting_info = None
            setting_reg = None
            for r in ['x5_str', 'x6_str', 'x7_str', 'x4_str', 'x1_str', 'x2_str', 'x3_str']:
                if r in regs_meta and regs_meta[r][0].startswith('car_setting_'):
                    setting_info = regs_meta[r]
                    setting_reg = r
                    break
            
            if setting_info:
                key, key_callsite, key_stmt = setting_info
                
                if target_addr in [0xe00240, 0xf00240] and key.startswith("car_setting_instruction_"):
                    if extracted:
                        extracted[-1]["instructions"].append({
                            "key": key,
                            "callsite": hex(ins.address)
                        })
                    del regs_meta[setting_reg]
                    continue

                cls = factory_classes.get(target_addr, "UnknownVagSettingClass")
                
                ecu_info = None
                wl_info = None
                interp_info = None
                
                for r in ['x1_sym', 'x2_sym', 'x3_sym', 'x4_sym']:
                    if r in regs_meta:
                        s_name = regs_meta[r][0]
                        if "Ecu" in s_name:
                            ecu_info = regs_meta[r]
                        elif "Whitelist" in s_name:
                            wl_info = regs_meta[r]
                        elif "Interpretation" in s_name:
                            interp_info = regs_meta[r]
                
                w8_val = regs_meta.get('w8')
                w9_val = regs_meta.get('w9')
                w1_val = regs_meta.get('w1')
                w2_val = regs_meta.get('w2')
                w3_val = regs_meta.get('w3')
                
                extracted.append({
                    "asm_address": hex(ins.address),
                    "factory_address": hex(target_addr),
                    "concrete_class": cls,
                    "setting_key": key,
                    "key_provenance": {
                        "callsite": key_callsite,
                        "instruction": key_stmt
                    },
                    "ecu": {
                        "name": ecu_info[0] if ecu_info else None,
                        "callsite": ecu_info[1] if ecu_info else None,
                        "evidence": ecu_info[2] if ecu_info else None
                    },
                    "whitelist": {
                        "name": wl_info[0] if wl_info else None,
                        "callsite": wl_info[1] if wl_info else None,
                        "evidence": wl_info[2] if wl_info else None
                    },
                    "interpretation": {
                        "name": interp_info[0] if interp_info else None,
                        "callsite": interp_info[1] if interp_info else None
                    },
                    "w8": w8_val,
                    "w9": w9_val,
                    "w1": w1_val,
                    "w2": w2_val,
                    "w3": w3_val,
                    "instructions": []
                })
                
                del regs_meta[setting_reg]

    print(f"\n[+] Total settings extracted from VagCanSettings::getSettings: {len(extracted)}")
    unique_keys = set(e['setting_key'] for e in extracted)
    print(f"[+] Unique setting keys: {len(unique_keys)}")
    
    out_path = os.path.join(base_dir, "research", "molecular", "asm_extracted_settings.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=2)
    print(f"[+] Wrote {out_path}")

    # Sample output
    for e in extracted[:15]:
        ecu_str = str(e['ecu']['name']) if e['ecu'] else 'None'
        wl_str = str(e['whitelist']['name']) if e['whitelist'] else 'None'
        w8_v = str(e['w8'][0]) if e['w8'] else 'None'
        w9_v = str(e['w9'][0]) if e['w9'] else 'None'
        print(f"{e['asm_address']} | {e['setting_key']:40s} | {e['concrete_class']:25s} | ECU={ecu_str:25s} | WL={wl_str:25s} | w8={w8_v:5s} | w9={w9_v:5s}")

if __name__ == '__main__':
    build_extractor()
