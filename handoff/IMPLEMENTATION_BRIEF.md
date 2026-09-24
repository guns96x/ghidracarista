# Implementation Brief for Android Diagnostic Stack Development

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
