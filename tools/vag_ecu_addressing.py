"""
tools/vag_ecu_addressing.py
Complete verified VAG ECU CAN Transport Map directly derived from:
- VagUdsEcu::initialize() (libCarista.so.c lines 583,306 - 583,550)
- VagCanEcu::initialize() (libCarista.so.c lines 455,613 - 455,750)
Strict rule:
CAN 11-bit rule: if (TX >= 0x7E0) RX = TX + 8 else RX = TX + 0x6A
Zero fallback to 0x70E/0x778 allowed!
"""

VAG_UDS_ECU_ADDRESSES = {
    "VagUdsEcu::CAN_GATEWAY": {"tx": "0x710", "rx": "0x77A", "logical": "0x19"},
    "VagUdsEcu::ENGINE": {"tx": "0x7E0", "rx": "0x7E8", "logical": "0x01"},
    "VagUdsEcu::ENGINE_2": {"tx": "0x7E2", "rx": "0x7EA", "logical": "0x11"},
    "VagUdsEcu::ENGINE_3_BATTERY_2": {"tx": "0x728", "rx": "0x792", "logical": "0x21"},
    "VagUdsEcu::ENGINE_29_BIT": {"tx": "0x17fc0076", "rx": "0x17fe0076", "logical": "0x01", "is_29bit": True},
    "VagUdsEcu::HIGH_BEAM_ASSIST": {"tx": "0x730", "rx": "0x79A", "logical": "0x20"},
    "VagUdsEcu::TRANSMISSION": {"tx": "0x7E1", "rx": "0x7E9", "logical": "0x02"},
    "VagUdsEcu::TRANSMISSION_29_BIT": {"tx": "0x17fc0077", "rx": "0x17fe0077", "logical": "0x02", "is_29bit": True},
    "VagUdsEcu::ELEC_DRIVE": {"tx": "0x7E6", "rx": "0x7EE", "logical": "0x51"},
    "VagUdsEcu::ABS": {"tx": "0x713", "rx": "0x77D", "logical": "0x03"},
    "VagUdsEcu::BRAKE_BOOSTER": {"tx": "0x73B", "rx": "0x7A5", "logical": "0x23"},
    "VagUdsEcu::PARKING_BRAKE": {"tx": "0x752", "rx": "0x7BC", "logical": "0x53"},
    "VagUdsEcu::STEERING_ASSIST": {"tx": "0x712", "rx": "0x77C", "logical": "0x44"},
    "VagUdsEcu::STEERING_ANGLE": {"tx": "0x751", "rx": "0x7BB", "logical": "0x04"},
    "VagUdsEcu::STEERING_ACTIVE": {"tx": "0x716", "rx": "0x780", "logical": "0x1B"},
    "VagUdsEcu::HVAC": {"tx": "0x746", "rx": "0x7B0", "logical": "0x08"},
    "VagUdsEcu::HVAC_REAR": {"tx": "0x71A", "rx": "0x784", "logical": "0x28"},
    "VagUdsEcu::AUX_HEAT": {"tx": "0x76A", "rx": "0x7D4", "logical": "0x18"},
    "VagUdsEcu::AIRBAG": {"tx": "0x715", "rx": "0x77F", "logical": "0x15"},
    "VagUdsEcu::SUSPENSION": {"tx": "0x772", "rx": "0x7DC", "logical": "0x14"},
    "VagUdsEcu::INSTRUMENT_CLUSTER": {"tx": "0x714", "rx": "0x77E", "logical": "0x17"},
    "VagUdsEcu::IMMOBILIZER": {"tx": "0x711", "rx": "0x77B", "logical": "0x25"},
    "VagUdsEcu::CENTRAL_ELEC": {"tx": "0x70E", "rx": "0x778", "logical": "0x09"},
    "VagUdsEcu::CENTRAL_CONVENIENCE": {"tx": "0x17fc008b", "rx": "0x17fe008b", "logical": "0x46", "is_29bit": True},
    "VagUdsEcu::XENON": {"tx": "0x754", "rx": "0x7BE", "logical": "0x55"},
    "VagUdsEcu::TIRE_PRESSURE": {"tx": "0x70B", "rx": "0x775", "logical": "0x65"},
    "VagUdsEcu::STEERING_WHEEL": {"tx": "0x70C", "rx": "0x776", "logical": "0x16"},
    "VagUdsEcu::DOOR_DRIVER": {"tx": "0x74A", "rx": "0x7B4", "logical": "0x42"},
    "VagUdsEcu::DOOR_PASSENGER": {"tx": "0x74B", "rx": "0x7B5", "logical": "0x52"},
    "VagUdsEcu::SLIDE_DOOR_REAR_LEFT": {"tx": "0x733", "rx": "0x79D", "logical": "0x0B"},
    "VagUdsEcu::SLIDE_DOOR_REAR_RIGHT": {"tx": "0x734", "rx": "0x79E", "logical": "0x0D"},
    "VagUdsEcu::SEAT_MEM_DRIVER": {"tx": "0x74C", "rx": "0x7B6", "logical": "0x36"},
    "VagUdsEcu::SEAT_MEM_PASSENGER": {"tx": "0x74D", "rx": "0x7B7", "logical": "0x06"},
    "VagUdsEcu::TRUNK": {"tx": "0x723", "rx": "0x78D", "logical": "0x6D"},
    "VagUdsEcu::DIFFERENTIAL_LOCKS": {"tx": "0x71E", "rx": "0x788", "logical": "0x22"},
    "VagUdsEcu::BATTERY_REGULATOR": {"tx": "0x17fc009c", "rx": "0x17fe009c", "logical": "0x61", "is_29bit": True},
    "VagUdsEcu::BATTERY_CHARGER": {"tx": "0x71D", "rx": "0x787", "logical": "0xC6"},
    "VagUdsEcu::LEVEL_CONTROL": {"tx": "0x755", "rx": "0x7BF", "logical": "0x34"},
    "VagUdsEcu::AWD": {"tx": "0x70F", "rx": "0x779", "logical": "0x22"},
    "VagUdsEcu::AUTO_DIST_REG": {"tx": "0x757", "rx": "0x7C1", "logical": "0x13"},
    "VagUdsEcu::CONVERTIBLE_ROOF": {"tx": "0x72D", "rx": "0x797", "logical": "0x26"},
    "VagUdsEcu::LANE_CHANGE": {"tx": "0x74E", "rx": "0x7B8", "logical": "0x3C"},
    "VagUdsEcu::BACK_UP_CAMERA": {"tx": "0x769", "rx": "0x7D3", "logical": "0x6C"},
    "VagUdsEcu::BACK_UP_CAMERA_2": {"tx": "0x6B8", "rx": "0x722", "logical": "0x6C"},
    "VagUdsEcu::IMAGE_PROCESSING": {"tx": "0x758", "rx": "0x7C2", "logical": "0xA5"},
    "VagUdsEcu::PARK_STEER_ASSIST": {"tx": "0x70A", "rx": "0x774", "logical": "0x10"},
    "VagUdsEcu::ACC_START_AUTH": {"tx": "0x732", "rx": "0x79C", "logical": "0x05"},
    "VagUdsEcu::NAVIGATION": {"tx": "0x76C", "rx": "0x7D6", "logical": "0x37"},
    "VagUdsEcu::SOUND_SYSTEM": {"tx": "0x76F", "rx": "0x7D9", "logical": "0x47"},
    "VagUdsEcu::MEDIA_PLAYER_1": {"tx": "0x770", "rx": "0x7DA", "logical": "0x0E"},
    "VagUdsEcu::TELEPHONE": {"tx": "0x76B", "rx": "0x7D5", "logical": "0x77"},
    "VagUdsEcu::CENTRAL_CONVENIENCE_2": {"tx": "0x745", "rx": "0x7AF", "logical": "0x46"},
    "VagUdsEcu::SPECIAL_FUNC": {"tx": "0x72C", "rx": "0x796", "logical": "0xD0"},
    "VagUdsEcu::SPECIAL_FUNC_2": {"tx": "0x72B", "rx": "0x795", "logical": "0xD1"},
    "VagUdsEcu::INFOTAINMENT": {"tx": "0x773", "rx": "0x7DD", "logical": "0x5F"},
    "VagUdsEcu::INFOTAINMENT_2": {"tx": "0x75A", "rx": "0x7C4", "logical": "0x5F"},
    "VagUdsEcu::TELEMATICS": {"tx": "0x767", "rx": "0x7D1", "logical": "0x75"},
    "VagUdsEcu::TV_TUNER": {"tx": "0x76D", "rx": "0x7D7", "logical": "0x57"},
    "VagUdsEcu::TRAILER": {"tx": "0x747", "rx": "0x7B1", "logical": "0x69"},
    "VagUdsEcu::THERMAL_MANAGEMENT": {"tx": "0x742", "rx": "0x7AC", "logical": "0x71"},
    "VagUdsEcu::STRUCTURE_BORNE_SOUND": {"tx": "0x71C", "rx": "0x786", "logical": "0xA9"},
    "VagUdsEcu::EXTERIOR_NOISE_ACTUATOR": {"tx": "0x764", "rx": "0x7CE", "logical": "0xC0"},
    "VagUdsEcu::FRONT_SENSOR_DRIVER_ASSIST": {"tx": "0x74F", "rx": "0x7B9", "logical": "0xA5"},
    "VagUdsEcu::REAR_AXLE_STEERING": {"tx": "0x760", "rx": "0x7CA", "logical": "0xCB"},
    "VagUdsEcu::REAR_AXLE_STEERING_2": {"tx": "0x761", "rx": "0x7CB", "logical": "0xCC"},
    "VagUdsEcu::STEERING_COLUMN_LOCK": {"tx": "0x731", "rx": "0x79B", "logical": "0x2B"},
    "VagUdsEcu::SPECIAL_VEHICLE_ASSIST": {"tx": "0x72F", "rx": "0x799", "logical": "0x3D"},
    "VagUdsEcu::SENSOR_ELEC": {"tx": "0x721", "rx": "0x78B", "logical": "0xCD"},
    "VagUdsEcu::AC_COMPRESSOR": {"tx": "0x719", "rx": "0x783", "logical": "0xBC"},
    "VagUdsEcu::GEAR_SHIFT": {"tx": "0x753", "rx": "0x7BD", "logical": "0x81"},
    "VagUdsEcu::HEADS_UP_DISPLAY": {"tx": "0x71B", "rx": "0x785", "logical": "0x82"},
    "VagUdsEcu::NIGHT_VISION": {"tx": "0x727", "rx": "0x791", "logical": "0x84"},
    "VagUdsEcu::ONBOARD_CAMERA": {"tx": "0x726", "rx": "0x790", "logical": "0x85"},
    "VagUdsEcu::SEAT_MULTICONT_DRIVER": {"tx": "0x735", "rx": "0x79F", "logical": "0x88"},
    "VagUdsEcu::MULTIFUNC_MODULE": {"tx": "0x17fc00a9", "rx": "0x17fe00a9", "logical": "0x4F", "is_29bit": True},
    "VagUdsEcu::SUNROOF": {"tx": "0x17fc0084", "rx": "0x17fe0084", "logical": "0xCA", "is_29bit": True},
    "VagUdsEcu::APPLICATION_SERVER_3_SYSTEM_1_INFOTAINMENT": {"tx": "0x18040008", "rx": "0x18060008", "logical": "0x81", "is_29bit": True}
}

