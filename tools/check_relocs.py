from elftools.elf.elffile import ELFFile

def check():
    with open('extracted/arm64/lib/arm64-v8a/libCarista.so', 'rb') as f:
        elf = ELFFile(f)
        for sec in elf.iter_sections():
            if sec['sh_addr'] <= 0x1ba7e58 < sec['sh_addr'] + sec['sh_size']:
                print(f"0x1ba7e58 is in section: {sec.name}")

        targets = {0x1ba7e58, 0x1ba7fd8, 0x1ba28e0}
        for sec in elf.iter_sections():
            if 'rela' in sec.name.lower():
                symtab = elf.get_section(sec['sh_link'])
                for rel in sec.iter_relocations():
                    if rel['r_offset'] in targets:
                        sym = symtab.get_symbol(rel['r_info_sym'])
                        print(f"Reloc at {hex(rel['r_offset'])}: symbol={sym.name}")

if __name__ == '__main__':
    check()
