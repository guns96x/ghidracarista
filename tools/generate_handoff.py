import os
import json

HANDOFF_DIR = r"d:\ghidracarista\handoff"

def main():
    os.makedirs(HANDOFF_DIR, exist_ok=True)
    print("Generating Handoff artifacts for ChatGPT in handoff/...")

    # 1. VERIFIED_COMMANDS.json (ONLY VERIFIED & CORROBORATED)
    verified_commands = {
        "metadata": {
            "target": "Independent Clean-Room Android VAG Diagnostic Stack",
            "date": "2026-09-24",
            "source_binary": "libCarista.so (ELF 64-bit ARMv8, SHA256: fe6708565270f20c...)",
            "decompiled_source": "libCarista.so.c (1,408,085 lines Ghidra export)",
            "classes_dex": "classes.dex & classes2.dex"
        },
        "transport": {
            "rfcomm_spp_uuid": "00001101-0000-1000-8000-00805F9B34FB",
            "client_config_descriptor_uuid": "00002902-0000-1000-8000-00805f9b34fb",
            "command_delimiter": "\\r",
            "prompt_char": ">",
            "elm_init_sequence": [
                {"cmd": "AT Z", "expect": "ELM327", "notes": "Microcontroller reset"},
                {"cmd": "AT E0", "expect": "OK", "notes": "Echo off"},
                {"cmd": "AT L0", "expect": "OK", "notes": "Linefeeds off"},
                {"cmd": "AT S0", "expect": "OK", "notes": "Spaces off"},
                {"cmd": "AT H1", "expect": "OK", "notes": "Headers on"},
                {"cmd": "AT SP 6", "expect": "OK", "notes": "Set ISO 15765-4 11-bit 500k CAN"}
            ]
        },
        "ecu_addressing_rules": {
            "can_11bit": {
                "rule": "if (TX >= 0x795) RX = TX + 8 else RX = TX + 0x6A",
                "evidence": "libCarista.so.c line 584009-584012 (VagUdsEcu constructor)"
            },
            "can_29bit": {
                "rule": "RX = TX + 0x00020000",
                "evidence": "libCarista.so.c line 583921 (VagUdsEcu 29-bit constructor)"
            },
            "tp20_logical": {
                "rule": "Channel Setup CAN ID = 0x200 + LogicalAddress",
                "evidence": "libCarista.so.c line 455618 (VagCanEcu::initialize)"
            }
        },
        "verified_ecus": [
            {"vag_id": "0x01", "name": "ENGINE", "tx": "0x7E0", "rx": "0x7E8", "tx_29bit": "0x17FC0076", "rx_29bit": "0x17FE0076", "tp20_setup": "0x201"},
            {"vag_id": "0x02", "name": "TRANSMISSION", "tx": "0x7E1", "rx": "0x7E9", "tx_29bit": "0x17FC0077", "rx_29bit": "0x17FE0077", "tp20_setup": "0x202"},
            {"vag_id": "0x03", "name": "ABS", "tx": "0x713", "rx": "0x77D", "tp20_setup": "0x203"},
            {"vag_id": "0x08", "name": "HVAC", "tx": "0x746", "rx": "0x7B0", "tp20_setup": "0x208"},
            {"vag_id": "0x09", "name": "CENTRAL_ELEC", "tx": "0x70E", "rx": "0x778", "tp20_setup": "0x209"},
            {"vag_id": "0x15", "name": "AIRBAG", "tx": "0x715", "rx": "0x77F", "tp20_setup": "0x215"},
            {"vag_id": "0x17", "name": "INSTRUMENT_CLUSTER", "tx": "0x714", "rx": "0x77E", "tp20_setup": "0x217"},
            {"vag_id": "0x19", "name": "CAN_GATEWAY", "tx": "0x710", "rx": "0x77A", "tp20_setup": "0x21F"},
            {"vag_id": "0x53", "name": "PARKING_BRAKE", "tx": "0x752", "rx": "0x7BC", "tp20_setup": "0x219"},
            {"vag_id": "0x5F", "name": "INFOTAINMENT", "tx": "0x773", "rx": "0x7DD", "tp20_setup": "0x25F"}
        ],
        "discovery_commands": [
            {
                "protocol": "UDS",
                "target_ecu": "CAN_GATEWAY (0x710)",
                "request_hex": "2204A1",
                "response_prefix": "6204A1",
                "record_length": 4,
                "installed_condition": "record[2] != 0",
                "active_bit": "bit 2 of record[2]",
                "evidence": "libCarista.so.c line 107137"
            },
            {
                "protocol": "TP2.0",
                "target_ecu": "CAN_GATEWAY (0x21F)",
                "request_hex": "1A9F",
                "response_prefix": "5A9F",
                "evidence": "libCarista.so.c line 100945"
            }
        ],
        "dtc_commands": [
            {
                "protocol": "UDS",
                "operation": "read_dtc",
                "request_hex": "19028D",
                "response_prefix": "5902",
                "record_length": 4,
                "dtc_bytes": 3,
                "status_byte": 1,
                "evidence": "libCarista.so.c line 108450"
            },
            {
                "protocol": "TP2.0",
                "operation": "read_dtc",
                "request_hex": "1802FF00",
                "response_prefix": "58",
                "evidence": "libCarista.so.c line 102841"
            },
            {
                "protocol": "UDS",
                "operation": "clear_dtc",
                "request_hex": "14FFFFFF",
                "response_prefix": "54",
                "evidence": "ISO 14229 / libCarista.so"
            }
        ],
        "service_routines": [
            {
                "operation": "epb_open",
                "ecu": "PARKING_BRAKE (0x752)",
                "request_hex": "310103A1",
                "response_prefix": "710103A1",
                "evidence": "libCarista.so.c line 111280"
            },
            {
                "operation": "epb_open_stop",
                "ecu": "PARKING_BRAKE (0x752)",
                "request_hex": "310203A1",
                "response_prefix": "710203A1",
                "evidence": "libCarista.so.c line 111400"
            },
            {
                "operation": "epb_close",
                "ecu": "PARKING_BRAKE (0x752)",
                "request_hex": "310103A0",
                "response_prefix": "710103A0",
                "evidence": "libCarista.so.c line 111212"
            },
            {
                "operation": "epb_close_stop",
                "ecu": "PARKING_BRAKE (0x752)",
                "request_hex": "310203A0",
                "response_prefix": "710203A0",
                "evidence": "libCarista.so.c line 111351"
            },
            {
                "operation": "routine_status_query",
                "request_hex": "220102",
                "response_prefix": "620102",
                "status_mapping": {
                    "0x00": "NONE",
                    "0x10": "SUCCEEDED",
                    "0x40": "FAILED_ABORTED_SAFETY",
                    "0x60": "FAILED_CONDITIONS_INCORRECT",
                    "0x80": "TIMEOUT",
                    "0xC0": "IN_PROGRESS"
                },
                "evidence": "libCarista.so.c line 110955"
            },
            {
                "operation": "dpf_regen_stationary",
                "ecu": "ENGINE (0x7E0)",
                "request_hex": "3101053D040000",
                "response_prefix": "7101053D",
                "evidence": "libCarista.so.c line 111143"
            },
            {
                "operation": "dpf_regen_driving",
                "ecu": "ENGINE (0x7E0)",
                "request_hex": "31010305040000",
                "response_prefix": "71010305",
                "evidence": "libCarista.so.c line 111145"
            }
        ],
        "identification_dids": [
            {"did": "0xF190", "name": "VIN", "request_hex": "22F190", "response_prefix": "62F190", "type": "ASCII_17"},
            {"did": "0xF187", "name": "PART_NUMBER", "request_hex": "22F187", "response_prefix": "62F187", "type": "ASCII"},
            {"did": "0xF189", "name": "SW_VERSION", "request_hex": "22F189", "response_prefix": "62F189", "type": "ASCII_4"},
            {"did": "0xF191", "name": "HW_VERSION", "request_hex": "22F191", "response_prefix": "62F191", "type": "ASCII"},
            {"did": "0xF18C", "name": "SERIAL_NUMBER", "request_hex": "22F18C", "response_prefix": "62F18C", "type": "ASCII"},
            {"did": "0xF19E", "name": "ASAM_ODX_FILE_ID", "request_hex": "22F19E", "response_prefix": "62F19E", "type": "ASCII"},
            {"did": "0xF1A2", "name": "ASAM_ODX_FILE_VER", "request_hex": "22F1A2", "response_prefix": "62F1A2", "type": "ASCII"},
            {"did": "0xF197", "name": "SYSTEM_COMPONENT_NAME", "request_hex": "22F197", "response_prefix": "62F197", "type": "ASCII"},
            {"did": "0xF1A5", "name": "WORKSHOP_CODE", "request_hex": "22F1A5", "response_prefix": "62F1A5", "type": "BYTES"},
            {"did": "0x0608", "name": "SLAVE_SUBMODULE_IDS", "request_hex": "220608", "response_prefix": "620608", "type": "BYTES"}
        ]
    }

    with open(os.path.join(HANDOFF_DIR, "VERIFIED_COMMANDS.json"), "w", encoding="utf-8") as f:
        json.dump(verified_commands, f, indent=2)
    print(f"Saved {os.path.join(HANDOFF_DIR, 'VERIFIED_COMMANDS.json')}")

    # 2. IMPLEMENTATION_BRIEF.md
    with open(os.path.join(HANDOFF_DIR, "IMPLEMENTATION_BRIEF.md"), "w", encoding="utf-8") as f:
        f.write("""# Implementation Brief for Android Diagnostic Stack Development

> **Target Audience:** ChatGPT / Android Software Engineers  
> **Mission:** Implement an independent, clean-room Android diagnostic application for VAG vehicles (VW, Audi, Škoda, SEAT).  
> **Source Evidence Base:** `research/db/diagnostic_evidence.json` & `handoff/VERIFIED_COMMANDS.json`  

---

## 1. What is VERIFIED
All data marked `VERIFIED` has exact function addresses, constant byte strings, and decompiled references in `libCarista.so`:
1. **CAN ID Derivation Rules**:
   - 11-bit standard: If `TX >= 0x795` then `RX = TX + 8`; if `TX < 0x795` then `RX = TX + 0x6A`.
   - 29-bit extended (MLB/Audi): `RX = TX + 0x00020000` (e.g. Engine `0x17FC0076` -> `0x17FE0076`).
   - TP2.0 channel setup: `Setup CAN ID = 0x200 + LogicalAddress` (Gateway = `0x21F`).
2. **ECU Discovery**:
   - Gateway UDS DID `0x04A1` (`22 04 A1`): Returns 4-byte records. Byte 0 is VAG ID, Byte 2 indicates installation status (`byte2 != 0` and bit 2 active).
   - Gateway TP2.0 Record `0x9F` (`1A 9F`).
3. **DTC Diagnostic Fault Reading**:
   - UDS: Service `19 02 8D` (mask `0x8D`: testFailed, pending, confirmed, warning indicator). Each DTC is 4 bytes (3 bytes DTC code, 1 byte status).
   - TP2.0: Service `18 02 FF 00` (All DTCs) and `18 00 FF 00` (Powertrain).
   - Clear DTC: `14 FF FF FF`.
4. **Service Routines**:
   - EPB Open (Service mode): `31 01 03 A1` (Routine ID `0x03A1`, target ECU `0x53` / TX `0x752`).
   - EPB Close: `31 01 03 A0` (Routine ID `0x03A0`).
   - DPF Standing Regen: `31 01 05 3D 04 00 00` (Routine ID `0x053D`, target ECU `0x01` / TX `0x7E0`).
   - DPF Driving Regen: `31 01 03 05 04 00 00` (Routine ID `0x0305`).
   - Routine Status Polling: DID `0x0102` (`22 01 02`). Status byte `>> 4`: `0x1` = Succeeded, `0xC` = In Progress, `0x4`/`0x6`/`0x8` = Error.
5. **Identification DIDs**:
   - VIN: `0xF190` (`22 F1 90`)
   - VAG Part Number: `0xF187` (`22 F1 87`)
   - Software Version: `0xF189` (`22 F1 89`)
   - Software Revision: `0xF1A2` (`22 F1 A2`)
   - Serial Number: `0xF18C` (`22 F1 8C`)
   - ASAM/ODX File ID: `0xF19E` (`22 F1 9E`)
   - Workshop Code: `0xF1A5` (`22 F1 A5`)
   - Slave Submodules: `0x0608` (`22 06 08`)

---

## 2. What is CORROBORATED
- **ELM327 Standard Init Flow**: `AT Z` -> `AT E0` -> `AT L0` -> `AT S0` -> `AT H1` -> `AT SP 6`.
- **Tester Present Heartbeat**: `3E 80` transmitted every 2,000 ms to maintain extended session (`10 03`).
- **ISO-TP Flow Control**: `30 00 00 00 00 00 00 00` (CTS, Block Size 0, STmin 0).

---

## 3. What Remains UNKNOWN / HYPOTHESIS
- **Cluster Oil Reset DIDs on MQB-evo**: Requires validation against specific cluster part numbers.
- **SFD Token Generation**: SFD online signing requires OEM server keys. The stack must detect SFD locks (`NRC 0x33`) and notify the user rather than attempt offline synthesis.

---

## 4. Transport API Architecture
```kotlin
interface TransportConnection {
    suspend fun open(address: String): Boolean
    suspend fun sendCommand(rawAscii: String, timeoutMs: Long = 5000): String
    suspend fun close()
    val isConnected: Boolean
}
```

---

## 5. Protocol API Architecture
```kotlin
interface DiagnosticCommunicator {
    suspend fun connect(adapterType: AdapterType): Boolean
    suspend fun queryGatewayEcuList(): List<DiscoveredEcu>
    suspend fun selectEcu(ecu: VagEcu)
    suspend fun enterSession(sessionType: Byte): Boolean
    suspend fun readDtcs(): List<FaultCode>
    suspend fun clearDtcs(): Boolean
    suspend fun readDid(didHex: String): ByteArray?
    suspend fun writeDid(didHex: String, data: ByteArray): Boolean
    suspend fun startRoutine(routineId: Int, optionRecord: ByteArray = byteArrayOf()): Boolean
    suspend fun stopRoutine(routineId: Int): Boolean
    suspend fun pollRoutineStatus(): RoutineStatus
}
```

---

## 6. Safety & Prerequisite Requirements
1. **Never perform write or routine operations in Default Session (`10 01`)**. Always transition to Extended Session (`10 03`) and run `TesterPresent` keepalive.
2. **Prior to EPB Caliper Retraction**:
   - Vehicle must be stationary (speed = 0).
   - Handbrake switch disengaged.
   - Ignition ON, Engine OFF.
   - Check no active hydraulic fault codes exist in ABS (`0x03`) or EPB (`0x53`).
3. **Prior to DPF Regeneration**:
   - Engine coolant temperature > 70 °C.
   - Minimum fuel level > 1/4 tank.
   - Hood closed, transmission in Park / Neutral.

---

## 7. Exact Paths to Evidence Artifacts
- **Symbol Index**: `research/ghidra_export/symbols_vag.json`
- **Class & Command Evidence**: `research/ghidra_export/commands_evidence.json`
- **Evidence Database**: `research/db/diagnostic_evidence.json` & `.csv`
- **ECU Addressing Database**: `research/db/vag_ecus.json`
- **State Machine Diagrams**: `research/state_machines/`
- **Audit Findings**: `research/SPEC_AUDIT.md` & `research/unverified_claims.md`
""")

    # 3. OPEN_QUESTIONS.md
    with open(os.path.join(HANDOFF_DIR, "OPEN_QUESTIONS.md"), "w", encoding="utf-8") as f:
        f.write("""# Open Questions & Investigation Log for Next AI Stage

1. **CAN-FD Transport Support on Low-Cost Adapters**:
   - Standard ELM327 does not support CAN-FD (required for some MQB-evo diagnostics).
   - Recommendation: Require vLinker FD / MC+ or OBDLink EX for full MQB-evo access, while falling back to 500k classical CAN on PQ35/MQB.

2. **Submodule LIN Slave Coding**:
   - Slaves (Wiper motor, Rain/Light sensor) on PQ35 are coded via BCM Master (`3B 9A <SubId> <Coding>`). On MQB, slaves are coded via DID `0x0608` / `0x0609`.
   - Need empirical validation on live vehicle for MQB LIN slave write framing.

3. **Battery Registration DID Variants**:
   - Gateway (`0x19`) Battery Adaptation uses DID `0x2A1B` (Serial), `0x2A1C` (Vendor), `0x2A1D` (Capacity) on MQB, whereas older platforms used channel adaptation.
   - Recommended: Implement both channel and DID adaptation paths based on ECU software level.
""")

    print(f"Generated all handoff files in {HANDOFF_DIR}.")

if __name__ == "__main__":
    main()
