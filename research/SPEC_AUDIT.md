# Audit of VAG_OBD_Diagnostic_Specification.md Against Verified Evidence

> **Audit Date:** 2026-09-24  
> **Auditor:** Antigravity Autonomous Clean-Room Protocol Engine  
> **Evidence Baseline:** `libCarista.so` (ELF 64-bit ARMv8), `libCarista.so.c` (1,408,085 lines Ghidra export), `classes.dex`  

---

## 1. Executive Summary
The audit of `VAG_OBD_Diagnostic_Specification.md` revealed **critical errors** in CAN identifier addressing, electronic parking brake (EPB) routine IDs, DTC status masks, and discovery methodology. Using the previous specification without corrections would result in:
1. Transmitting brake actuator commands to the **HVAC (Climate Control)** ECU instead of the Electronic Parking Brake ECU.
2. Routine failure (NRC `0x31` RequestOutOfRange) due to incorrect EPB routine IDs (`0x0010` vs real `0x03A1`).
3. Failed gateway communication for Central Electrics (`0x709` vs real `0x70E`).
4. Highly inefficient brute-force bus polling instead of reading the Gateway Installation List (`22 04 A1`).

---

## 2. Claim-by-Claim Audit Table

| # | Specification Claim | Real Binary Evidence | Status | Correction | Confidence |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | **EPB Tx CAN ID**: `0x746` / `0x7B0` | `libCarista.so.c` lines 583356 & 583368: `0x746` is `HVAC`; `PARKING_BRAKE` is `0x752` / `0x7BC` | **CRITICAL ERROR** | Change EPB to Tx `0x752`, Rx `0x7BC` | `VERIFIED` |
| 2 | **EPB Open Routine ID**: `31 01 00 10` | `libCarista.so.c` line 111280 (`StartVagUdsParkingBrakeOpenCommand`): Routine ID is `0x03A1` | **CRITICAL ERROR** | Use `31 01 03 A1` | `VERIFIED` |
| 3 | **EPB Close Routine ID**: `31 01 00 11` | `libCarista.so.c` line 111212 (`StartVagUdsParkingBrakeCloseCommand`): Routine ID is `0x03A0` | **CRITICAL ERROR** | Use `31 01 03 A0` | `VERIFIED` |
| 4 | **BCM Tx CAN ID**: `0x709` / `0x773` | `libCarista.so.c` line 583389 (`CENTRAL_ELEC`): Tx `0x70E`, Rx `0x778` | **INCORRECT** | Change BCM (0x09) to Tx `0x70E`, Rx `0x778` | `VERIFIED` |
| 5 | **DTC Status Mask**: `19 02 09` | `libCarista.so.c` line 108450 (`ReadDtcsByStatusMaskCommand`): VAG uses mask `0x8D` | **INCORRECT** | Use `19 02 8D` | `VERIFIED` |
| 6 | **AutoScan Discovery**: Brute-force polling `01, 02, 03...` with `22 F1 87` | `libCarista.so.c` line 107137 (`GetVagUdsEcuListCommand`): Gateway list query `22 04 A1` | **SUBOPTIMAL / UNVERIFIED** | Query Gateway DID `0x04A1` (UDS) or `1A 9F` (TP2.0) | `VERIFIED` |
| 7 | **Long Coding DID**: `22 F1 A3` | `libCarista.so.c` line 104500 & line 105028: Coding uses `1A 9A` / `3B 9A` (TP2.0) and `0x0600` (UDS) | **UNCONFIRMED** | Verify ECU-specific DID before write | `LIKELY` |
| 8 | **Engine Tx CAN ID**: `0x7E0` / `0x7E8` | `libCarista.so.c` line 583318: `ENGINE = VagUdsEcu(pVVar1, 0x7e0, true)` | **CORRECT** | None (valid) | `VERIFIED` |
| 9 | **Transmission Tx CAN ID**: `0x7E1` / `0x7E9` | `libCarista.so.c` line 583334: `TRANSMISSION = VagUdsEcu(pVVar1, 0x7e1, true)` | **CORRECT** | None (valid) | `VERIFIED` |
| 10 | **ABS Tx CAN ID**: `0x713` / `0x77D` | `libCarista.so.c` line 583350: `ABS = VagUdsEcu(pVVar1, 0x713, true)` | **CORRECT** | None (valid) | `VERIFIED` |
| 11 | **Cluster Tx CAN ID**: `0x714` / `0x77E` | `libCarista.so.c` line 583383: `INSTRUMENT_CLUSTER = VagUdsEcu(pVVar1, 0x714, true)` | **CORRECT** | None (valid) | `VERIFIED` |
| 12 | **Gateway Tx CAN ID**: `0x710` / `0x77A` | `libCarista.so.c` line 583315: `CAN_GATEWAY = VagUdsEcu(pVVar1, 0x710, true)` | **CORRECT** | None (valid) | `VERIFIED` |
| 13 | **VIN DID**: `22 F1 90` | Standard UDS DID & `libCarista.so` string table | **CORRECT** | None (valid) | `VERIFIED` |
| 14 | **Clear DTC**: `14 FF FF FF` | Standard UDS Service 0x14 | **CORRECT** | None (valid) | `VERIFIED` |
| 15 | **Tester Present**: `3E 80` | `libCarista.so` line 1347172 | **CORRECT** | None (valid) | `VERIFIED` |
