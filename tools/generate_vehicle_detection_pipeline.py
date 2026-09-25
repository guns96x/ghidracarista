#!/usr/bin/env python3
"""
tools/generate_vehicle_detection_pipeline.py
Produces:
- research/molecular/VEHICLE_DETECTION_PIPELINE.md
- research/molecular/ecu_identification_rules.json
"""

import os
import json

PIPELINE_RULES = {
    "metadata": {
        "title": "VAG Vehicle and ECU Identification Pipeline Rules",
        "date": "2026-09-25",
        "evidence_source": "libCarista.so.c lines 107100-108500 and 584000-584050"
    },
    "pipeline_stages": [
        {
            "stage_index": 1,
            "name": "ADAPTER_HANDSHAKE",
            "description": "Establish microcontroller state and configure bus filters",
            "commands": [
                {"cmd": "AT Z", "expect": "ELM327", "retry": 3},
                {"cmd": "AT E0", "expect": "OK"},
                {"cmd": "AT L0", "expect": "OK"},
                {"cmd": "AT S0", "expect": "OK"},
                {"cmd": "AT H1", "expect": "OK"},
                {"cmd": "AT SP 6", "expect": "OK", "desc": "ISO 15765-4 11-bit 500k CAN"}
            ]
        },
        {
            "stage_index": 2,
            "name": "VIN_ACQUISITION",
            "description": "Read 17-character VIN via standard OBD2 or UDS",
            "methods": [
                {
                    "protocol": "OBD2_BROADCAST",
                    "request": "09 02",
                    "target": "0x7DF",
                    "response_prefix": "49 02 01",
                    "format": "ASCII 17 bytes"
                },
                {
                    "protocol": "UDS_ENGINE",
                    "request": "22 F1 90",
                    "target": "0x7E0 (ENGINE)",
                    "response_prefix": "62 F1 90",
                    "format": "ASCII 17 bytes"
                },
                {
                    "protocol": "UDS_GATEWAY",
                    "request": "22 F1 90",
                    "target": "0x710 (CAN_GATEWAY)",
                    "response_prefix": "62 F1 90",
                    "format": "ASCII 17 bytes"
                }
            ],
            "vin_parsing": {
                "wmi": "bytes 0-2 (e.g. WVW = Volkswagen Germany, TMB = Skoda, VSS = SEAT, WAU = Audi)",
                "vds": "bytes 3-8 (Vehicle Descriptor Section)",
                "model_year_code": "byte 9 (char 10): 8=2008, 9=2009, A=2010, B=2011, C=2012, D=2013, E=2014, F=2015, G=2016, H=2017, J=2018, K=2019, L=2020, M=2021, N=2022, P=2023, R=2024",
                "plant": "byte 10 (char 11)",
                "serial": "bytes 11-16 (chars 12-17)"
            }
        },
        {
            "stage_index": 3,
            "name": "GATEWAY_DISCOVERY",
            "description": "Extract full installed ECU inventory from Gateway installation table",
            "uds_discovery": {
                "ecu": "0x19 (CAN_GATEWAY)",
                "tx": "0x710",
                "rx": "0x77A",
                "request": "22 04 A1",
                "response_prefix": "62 04 A1",
                "record_length_bytes": 4,
                "record_fields": {
                    "byte_0": "VAG Logical Address (e.g. 0x01=Engine, 0x03=ABS, 0x09=Central Elec, 0x17=Cluster, 0x53=EPB)",
                    "byte_1": "Sub-bus index (0x01=Drive CAN, 0x02=Convenience, 0x03=Infotainment, 0x04=Extended)",
                    "byte_2": "Installation & Communication flags (bit 0=Coded, bit 2=Communicating/Active)",
                    "byte_3": "Error status flags (bit 0=DTC stored)"
                },
                "installed_filter": "record[2] != 0",
                "active_filter": "(record[2] & 0x04) != 0"
            },
            "tp20_discovery": {
                "ecu": "0x19 (CAN_GATEWAY)",
                "setup_can_id": "0x21F",
                "request": "1A 9F",
                "response_prefix": "5A 9F",
                "evidence": "libCarista.so.c line 100945"
            }
        },
        {
            "stage_index": 4,
            "name": "ECU_IDENTIFICATION",
            "description": "Query each discovered ECU for full software, hardware, and ASAM descriptors",
            "prerequisite": "DiagnosticSessionControl Extended (10 03)",
            "identification_dids": [
                {"did": "0xF187", "name": "VAG_PART_NUMBER", "type": "ASCII_11", "desc": "e.g. 1K0 907 379 BE"},
                {"did": "0xF189", "name": "SOFTWARE_VERSION", "type": "ASCII_4", "desc": "e.g. 0109"},
                {"did": "0xF191", "name": "HARDWARE_VERSION", "type": "ASCII_3", "desc": "e.g. H04"},
                {"did": "0xF18C", "name": "SERIAL_NUMBER", "type": "ASCII", "desc": "ECU hardware serial number"},
                {"did": "0xF197", "name": "SYSTEM_COMPONENT_NAME", "type": "ASCII", "desc": "e.g. J104 C4 450M VD82"},
                {"did": "0xF19E", "name": "ASAM_ODX_FILE_ID", "type": "ASCII", "desc": "e.g. EV_BOSCH_ESP9_MQB"},
                {"did": "0xF1A2", "name": "ASAM_ODX_FILE_VERSION", "type": "ASCII", "desc": "e.g. 001002"},
                {"did": "0xF1A3", "name": "LONG_CODING_STRING", "type": "HEX_BYTES", "desc": "Current multi-byte coding payload"},
                {"did": "0x0608", "name": "SLAVE_SUBMODULES", "type": "RECORD_LIST", "desc": "LIN slave devices (Wiper, Rain sensor)"}
            ]
        },
        {
            "stage_index": 5,
            "name": "APPLICABILITY_EVALUATION",
            "description": "Six-layer gating logic to determine if a specific setting or tool can be run safely",
            "layers": [
                {"layer": 1, "name": "OEM_GATE", "rule": "Vehicle brand must match feature OEM (VAG: VW, Audi, Skoda, SEAT, Cupra, Bentley, Lamborghini)"},
                {"layer": 2, "name": "PLATFORM_GATE", "rule": "Vehicle chassis code must match feature platform (PQ35, MQB, MLB, MLBevo)"},
                {"layer": 3, "name": "ECU_PRESENCE_GATE", "rule": "Required ECU (e.g. 0x53 for EPB, 0x09 for BCM) must be installed in Gateway list"},
                {"layer": 4, "name": "SW_HW_RANGE_GATE", "rule": "ECU Software and Hardware version must fall within tested bounds"},
                {"layer": 5, "name": "ASAM_WHITELIST_GATE", "rule": "ASAM_ODX_FILE_ID must match whitelist in applicability_rules.json"},
                {"layer": 6, "name": "SECURITY_SFD_GATE", "rule": "If vehicle is MQB2020+ and ECU is SFD protected, feature requires SFD token. Otherwise unlocked."}
            ]
        }
    ]
}

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_json = os.path.join(base_dir, "research", "molecular", "ecu_identification_rules.json")
    out_md = os.path.join(base_dir, "research", "molecular", "VEHICLE_DETECTION_PIPELINE.md")

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(PIPELINE_RULES, f, indent=2)
    print(f"[+] Wrote {out_json}")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Molecular Vehicle & ECU Identification Pipeline\n\n")
        f.write("Full end-to-end specification of how Carista discovers vehicle identity, interrogates the gateway, and evaluates ECU applicability.\n\n")

        f.write("## 1. End-to-End Discovery Pipeline Flowchart\n\n")
        f.write("```mermaid\n")
        f.write("flowchart TD\n")
        f.write("    A[\"1. Adapter Handshake<br/>(AT Z, AT E0, AT SP 6)\"] --> B[\"2. VIN Acquisition<br/>(Read DID 0xF190 / Mode 09 PID 02)\"]\n")
        f.write("    B --> C[\"3. Gateway Discovery<br/>(UDS 22 04 A1 / TP2.0 1A 9F)\"]\n")
        f.write("    C --> D[\"4. Parse Installed ECUs<br/>(Filter record[2] != 0 & active bit)\"]\n")
        f.write("    D --> E[\"5. Interrogate Discovered ECUs<br/>(DIDs F187, F189, F191, F19E, F1A3)\"]\n")
        f.write("    E --> F[\"6. Applicability Evaluation<br/>(OEM -> Platform -> ECU -> ASAM Whitelist -> SFD Check)\"]\n")
        f.write("    F --> G[\"7. Populate Enabled Features & Services\"]\n")
        f.write("```\n\n")

        for st in PIPELINE_RULES["pipeline_stages"]:
            f.write(f"## Stage {st['stage_index']}: {st['name']}\n\n")
            f.write(f"**Description**: {st['description']}  \n\n")
            f.write("```json\n")
            f.write(json.dumps(st, indent=2) + "\n")
            f.write("```\n\n")

    print(f"[+] Wrote {out_md}")

if __name__ == "__main__":
    main()
