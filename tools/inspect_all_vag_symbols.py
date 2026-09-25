from elftools.elf.elffile import ELFFile

def inspect():
    with open('extracted/arm64/lib/arm64-v8a/libCarista.so', 'rb') as f:
        elf = ELFFile(f)
        for sname in ['.symtab', '.dynsym']:
            sec = elf.get_section_by_name(sname)
            if sec:
                print(f"--- Symbols in {sname} ---")
                for sym in sec.iter_symbols():
                    if 'Vag' in sym.name and ('Setting' in sym.name or 'getSettings' in sym.name):
                        if 'FreezeFrame' not in sym.name:
                            print(f"{hex(sym['st_value']):10s} sz={sym['st_size']:6d} {sym.name}")

if __name__ == '__main__':
    inspect()