# For VagCanEcu, KWP/TP2.0 logical addresses
VAG_CAN_ECU_ADDRESSES = {
    "VagCanEcu::ENGINE": {"logical": "0x01", "kwp_name": "Engine"},
    "VagCanEcu::TRANSMISSION": {"logical": "0x02", "kwp_name": "Auto Trans"},
    "VagCanEcu::ABS": {"logical": "0x03", "kwp_name": "ABS Brakes"},
    "VagCanEcu::STEERING_ANGLE": {"logical": "0x04", "kwp_name": "Steering Angle"},
    "VagCanEcu::ACC_START_AUTH": {"logical": "0x05", "kwp_name": "Acc/Start Auth."},
    "VagCanEcu::AIRBAG": {"logical": "0x15", "kwp_name": "Airbags"},
    "VagCanEcu::CONTROL_HEAD": {"logical": "0x07", "kwp_name": "Control Head"},
    "VagCanEcu::HVAC": {"logical": "0x08", "kwp_name": "Auto HVAC"},
    "VagCanEcu::CENTRAL_ELEC": {"logical": "0x09", "kwp_name": "Cent. Elect."},
    "VagCanEcu::PARK_STEER_ASSIST": {"logical": "0x10", "kwp_name": "Park/Steer Assist"},
    "VagCanEcu::AUTO_DIST_REG": {"logical": "0x13", "kwp_name": "Auto Dist. Reg"},
    "VagCanEcu::STEERING_WHEEL": {"logical": "0x16", "kwp_name": "Steering Wheel"},
    "VagCanEcu::INSTRUMENT_CLUSTER": {"logical": "0x17", "kwp_name": "Instruments"},
    "VagCanEcu::AUX_HEAT": {"logical": "0x18", "kwp_name": "Aux. Heat"},
    "VagCanEcu::CAN_GATEWAY": {"logical": "0x19", "kwp_name": "CAN Gateway"},
    "VagCanEcu::HIGH_BEAM_ASSIST": {"logical": "0x20", "kwp_name": "High Beam Assist"},
    "VagCanEcu::SEAT_MEM_DRIVER": {"logical": "0x36", "kwp_name": "Seat Mem. Driver"},
    "VagCanEcu::NAVIGATION": {"logical": "0x37", "kwp_name": "Navigation"},
    "VagCanEcu::DOOR_DRIVER": {"logical": "0x42", "kwp_name": "Door Elect. Driver"},
    "VagCanEcu::STEERING_ASSIST": {"logical": "0x44", "kwp_name": "Steering Assist"},
    "VagCanEcu::CENTRAL_CONVENIENCE": {"logical": "0x46", "kwp_name": "Central Conv."},
    "VagCanEcu::SOUND_SYSTEM": {"logical": "0x47", "kwp_name": "Sound System"},
    "VagCanEcu::CENTRAL_ELEC_2": {"logical": "0x4F", "kwp_name": "Cent. Elect. 2"},
    "VagCanEcu::DOOR_PASSENGER": {"logical": "0x52", "kwp_name": "Door Elect. Pass."},
    "VagCanEcu::PARKING_BRAKE": {"logical": "0x53", "kwp_name": "Parking Brake"},
    "VagCanEcu::XENON": {"logical": "0x55", "kwp_name": "Xenon Range"},
    "VagCanEcu::RADIO": {"logical": "0x56", "kwp_name": "Radio"},
    "VagCanEcu::INFOTAINMENT": {"logical": "0x5F", "kwp_name": "Information Electr."},
    "VagCanEcu::BATTERY_REGULATOR": {"logical": "0x61", "kwp_name": "Battery Regul."},
    "VagCanEcu::PARKING_ASSIST": {"logical": "0x76", "kwp_name": "Parking Assist"},
    "VagCanEcu::TELEPHONE": {"logical": "0x77", "kwp_name": "Telephone"}
}

