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

def extract_settings_from_asm():
    with open('extracted/arm64/lib/arm64-v8a/libCarista.so', 'rb') as f:
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

        func_addr = 0x1402f68
        func_size = 502868
        f.seek(func_addr)
        code = f.read(func_size)

    print(f"Read {len(code)} bytes of ARM64 code for VagCanSettings::getSettings.")

    cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    cs.detail = True

    regs = {}
    found_settings = []
    
    instructions = list(cs.disasm(code, func_addr))
    print(f"Disassembled {len(instructions)} instructions.")

    for idx, ins in enumerate(instructions):
        if ins.mnemonic == 'adrp':
            reg = ins.op_str.split(',')[0].strip()
            imm = parse_imm(ins.op_str.split('#')[1])
            regs[reg] = imm
        elif ins.mnemonic == 'add':
            parts = [p.strip() for p in ins.op_str.split(',')]
            dst = parts[0]
            src = parts[1]
            if src in regs and len(parts) >= 3 and '#' in parts[2]:
                imm = parse_imm(parts[2].split('#')[1])
                full_addr = regs[src] + imm
                regs[dst] = full_addr
                s = read_string(full_addr)
                if s and s.startswith('car_setting_'):
                    regs[dst + '_str'] = s
        elif ins.mnemonic == 'mov':
            parts = [p.strip() for p in ins.op_str.split(',')]
            dst = parts[0]
            if len(parts) >= 2 and '#' in parts[1]:
                val = parse_imm(parts[1].split('#')[1])
                regs[dst] = val
        elif ins.mnemonic == 'bl':
            target = ins.op_str.strip()
            setting_key = None
            for r in ['x5_str', 'x6_str', 'x7_str', 'x4_str', 'x1_str', 'x2_str', 'x3_str']:
                if r in regs and regs[r].startswith('car_setting_'):
                    setting_key = regs[r]
                    break
            
            if setting_key:
                found_settings.append({
                    "asm_address": hex(ins.address),
                    "target": target,
                    "key": setting_key,
                    "w8": regs.get('w8'),
                    "w9": regs.get('w9'),
                    "w1": regs.get('w1'),
                    "w2": regs.get('w2')
                })
                for r in list(regs.keys()):
                    if r.endswith('_str'):
                        del regs[r]

    print(f"\nExtracted {len(found_settings)} settings from VagCanSettings::getSettings disassembly!")
    unique_keys = set(s['key'] for s in found_settings)
    print(f"Unique keys: {len(unique_keys)}")
    for s in found_settings[:25]:
        print(f"{s['asm_address']}: {s['key']} -> target {s['target']} (w8={s['w8']}, w9={s['w9']})")

if __name__ == '__main__':
    extract_settings_from_asm()
