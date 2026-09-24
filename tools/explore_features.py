#!/usr/bin/env python3
"""
Explore all car_setting_* and diagnostic features in libCarista.so.c, resources.arsc, and DEX.
"""

import re
import struct
import json

def parse_arsc_strings():
    with open(r'd:\ghidracarista\extracted\base\resources.arsc', 'rb') as f:
        data = f.read()

    def parse_string_pool(data, offset):
        chunk_type, chunk_hdr_size, chunk_size = struct.unpack('<HHI', data[offset:offset+8])
        string_count, style_count, flags, strings_start, styles_start = struct.unpack('<IIIII', data[offset+8:offset+28])
        is_utf8 = (flags & (1 << 8)) != 0
        offsets = struct.unpack(f'<{string_count}I', data[offset+28:offset+28+string_count*4])
        pool_base = offset + strings_start
        pool_strings = []
        for o in offsets:
            p = pool_base + o
            if is_utf8:
                u16_len = data[p]
                p += 1
                if u16_len & 0x80:
                    u16_len = ((u16_len & 0x7F) << 8) | data[p]
                    p += 1
                u8_len = data[p]
                p += 1
                if u8_len & 0x80:
                    u8_len = ((u8_len & 0x7F) << 8) | data[p]
                    p += 1
                s = data[p:p+u8_len].decode('utf-8', 'ignore')
                pool_strings.append(s)
            else:
                u16_len = struct.unpack('<H', data[p:p+2])[0]
                p += 2
                s = data[p:p+u16_len*2].decode('utf-16le', 'ignore')
                pool_strings.append(s)
        return pool_strings, offset + chunk_size

    global_strings, pkg_offset = parse_string_pool(data, 12)
    types, _ = parse_string_pool(data, pkg_offset + 288)
    keys, next_offset = parse_string_pool(data, pkg_offset + 744)

    string_type_id = types.index('string') + 1

    offset = next_offset
    key_to_string = {}
    while offset < len(data):
        chunk_type, chunk_hdr_sz, chunk_sz = struct.unpack('<HHI', data[offset:offset+8])
        if chunk_type == 0x0201: # RES_TABLE_TYPE_TYPE
            type_id, res0, res1, entry_count, entries_start = struct.unpack('<BBHI I', data[offset+8:offset+20])
            lang = data[offset+28:offset+30].decode('ascii', 'ignore').rstrip('\x00')
            country = data[offset+30:offset+32].decode('ascii', 'ignore').rstrip('\x00')
            locale = f'{lang}_{country}'.strip('_') or 'default'
            
            if type_id == string_type_id and locale == 'default':
                entry_offsets = struct.unpack(f'<{entry_count}i', data[offset+chunk_hdr_sz:offset+chunk_hdr_sz+entry_count*4])
                base = offset + entries_start
                for entry_idx, eo in enumerate(entry_offsets):
                    if eo != -1:
                        ep = base + eo
                        size, flags, key_idx = struct.unpack('<HHI', data[ep:ep+8])
                        if flags & 0x0001 == 0:
                            val_size, res0, val_type, val_data = struct.unpack('<HBBI', data[ep+8:ep+16])
                            if val_type == 0x03 and val_data < len(global_strings):
                                k = keys[key_idx]
                                v = global_strings[val_data]
                                key_to_string[k] = v
        offset += chunk_sz
        if chunk_sz == 0: break

    return key_to_string

def main():
    print('Parsing ARSC default strings...')
    key_to_string = parse_arsc_strings()
    print(f'Parsed {len(key_to_string)} strings from resources.arsc.')

    # Categories
    categories = {k: v for k, v in key_to_string.items() if 'category' in k}
    print(f'Found {len(categories)} category strings.')
    for k, v in sorted(categories.items())[:20]:
        print(f'  {k} -> {v}')

    # Settings
    car_settings = {k: v for k, v in key_to_string.items() if k.startswith('car_setting_') and 'category' not in k}
    print(f'Found {len(car_settings)} car_setting_* strings.')
    
    # Check C++ string references
    print('Reading libCarista.so.c...')
    with open(r'd:\ghidracarista\libCarista.so.c', 'r', encoding='utf-8', errors='ignore') as f:
        text_c = f.read()

    settings_in_c = set(re.findall(r'"(car_setting_[a-zA-Z0-9_]+)"', text_c))
    print(f'Found {len(settings_in_c)} setting strings directly in libCarista.so.c.')

    common_vals = {'car_setting_yes', 'car_setting_no', 'car_setting_enabled', 'car_setting_disabled', 'car_setting_on', 'car_setting_off', 'car_setting_open', 'car_setting_closed', 'car_setting_default', 'car_setting_none', 'car_setting_active', 'car_setting_inactive', 'car_setting_not_active', 'car_setting_installed', 'car_setting_not_installed', 'car_setting_auto', 'car_setting_manual'}
    real_features = [s for s in settings_in_c if s not in common_vals and not re.match(r'^car_setting_\d+$', s)]
    print(f'Distinct features verified in C++: {len(real_features)}')
    for rf in sorted(real_features)[:30]:
        label = key_to_string.get(rf, rf)
        print(f'  {rf} -> "{label}"')

if __name__ == '__main__':
    main()