def resolve_ecu_transport(ecu_name):
    """
    Returns exact physical and logical transport addresses.
    Never returns generic fallback 0x70E/0x778!
    """
    if not ecu_name:
        return None
    
    clean_name = ecu_name.replace("&", "").strip()
    
    if clean_name in VAG_UDS_ECU_ADDRESSES:
        info = VAG_UDS_ECU_ADDRESSES[clean_name]
        return {
            "name": clean_name.replace("VagUdsEcu::", ""),
            "full_name": clean_name,
            "protocol": "UDS (ISO 14229)",
            "logical_address": info["logical"],
            "uds_tx_id": info["tx"],
            "uds_rx_id": info["rx"],
            "is_29bit": info.get("is_29bit", False)
        }
    
    if clean_name in VAG_CAN_ECU_ADDRESSES:
        info = VAG_CAN_ECU_ADDRESSES[clean_name]
        # A VagCanEcu is a KWP2000/TP2.0 endpoint. A same-named VagUdsEcu having CAN IDs is not
        # evidence for this ECU, so no UDS TX/RX IDs are attached (Round 4, protocol consistency).
        return {
            "name": clean_name.replace("VagCanEcu::", ""),
            "full_name": clean_name,
            "protocol": "KWP2000 / TP2.0 / CAN",
            "logical_address": info["logical"],
            "uds_tx_id": None,
            "uds_rx_id": None,
            "tp20_channel": f"0x200 + {info['logical']}"
        }

    return None
