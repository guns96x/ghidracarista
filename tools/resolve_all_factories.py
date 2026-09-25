import re
import json
import capstone
from elftools.elf.elffile import ELFFile

def map_factories():
    so_path = 'extracted/arm64/lib/arm64-v8a/libCarista.so'
    with open(so_path, 'rb') as f:
        elf = ELFFile(f)
        
        plt_sec = elf.get_section_by_name('.plt')
        rela_plt = elf.get_section_by_name('.rela.plt')
        symtab = elf.get_section(rela_plt['sh_link'])
        
        got_to_sym = {}
        for rel in rela_plt.iter_relocations():
            got_addr = rel['r_offset']
            sym = symtab.get_symbol(rel['r_info_sym'])
            got_to_sym[got_addr] = sym.name

        f.seek(plt_sec['sh_addr'])
        plt_code = f.read(plt_sec['sh_size'])
        cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
        
        plt_to_class = {}
        instructions = list(cs.disasm(plt_code, plt_sec['sh_addr']))
        for i in range(len(instructions) - 3):
            ins0, ins1, ins2, ins3 = instructions[i:i+4]
            if ins0.mnemonic == 'adrp' and ins1.mnemonic == 'ldr' and ins3.mnemonic == 'br':
                m_page = re.search(r'#(0x[0-9a-fA-F]+|\d+)', ins0.op_str)
                m_off = re.search(r'#(0x[0-9a-fA-F]+|\d+)', ins1.op_str)
                if m_page and m_off:
                    page = int(m_page.group(1), 0)
                    off = int(m_off.group(1), 0)
                    got_addr = page + off
                    if got_addr in got_to_sym:
                        sym_name = got_to_sym[got_addr]
                        m = re.search(r'__shared_ptr_emplaceI([0-9A-Za-z_]+)', sym_name)
                        if m:
                            cls = re.sub(r'^[0-9]+', '', m.group(1)).split('NS_')[0]
                            plt_to_class[ins0.address] = (cls, sym_name)

        print(f"Mapped {len(plt_to_class)} PLT entries to Setting classes.")

        # Now, check any function in .text: if it calls a PLT entry that is a Setting class, map it!
        # Read text section from 0x1400000 to 0x1600000 (where all setting factories live)
        text_sec = elf.get_section_by_name('.text')
        f.seek(0x1470000)
        text_chunk = f.read(0x1600000 - 0x1470000)
        
        text_ins = list(cs.disasm(text_chunk, 0x1470000))
        # Find functions that call these PLT entries
        func_to_class = {}
        curr_func = None
        for ins in text_ins:
            # function prologue
            if ins.mnemonic == 'stp' and 'x29, x30, [sp' in ins.op_str:
                curr_func = ins.address
            elif ins.mnemonic == 'bl':
                m_tgt = re.search(r'#(0x[0-9a-fA-F]+|\d+)', ins.op_str)
                if m_tgt:
                    tgt = int(m_tgt.group(1), 0)
                    if tgt in plt_to_class and curr_func:
                        func_to_class[curr_func] = plt_to_class[tgt][0]

        print(f"Mapped {len(func_to_class)} helper factories in .text to Setting classes!")
        
        # Merge both
        all_factories = {}
        for addr, (cls, _) in plt_to_class.items():
            all_factories[addr] = cls
        for addr, cls in func_to_class.items():
            all_factories[addr] = cls

        print(f"Total factory addresses resolved: {len(all_factories)}")
        
        # Save to JSON
        out_path = 'research/molecular/resolved_factories_map.json'
        with open(out_path, 'w', encoding='utf-8') as f_out:
            json.dump({hex(k): v for k, v in all_factories.items()}, f_out, indent=2)
        print(f"Saved to {out_path}")

if __name__ == '__main__':
    map_factories()
