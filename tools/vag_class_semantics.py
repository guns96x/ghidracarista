"""Constructor semantics of the VAG setting classes (shared by the extractor and the model).

Evidence is the base-constructor call inside each class constructor in libCarista.so.c.
Classes absent from this table have UNVERIFIED semantics and can never be EXACT.
"""

# VagSetting::VagSetting(wl, Type, Ecu*, uint16 id, int pos, vector<u8> mask, name, interp, ...)
# VagCanCodingSetting::VagCanCodingSetting(wl, Type, VagCanEcu*, 0, int pos, vector<u8> mask, ...)
# Evidence: base-constructor calls inside each class constructor in libCarista.so.c.
CLASS_SEMANTICS = {
    "VagUdsCodingSetting": {
        "vag_setting_type": 8, "fixed_id": 0x600, "int_roles": ["byte_position", "mask"],
        "evidence": "VagUdsCodingSetting::VagUdsCodingSetting -> VagSetting(wl, 8, ecu, 0x600, param_3, mask...) (libCarista.so.c ~582994-583168)",
    },
    "VagUdsAdaptationSetting": {
        "vag_setting_type": 7, "fixed_id": None, "int_roles": ["did", "byte_position", "mask"],
        "evidence": "VagUdsAdaptationSetting(VagUdsEcu*, wl, uint16, int, uint8, ...) -> VagSetting(wl, 7, ecu, did, pos, mask...) (libCarista.so.c ~578472-578760)",
    },
    "VagCanShortAdaptationSetting": {
        "vag_setting_type": 0, "fixed_id": None, "int_roles": ["channel", "byte_position", "mask"],
        "evidence": "VagCanShortAdaptationSetting(VagCanEcu*, wl, uint8, int, uint8, ...) -> VagSetting(wl, 0, ecu, channel, pos, mask...) (libCarista.so.c ~528460-528760)",
    },
    "VagCanLongAdaptationSetting": {
        "vag_setting_type": 1, "fixed_id": None, "int_roles": ["channel", "byte_position", "mask"],
        "evidence": "VagCanLongAdaptationSetting -> VagSetting(wl, 1, ecu, channel, pos, mask...)",
    },
    "VagCanLongCodingSetting": {
        "vag_setting_type": 3, "fixed_id": 0, "int_roles": ["byte_position", "mask"],
        "evidence": "VagCanLongCodingSetting(VagCanEcu*, wl, int, vector<u8>, ...) -> VagCanCodingSetting(wl, 3, ecu, 0, pos, mask...) (libCarista.so.c ~460734)",
    },
    "VagCanShortCodingSetting": {
        "vag_setting_type": 2, "fixed_id": 0, "int_roles": ["byte_position", "mask"],
        "evidence": "VagCanShortCodingSetting(VagCanEcu*, wl, int, vector<u8>, ...) -> VagCanCodingSetting(wl, 2, ecu, 0, pos, mask...) (libCarista.so.c ~528900)",
    },
}
