import re
import json

def extract_precise():
    with open("libCarista.so.c", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # Pre-map all factory functions to their class names
    factory_classes = {}
    def_pattern = re.compile(r'^(?:void|undefined[0-9* ]+)\s+(FUN_015[0-9a-f]{5})\(')
    for idx, line in enumerate(lines):
        m = def_pattern.match(line)
        if m:
            fun = m.group(1)
            def_chunk = "".join(lines[idx:idx+45])
            m_class = re.search(r'__shared_ptr_emplaceI([0-9A-Za-z_]+)', def_chunk)
            direct_class = re.search(r'([A-Za-z0-9_]+Setting) \*this', def_chunk)
            direct_class2 = re.search(r'([A-Za-z0-9_]+Setting)::\1', def_chunk)
            
            cls = None
            if m_class:
                cls = re.sub(r'^[0-9]+', '', m_class.group(1))
                if "NS_" in cls:
                    cls = cls.split("NS_")[0]
            elif direct_class:
                cls = direct_class.group(1)
            elif direct_class2:
                cls = direct_class2.group(1)
            if cls:
                factory_classes[fun] = cls

    print(f"Total factory classes mapped: {len(factory_classes)}")

    var_values = {}
    extracted_settings = []
    assign_pattern = re.compile(r'^\s*([a-zA-Z0-9_]+)(?:\[[0-9]+\])?\s*=\s*([^;]+);')
    
    start_line = 519330
    end_line = 538700

    i = start_line
    while i < end_line:
        line = lines[i]
        lno = i + 1
        
        # Check variable assignment
        m_assign = assign_pattern.match(line)
        if m_assign:
            var_name = m_assign.group(1)
            val_str = m_assign.group(2).strip()
            val = None
            if val_str.startswith("0x") or val_str.startswith("-0x"):
                try:
                    val = int(val_str, 16)
                except ValueError:
                    val = val_str
            elif val_str.isdigit() or (val_str.startswith("-") and val_str[1:].isdigit()):
                val = int(val_str)
            elif val_str.startswith('"') and val_str.endswith('"'):
                val = val_str.strip('"')
            else:
                val = val_str
            var_values[var_name] = (val, lno)

        # Check if line starts a FUN_015 call or Setting call
        if re.search(r'FUN_015[0-9a-f]{5}\(', line) or "Setting::" in line:
            # Buffer until semicolon
            call_lines = [line.strip()]
            call_start_lno = lno
            j = i
            while ";" not in lines[j] and j < min(len(lines), i + 15):
                j += 1
                call_lines.append(lines[j].strip())
            
            call_text = " ".join(call_lines)
            
            if "car_setting_" in call_text:
                m_key = re.search(r'"(car_setting_[a-zA-Z0-9_]+)"', call_text)
                m_fun = re.search(r'(FUN_015[0-9a-f]{5})', call_text)
                
                if m_key and m_fun:
                    key = m_key.group(1)
                    fun = m_fun.group(1)
                    cls = factory_classes.get(fun, "UnknownSettingClass")
                    
                    m_ecu = re.search(r'&?(Vag(?:Uds|Can)Ecu::[A-Z0-9_]+)', call_text)
                    ecu_str = m_ecu.group(1) if m_ecu else None
                    
                    m_wl = re.search(r'&?(VagWhitelists::[A-Z0-9_]+)', call_text)
                    wl_str = m_wl.group(1) if m_wl else None
                    
                    m_interp = re.search(r'&?(MultipleChoiceInterpretation::[A-Z0-9_]+|NumericalInterpretation::[A-Z0-9_]+)', call_text)
                    interp_str = m_interp.group(1) if m_interp else None
                    
                    # Extract variables in argument list
                    inside_parens = call_text[call_text.find("(")+1:call_text.rfind(")")]
                    args = [a.strip() for a in inside_parens.split(",")]
                    
                    param_vars = []
                    for arg in args:
                        clean_arg = arg.replace("&", "").strip()
                        if "[" in clean_arg:
                            clean_arg = clean_arg.split("[")[0]
                        if clean_arg in var_values:
                            param_vars.append((clean_arg, var_values[clean_arg][0]))
                    
                    extracted_settings.append({
                        "line": call_start_lno,
                        "key": key,
                        "factory_function": fun,
                        "concrete_class": cls,
                        "ecu": ecu_str,
                        "whitelist": wl_str,
                        "interpretation": interp_str,
                        "resolved_vars": param_vars,
                        "call_snippet": call_text.strip()[:140]
                    })
            i = j
        i += 1

    print(f"Extracted {len(extracted_settings)} settings with full factory calls:")
    for s in extracted_settings[:25]:
        print(f"L{s['line']:6d} | {s['key']:45s} | {s['concrete_class']:25s} | {s['ecu']} | vars={s['resolved_vars']}")

    with open("research/molecular/extracted_vag_settings_raw.json", "w", encoding="utf-8") as f:
        json.dump(extracted_settings, f, indent=2)
    print("Saved to research/molecular/extracted_vag_settings_raw.json")

if __name__ == "__main__":
    extract_precise()
