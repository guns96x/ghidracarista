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

def extract_banned_asm():
    base_dir = r"d:\ghidracarista"
    so_path = os.path.join(base_dir, "extracted", "arm64", "lib", "arm64-v8a", "libCarista.so")
    factories_map_path = os.path.join(base_dir, "research", "molecular", "resolved_factories_map.json")
    
    with open(factories_map_path, "r", encoding="utf-8") as f:
        factories_raw = json.load(f)
    factory_classes = {int(k, 16): v for k, v in factories_raw.items()}

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

        # VagCanSettingsBanned::getSettings() is at 0x14d0140, size ~ 110,000 bytes
        func_addr = 0x14d0140
        func_size = 110000
        f.seek(func_addr)
        code = f.read(func_size)

    cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    cs.detail = True
    instructions = list(cs.disasm(code, func_addr))
    print(f"[+] Disassembled {len(instructions)} instructions in VagCanSettingsBanned.")

    regs = {}
    regs_meta = {}
    stack_slots = {}
    extracted = []

    for ins in instructions:
        # 1. adrp
        if ins.mnemonic == 'adrp':
            reg = ins.op_str.split(',')[0].strip()
            imm = parse_imm(ins.op_str.split('#')[1])
            regs[reg] = imm
        # 2. add
        elif ins.mnemonic == 'add':
            parts = [p.strip() for p in ins.op_str.split(',')]
            dst = parts[0]
            src = parts[1]
            shift = 0
            if len(parts) >= 4 and 'lsl' in parts[3]:
                shift = parse_imm(parts[3].split('#')[1])
            
            if src in regs and isinstance(regs[src], int) and len(parts) >= 3 and '#' in parts[2]:
                imm = parse_imm(parts[2].split('#')[1]) << shift
                full_addr = regs[src] + imm
                regs[dst] = full_addr
                s = read_string(full_addr)
                if s and s.startswith('car_setting_'):
                    regs_meta[dst + '_str'] = (s, hex(ins.address), f"add {ins.op_str}")
            elif src == 'sp' and len(parts) >= 3 and '#' in parts[2]:
                imm = parse_imm(parts[2].split('#')[1]) << shift
                regs[dst] = ('sp', imm)
            elif src in regs and isinstance(regs[src], tuple) and regs[src][0] == 'sp' and len(parts) >= 3 and '#' in parts[2]:
                imm = parse_imm(parts[2].split('#')[1]) << shift
                regs[dst] = ('sp', regs[src][1] + imm)
        # 3. ldr
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
        # 4. mov / movz
        elif ins.mnemonic in ('mov', 'movz'):
            parts = [p.strip() for p in ins.op_str.split(',')]
            dst = parts[0]
            if len(parts) >= 2 and '#' in parts[1]:
                val = parse_imm(parts[1].split('#')[1])
                regs[dst] = val
                regs_meta[dst] = (val, hex(ins.address), ins.op_str)
        # 5. str / strh / strb
        elif ins.mnemonic in ('str', 'strh', 'strb'):
            parts = [p.strip() for p in ins.op_str.split(',')]
            src = parts[0]
            m_sp = re.search(r'\[\s*([a-zA-Z0-9]+)(?:,\s*#([0-9a-fx]+))?\s*\]', ins.op_str)
            if m_sp:
                base_reg = m_sp.group(1)
                offset = parse_imm(m_sp.group(2)) if m_sp.group(2) else 0
                target_sp_off = None
                if base_reg == 'sp':
                    target_sp_off = offset
                elif base_reg in regs and isinstance(regs[base_reg], tuple) and regs[base_reg][0] == 'sp':
                    target_sp_off = regs[base_reg][1] + offset
                
                if target_sp_off is not None:
                    if src in ('wzr', 'xzr'):
                        stack_slots[target_sp_off] = (0, hex(ins.address), "wzr")
                    elif src in regs and isinstance(regs[src], int):
                        stack_slots[target_sp_off] = (regs[src], hex(ins.address), f"{ins.mnemonic} {src} -> {regs[src]}")
        # 6. stp
        elif ins.mnemonic == 'stp':
            parts = [p.strip() for p in ins.op_str.split(',')]
            src1 = parts[0]
            src2 = parts[1]
            m_sp = re.search(r'\[\s*([a-zA-Z0-9]+)(?:,\s*#([0-9a-fx]+))?\s*\]', ins.op_str)
            if m_sp:
                base_reg = m_sp.group(1)
                offset = parse_imm(m_sp.group(2)) if m_sp.group(2) else 0
                target_sp_off = None
                if base_reg == 'sp':
                    target_sp_off = offset
                elif base_reg in regs and isinstance(regs[base_reg], tuple) and regs[base_reg][0] == 'sp':
                    target_sp_off = regs[base_reg][1] + offset
                
                if target_sp_off is not None:
                    if src1 in ('wzr', 'xzr'): stack_slots[target_sp_off] = (0, hex(ins.address), "wzr")
                    elif src1 in regs and isinstance(regs[src1], int): stack_slots[target_sp_off] = (regs[src1], hex(ins.address), f"str {src1}")
                    if src2 in ('wzr', 'xzr'): stack_slots[target_sp_off+4] = (0, hex(ins.address), "wzr")
                    elif src2 in regs and isinstance(regs[src2], int): stack_slots[target_sp_off+4] = (regs[src2], hex(ins.address), f"str {src2}")
        # 7. bl (factory call)
        elif ins.mnemonic == 'bl':
            target_str = ins.op_str.strip()
            target_addr = parse_imm(target_str.replace("#", ""))
            
            # Check if any car_setting string is active in regs_meta
            setting_info = None
            setting_reg = None
            for r in ['x6_str', 'x5_str', 'x7_str', 'x4_str', 'x1_str', 'x2_str', 'x3_str']:
                if r in regs_meta and regs_meta[r][0].startswith('car_setting_'):
                    setting_info = regs_meta[r]
                    setting_reg = r
                    break
            
            if setting_info:
                key, key_callsite, key_stmt = setting_info
                cls = factory_classes.get(target_addr, "UnknownVagSettingClass")

                ecu_info = None
                wl_info = None
                interp_info = None

                for r in ['x1_sym', 'x2_sym', 'x3_sym', 'x4_sym', 'x7_sym']:
                    if r in regs_meta:
                        s_name = regs_meta[r][0]
                        if "Ecu" in s_name:
                            ecu_info = regs_meta[r]
                        elif "Whitelist" in s_name:
                            wl_info = regs_meta[r]
                        elif "Interpretation" in s_name:
                            interp_info = regs_meta[r]

                # Resolve stack-passed arguments (DID, byte_offset, bit_mask)
                # In factory calls, pointers are passed in x3, x4, x5
                stack_args = []
                for r in ['x3', 'x4', 'x5', 'x6']:
                    if r in regs and isinstance(regs[r], tuple) and regs[r][0] == 'sp':
                        sp_off = regs[r][1]
                        if sp_off in stack_slots:
                            stack_args.append(stack_slots[sp_off][0])
                        else:
                            stack_args.append(None)

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
                    "stack_args": stack_args,
                    "w8": regs_meta.get('w8'),
                    "w9": regs_meta.get('w9')
                })

                del regs_meta[setting_reg]

    print(f"[+] Extracted {len(extracted)} settings from VagCanSettingsBanned.")
    out_path = os.path.join(base_dir, "research", "molecular", "banned_asm_extracted_settings.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=2)
    print(f"[+] Wrote {out_path}")

    # Inspect sample
    for e in extracted[:10]:
        ecu = e['ecu']['name'] if e['ecu'] else 'None'
        print(f"{e['asm_address']} | {e['setting_key']:40s} | {e['concrete_class']:25s} | ECU={ecu} | stack_args={e['stack_args']}")

if __name__ == '__main__':
    extract_banned_asm()
