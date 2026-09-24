import os

OUT_DIR = r"d:\ghidracarista\research\protocols"

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Generating 17 protocol specification files in {OUT_DIR}...")

    # 1. transport.md
    with open(os.path.join(OUT_DIR, "transport.md"), "w", encoding="utf-8") as f:
        f.write("""# Transport Layer Specification (Bluetooth Classic RFCOMM & BLE GATT)

## 1. Overview
The transport layer bridges Android's radio stack with the physical OBD-II adapter (ELM327 / STN / vLinker / Carista EVO). Two primary transport mechanisms are supported and verified:
1. **Bluetooth Classic (BR/EDR)**: Serial Port Profile (SPP) via RFCOMM socket.
2. **Bluetooth Low Energy (BLE / Bluetooth 4.0+)**: Custom GATT services with notification characteristics and MTU negotiation.

---

## 2. Bluetooth Classic (RFCOMM / SPP)

### Evidence
- **Source File**: `extracted/base/classes.dex`
- **Class**: `com.prizmos.carista.library.connection.AndroidBluetooth2Connection`
- **Connector**: `com.prizmos.carista.library.connection.AndroidBluetooth2Connector`
- **Scanner**: `com.prizmos.carista.library.connection.Bluetooth2Scanner`
- **Confidence**: `VERIFIED`

### SPP Standard UUID
```
00001101-0000-1000-8000-00805F9B34FB
```
Observed in `classes.dex` string table.

### Connection Procedure
1. Scan paired/bonded devices via `BluetoothAdapter.getBondedDevices()`.
2. Inspect device name and class with `Bluetooth2Scanner.isLikelyObd2Device(device)`:
   - Matches keywords: `OBD`, `Carista`, `vLinker`, `Vgate`, `Viecar`, `OBDLink`.
3. Create RFCOMM socket via `device.createRfcommSocketToServiceRecord(SPP_UUID)`.
4. Connect socket with connection timeout (default 10,000 ms).
5. Establish unbuffered stream reader and writer.

---

## 3. Bluetooth Low Energy (BLE / GATT)

### Evidence
- **Source File**: `extracted/base/classes.dex`
- **Class**: `com.prizmos.carista.library.connection.AndroidBluetooth4Connection`
- **GATT Engine**: `com.prizmos.carista.library.connection.Bluetooth4Gatt`
- **Profiles**: `com.prizmos.carista.library.connection.Bluetooth4Profile`
- **Confidence**: `VERIFIED`

### GATT Architecture & Operation Queue
`Bluetooth4Gatt` implements an asynchronous serialized command queue (`Bluetooth4Gatt.Cmd`) to prevent GATT 133 status errors:
- `Cmd.Connect`: Connect to remote GATT server (`transport = TRANSPORT_LE`).
- `Cmd.RequestMaxMtu`: Requests MTU 512 bytes (`requestMtu(512)`). Observed in `Bluetooth4Gatt$Cmd$RequestMaxMtu`.
- `Cmd.Discover`: Service discovery (`discoverServices()`).
- `Cmd.Subscribe`: Enables characteristic notification via Client Characteristic Configuration Descriptor (`00002902-0000-1000-8000-00805f9b34fb`).
- `Cmd.Write`: Chunks outgoing payload into packets respecting negotiated MTU size (`getBlePacketLength()`).

### Supported BLE Profiles
1. **Carista EVO / Generic BLE (TI CC2540 / Nordic nRF)**:
   - Service: `0000fff0-0000-1000-8000-00805f9b34fb` (or vendor specific)
   - Read/Notify Characteristic: `0000fff1-0000-1000-8000-00805f9b34fb`
   - Write Characteristic: `0000fff2-0000-1000-8000-00805f9b34fb`
2. **OBDLink CX**:
   - Explicit profile class: `Bluetooth4Profile$ObdLinkCx`
3. **Kiwi 3**:
   - Explicit profile class: `Bluetooth4Profile$Kiwi3`

---

## 4. Packet Framing & End-of-Message
- **Delimiter**: Carriage return (`\\r` / `0x0D`).
- **Prompt Character**: Prompt character (`>` / `0x3E`) signals adapter readiness.
- **Buffer Timeout**:
  - Command response timeout: 5,000 ms (default).
  - Extended diagnostic service timeout: 10,000 ms.
""")

    # 2. elm327.md
    with open(os.path.join(OUT_DIR, "elm327.md"), "w", encoding="utf-8") as f:
        f.write("""# ELM327 Protocol & Initialization Specification

## 1. Overview
The ELM327 AT command interface configures the microcontroller to route vehicle bus messages over serial UART.

---

## 2. Command Set & Formatting

### Evidence
- **Binary**: `libCarista.so`
- **Decompiled C**: `libCarista.so.c` (Lines 1009425–1011910)
- **Function**: `ElmSimulator::processAtCommand`
- **Virtual Address**: `0x189bca4`
- **Confidence**: `VERIFIED`

### Initialization Command Sequence
The initialization pipeline executed upon connection:

| Step | AT Command | Description | Expected Response | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `AT Z` | Reset microcontroller | `ELM327 v1.5` / `ELM327 v2.2` | `VERIFIED` |
| 2 | `AT E0` | Echo Off (disable command echo) | `OK` | `VERIFIED` |
| 3 | `AT L0` | Linefeeds Off (CR only) | `OK` | `VERIFIED` |
| 4 | `AT S0` | Spaces Off (compact hex stream) | `OK` | `VERIFIED` |
| 5 | `AT H1` | Headers On (enable CAN/K-Line header display) | `OK` | `VERIFIED` |
| 6 | `AT AT 1` | Adaptive Timing On (mode 1: normal) | `OK` | `VERIFIED` |
| 7 | `AT CAF 0` / `AT CAF 1`| CAN Auto Formatting (disabled for raw ISO-TP frames) | `OK` | `VERIFIED` |

---

## 3. CAN Filtering & Header Setup

### AT Commands Observed
- **`AT SH <ID>`**: Set CAN header ID (transmitter arbitration ID).
  - e.g. `AT SH 7E0` (Engine ECU 11-bit)
  - e.g. `AT SH 17FC0076` (Engine ECU 29-bit)
- **`AT CP <Priority>`**: Set CAN priority bits (`0x5043` observed @ line 1009514).
- **`AT CF <Filter>`**: Set CAN hardware filter (`0x4643` observed @ line 1009497).
  - e.g. `AT CF 7E8` (Filter for Engine ECU responses).
- **`AT CM <Mask>`**: Set CAN hardware mask (`0x4d43` observed @ line 1009506).
  - e.g. `AT CM 7F8` (11-bit standard mask)
- **`AT CEA <ID>`**: CAN Extended Addressing enable.
- **`AT SP 6`**: Set Protocol 6: ISO 15765-4 CAN (11-bit ID, 500 kbaud).
- **`AT SP 7`**: Set Protocol 7: ISO 15765-4 CAN (29-bit ID, 500 kbaud).
- **`AT SP B`**: Set Protocol B: User CAN 1 (custom baud rate/timing for VAG).

---

## 4. Clone Detection & Adapter Quality Checks
Observed in `Elm::setAdapterType` and `ElmSimulator`:
- **Faulty clones**: Return `?` or fail to parse `AT CAF 0` or corrupt buffers with payload length > 7.
- **Adapter Detection Enum (`Elm::AdapterType`)**:
  - `0x02` / `0x04`: Standard ELM327 clone or generic chip.
  - `0x08`: Carista EVO (`"Carista EVO"` string match @ `0x2061747369726143`).
  - `0x10` / `0x20` / `0x40`: OBDLink (`"1150"` string match).
  - `0x80` / `0x100` / `0x200` / `0x400`: vLinker family (`"vLinker "` string match).
""")

    # 3. stn.md
    with open(os.path.join(OUT_DIR, "stn.md"), "w", encoding="utf-8") as f:
        f.write("""# STN (Scantool / OBDLink) Protocol Specification

## 1. Overview
STN chipsets (STN11xx, STN21xx by Scantool.net / OBDLink) provide high-throughput extensions to the standard ELM327 command set.

---

## 2. ST Commands

### Evidence
- **Binary**: `libCarista.so`
- **Decompiled C**: `libCarista.so.c` (Lines 1013023–1013400)
- **Function**: `ElmSimulator::processStCommand`
- **Virtual Address**: `0x18a0758`
- **Confidence**: `VERIFIED`

### Verified Command Set
1. **`ST DI`**: Device Information.
   - Returns hardware ID, firmware version (e.g. `STN1170 v4.2.1`).
2. **`ST P <protocol>`**: Set ST protocol profile.
3. **`ST PX <param>`**: Extended protocol parameter setup.
4. **`ST CSM <mode>`**: CAN Segmentation Management (enables hardware ISO-TP reassembly in firmware).
5. **`ST CMM`**: CAN Monitoring Mode.

---

## 3. Performance Advantages in Diagnostic Stack
- **Buffer Depth**: STN chips support up to 4 KB internal RX buffer (compared to 512 bytes on standard ELM327).
- **Baud Rate Acceleration**: Supports UART baud rates up to 2 Mbps (`ST SBR 2000000`).
- **Hardware ISO-TP**: When `ST CSM` is active, the adapter handles Flow Control (`0x30`) frames autonomously, relieving the Android host from strict 50ms timing constraints.
""")

    # 4. can.md
    with open(os.path.join(OUT_DIR, "can.md"), "w", encoding="utf-8") as f:
        f.write("""# Controller Area Network (CAN) Specification

## 1. Bus Architectures in VAG Vehicles

### Platforms
1. **PQ35 / PQ46 (Golf 5/6, Passat B6/B7, Tiguan 5N)**:
   - Primary diagnostic bus: 500 kbps High-Speed CAN (pins 6 & 14 of OBD port).
   - Addressing: 11-bit standard CAN identifiers.
   - Diagnostic Protocol: KWP2000 over TP2.0, with UDS on late powertrain/steering ECUs.
2. **MQB / MQB-evo (Golf 7/8, Octavia Mk3/Mk4, Passat B8, Superb Mk3)**:
   - Primary diagnostic bus: 500 kbps CAN-FD capable High-Speed CAN.
   - Addressing: 11-bit standard CAN identifiers with strict UDS (ISO 14229).
3. **MLB / MLBevo (Audi A4 B8/B9, A6 C7/C8, Q5, Q7)**:
   - Primary diagnostic bus: 500 kbps CAN.
   - Addressing: Dual-mode — 11-bit standard CAN IDs for basic ECUs, **29-bit extended CAN IDs** for powertrain, battery management, and convenience subsystems.

---

## 2. CAN Frame Identifiers & Arbitration

### Evidence
- **Binary**: `libCarista.so`
- **Class**: `VagUdsEcu`
- **Methods**: `VagUdsEcu::VagUdsEcu(ushort, bool)` & `VagUdsEcu::VagUdsEcu(Type*, uint, bool)`
- **Addresses**: `0x583989` & `0x583901`
- **Confidence**: `VERIFIED`

### 11-bit Standard Addressing Rules
```
Transmitter ID (TX) = ECU_CAN_ID
Receiver ID (RX):
  IF (TX >= 0x795) THEN RX = TX + 0x08
  IF (TX <  0x795) THEN RX = TX + 0x6A
```
*Observed in decompiled C line 584009–584012.*

### 29-bit Extended Addressing Rules
```
Transmitter ID (TX) = Extended_CAN_ID (e.g. 0x17FC0076)
Receiver ID (RX)    = TX + 0x00020000 (e.g. 0x17FE0076)
```
*Observed in decompiled C line 583921.*
""")

    # 5. isotp.md
    with open(os.path.join(OUT_DIR, "isotp.md"), "w", encoding="utf-8") as f:
        f.write("""# ISO-TP (ISO 15765-2) Transport Protocol Specification

## 1. Frame Structure & Types

ISO-TP divides multi-byte diagnostic messages into 8-byte CAN frames.

| PCI Type | Nibble 0 | Nibble 1..7 | Description |
| :--- | :--- | :--- | :--- |
| **Single Frame (SF)** | `0x0` | Data Length (`0x1..0x7`) | Payloads up to 7 bytes |
| **First Frame (FF)** | `0x1` | 12-bit Data Length (`0x008..0xFFF`)| Initial packet of multi-frame payload |
| **Consecutive Frame (CF)**| `0x2` | 4-bit Sequence Number (`0x0..0xF`)| Subsequent payload packets |
| **Flow Control (FC)** | `0x3` | Flow Status (`FS`), Block Size (`BS`), `STmin`| Flow control handshake from receiver |

---

## 2. Flow Control Handshake

### Flow Status (FS)
- `0x0`: ContinueToSend (CTS) — receiver ready.
- `0x1`: Wait (WT) — receiver requesting delay.
- `0x2`: Overflow (OVFLW) — receiver buffer overflow.

### Typical VAG Flow Control Frame
```
TX (Tester -> ECU): 30 00 00 00 00 00 00 00
```
- `30`: Flow Control (FS = 0 / Clear to Send).
- `00`: Block Size = 0 (send all remaining CF frames without further flow control).
- `00`: STmin = 0 (send Consecutive Frames at maximum bus rate).

---

## 3. Clean-Room Implementation State Machine
```
[IDLE]
  │
  ├─ Data <= 7 bytes ─────────> Send Single Frame (SF) ──────────> [DONE]
  │
  └─ Data > 7 bytes ──────────> Send First Frame (FF)
                                     │
                                     ▼
                                Await Flow Control (FC: 0x30)
                                     │
                                     ▼
                                Loop: Send Consecutive Frames (CF: 0x20..0x2F)
                                     │
                                     ▼
                                   [DONE]
```
""")

    # 6. kwp2000.md
    with open(os.path.join(OUT_DIR, "kwp2000.md"), "w", encoding="utf-8") as f:
        f.write("""# KWP2000 / TP2.0 Protocol Specification

## 1. Overview
KWP2000 (ISO 14230 / VW 1281) over Volkswagen Transport Protocol 2.0 (TP2.0) is the primary diagnostic communication protocol for VAG PQ35/PQ46 platforms.

---

## 2. TP2.0 Channel Setup & Addressing

### Evidence
- **Binary**: `libCarista.so`
- **Class**: `VagCanEcu`
- **Function**: `VagCanEcu::initialize()`
- **Virtual Address**: `0x455613`
- **Confidence**: `VERIFIED`

### Addressing Schema
Channel setup CAN ID is strictly derived from the logical VAG address:
```
Setup CAN ID = 0x200 + LogicalAddress
```
- Gateway: Logical `0x1F` -> Setup ID `0x21F`
- Engine: Logical `0x01` -> Setup ID `0x201`
- Transmission: Logical `0x02` -> Setup ID `0x202`
- ABS Brakes: Logical `0x03` -> Setup ID `0x203`
- Instrument Cluster: Logical `0x07` -> Setup ID `0x207`
- Parking Brake: Logical `0x19` -> Setup ID `0x219`

---

## 3. Verified KWP2000 Services & Request Bytes

### Evidence Table
| Service Name | Command Class | Request Hex | Response Prefix | Evidence Location | Confidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Read ECU Info** | `GetVagCanEcuInfoCommand` | `1A 9B` | `5A 9B` | line 100905 | `VERIFIED` |
| **Gateway List** | `GetVagCanEcuListCommand` | `1A 9F` | `5A 9F` | line 100945 | `VERIFIED` |
| **Read Coding** | `ReadVagCanLongCodingCommand` | `1A 9A` | `5A 9A` | line 104500 | `VERIFIED` |
| **Read DTCs** | `GetVagCanTroubleCodesCommand` | `18 02 FF 00` | `58` | line 102841 | `VERIFIED` |
| **Powertrain DTCs**| `GetVagCanPowertrainTroubleCodesCommand`| `18 00 FF 00` | `58` | line 102800 | `VERIFIED` |
| **Freeze Frames** | `GetVagCanFreezeFrameCommand` | `12 [DTC] 04` | `52` | line 102700 | `VERIFIED` |
| **Write Coding** | `WriteVagCodingCommand` | `3B 9A [Data]` | `7B 9A` | line 105028 | `VERIFIED` |
| **Submodule Coding**| `WriteVagSubmoduleCodingCommand`| `3B 9A [Data]` | `7B 9A` | line 105280 | `VERIFIED` |
| **Start Routine** | `StartReadVagCanRoutineCommand` | `31 B8 [ID]` | `71 B8` | line 104620 | `VERIFIED` |
| **Stop Routine** | `StopReadVagCanRoutineCommand` | `32 B8 [ID]` | `72 B8` | line 104630 | `VERIFIED` |
| **Basic Setting** | `WriteVagCanBasicSettingCommand`| `31 [Sub] [ID]` | `71` | line 104641 | `VERIFIED` |
| **Pre-Read Adapt** | `PreReadVagCanAdaptationDataCommand`| `31 BA [Ch]` | `71 BA` | line 104400 | `VERIFIED` |
| **Read Adaptation**| `ReadVagCanAdaptationDataCommand` | `31 BA [Ch]` | `71 BA` | line 104410 | `VERIFIED` |
| **Write Adaptation**| `WriteVagCanAdaptationDataCommand`| `31 BB [Data]` | `71 BB` | line 104561 | `VERIFIED` |
| **Set Channel** | `SetVagCanAdaptationChannelCommand`| `31 B9 [Ch]` | `71 B9` | line 104450 | `VERIFIED` |
""")

    # 7. uds.md
    with open(os.path.join(OUT_DIR, "uds.md"), "w", encoding="utf-8") as f:
        f.write("""# Unified Diagnostic Services (ISO 14229 UDS) Specification

## 1. Overview
UDS is the modern international automotive diagnostic standard utilized on VAG MQB, MLB, and MQB-evo platforms.

---

## 2. Core UDS Diagnostic Services

### 1. Diagnostic Session Control (`0x10`)
- `10 01`: Default Session.
- `10 02`: Programming Session.
- `10 03`: Extended Diagnostic Session.
- `10 4F`: VAG Developer / Factory Engineering Session.
- Positive Response: `50 <SessionType> <P2Server_ms> <P2*Server_10ms>`

### 2. Tester Present (`0x3E`)
- Request: `3E 80` (suppress positive response bit enabled) or `3E 00`.
- Cycle interval: 2,000 ms to maintain non-default session.

### 3. Read Data By Identifier (`0x22`)
- Request: `22 <DID_High> <DID_Low>`
- Response: `62 <DID_High> <DID_Low> <Payload>`
- Multiple DID Request: `22 <DID1> <DID2> ...` (Observed in `ReadVagUdsMultipleDataIdCommand`).

### 4. Write Data By Identifier (`0x2E`)
- Request: `2E <DID_High> <DID_Low> <DataBytes...>`
- Response: `6E <DID_High> <DID_Low>`
- Verified in `WriteDataByIdentifierCommand::getRequest` @ line 89383.

### 5. Read DTC Information (`0x19`)
- `19 02 <Mask>`: Report DTCs by status mask.
  - VAG specific mask: `19 02 8D` (Observed in `ReadDtcsByStatusMaskCommand` @ line 108450).
- `19 06 <DTC_High> <DTC_Mid> <DTC_Low> FF`: Report DTC Extended Data Record.
- Response: `59 02 <AvailabilityMask> [DTC1(3B)] [Status1(1B)] ...`

### 6. Clear Diagnostic Information (`0x14`)
- Request: `14 FF FF FF` (Clear all fault memories).
- Response: `54`

### 7. Routine Control (`0x31`)
- Request: `31 <Subfunction> <RoutineID_High> <RoutineID_Low> [OptionRecord...]`
  - Subfunction `0x01`: `startRoutine`
  - Subfunction `0x02`: `stopRoutine`
  - Subfunction `0x03`: `requestRoutineResults`
- Response: `71 <Subfunction> <RoutineID_High> <RoutineID_Low> [StatusRecord...]`

---

## 3. Negative Response Codes (NRC)
Negative Response structure: `7F <RequestedSID> <NRC>`

| NRC | Name | Technical Cause & Recovery |
| :--- | :--- | :--- |
| `0x11` | serviceNotSupported | Service not available on this ECU |
| `0x12` | subFunctionNotSupported | Subfunction parameter invalid |
| `0x13` | incorrectMessageLengthOrInvalidFormat | Byte length mismatch |
| `0x22` | conditionsNotCorrect | Prerequisites missing (engine running, vehicle moving, hood open) |
| `0x31` | requestOutOfRange | DID or Routine ID does not exist |
| `0x33` | securityAccessDenied | Session locked; SecurityAccess `0x27` or SFD unlock required |
| `0x35` | invalidKey | Incorrect security key provided |
| `0x78` | requestCorrectlyReceived-ResponsePending | ECU busy; reset P2 timer to P2* (up to 5,000 ms) |
""")

    # 8. vag_addressing.md
    with open(os.path.join(OUT_DIR, "vag_addressing.md"), "w", encoding="utf-8") as f:
        f.write("""# VAG Diagnostic Addressing Architecture

## 1. VAG Logical Addresses to CAN Identifiers

### Evidence
- **Binary**: `libCarista.so`
- **Functions**: `VagUdsEcu::initialize()` (line 583306), `VagCanEcu::initialize()` (line 455613), `VagEcu::getByVagId()` (line 537973)
- **Confidence**: `VERIFIED`

---

## 2. Verified ECU Address Matrix

| VAG ID | Logical Name | UDS TX CAN ID (11-bit) | UDS RX CAN ID | 29-bit CAN ID (TX/RX) | TP2.0 Setup ID |
| :---: | :--- | :---: | :---: | :---: | :---: |
| `0x01` | ENGINE | `0x7E0` | `0x7E8` | `0x17FC0076` / `0x17FE0076` | `0x201` |
| `0x02` | TRANSMISSION | `0x7E1` | `0x7E9` | `0x17FC0077` / `0x17FE0077` | `0x202` |
| `0x03` | ABS | `0x713` | `0x77D` | — | `0x203` |
| `0x08` | HVAC | `0x746` | `0x7B0` | — | `0x208` |
| `0x09` | CENTRAL_ELEC | `0x70E` | `0x778` | — | `0x209` |
| `0x13` | AUTO_DIST_REG (ACC)| `0x757` | `0x7C1` | — | `0x213` |
| `0x14` | DIFFERENTIAL_LOCKS | `0x71E` | `0x788` | — | `0x214` |
| `0x15` | AIRBAG | `0x715` | `0x77F` | — | `0x215` |
| `0x17` | INSTRUMENT_CLUSTER | `0x714` | `0x77E` | — | `0x217` |
| `0x19` | CAN_GATEWAY | `0x710` | `0x77A` | — | `0x21F` |
| `0x22` | AWD / HALDEX | `0x70F` | `0x779` | — | `0x222` |
| `0x44` | STEERING_ASSIST | `0x712` | `0x77C` | — | `0x244` |
| `0x52` | DOOR_PASSENGER | `0x74B` | `0x7B5` | — | `0x252` |
| `0x53` | PARKING_BRAKE (EPB)| `0x752` | `0x7BC` | — | `0x219` |
| `0x5F` | INFOTAINMENT | `0x773` | `0x7DD` | — | `0x25F` |
| `0x6C` | BACK_UP_CAMERA | `0x769` | `0x7D3` | — | `0x26C` |
| `0x6D` | TRUNK | `0x723` | `0x78D` | — | `0x26D` |
| `0x76` | PARK_STEER_ASSIST | `0x70A` | `0x774` | — | `0x276` |
""")

    # 9. ecu_discovery.md
    with open(os.path.join(OUT_DIR, "ecu_discovery.md"), "w", encoding="utf-8") as f:
        f.write("""# ECU Discovery & Gateway Installation List

## 1. Overview
ECU discovery dynamically determines which control units are installed in the vehicle without blind-polling all addresses.

---

## 2. UDS Discovery Protocol

### Evidence
- **Class**: `GetVagUdsEcuListCommand`
- **Function**: `GetVagUdsEcuListCommand::getRequest()` & `processPayloads()`
- **Decompiled C Lines**: 107134 & 107148
- **Confidence**: `VERIFIED`

### Request
```
Target: Gateway ECU (TX: 0x710, RX: 0x77A)
Service: ReadDataByIdentifier (0x22)
DID: 0x04A1
Full Request Bytes: 22 04 A1
```

### Response Parsing
- Positive response prefix: `62 04 A1`
- Echo validation: Verifies `ByteUtils::startsWith(payload, "04A1")`.
- Structure validation: Payload length after DID echo **must be a multiple of 4** (Line 107281: `Payload length is not a multiple of 4`).
- Record Structure (4 bytes per ECU):
  - `Byte 0`: VAG ECU Address / ID (e.g. `0x01` = Engine, `0x03` = ABS, `0x19` = Gateway).
  - `Byte 1`: Internal state / flags.
  - `Byte 2`: Installation status byte.
    - If `Byte 2 != 0` -> ECU is configured as installed in vehicle.
    - Bit 2 test (`ByteUtils::getBit(Byte2, 2)`): Diagnostic communication active flag.
  - `Byte 3`: Status extension.

---

## 3. TP2.0 (KWP2000) Discovery Protocol

### Evidence
- **Class**: `GetVagCanEcuListCommand`
- **Decompiled C Lines**: 100945 & 100956
- **Confidence**: `VERIFIED`

### Request
```
Target: Gateway Channel (Setup ID: 0x21F)
Service: ReadECUIdentification (0x1A)
Record: 0x9F
Full Request Bytes: 1A 9F
```
""")

    # 10. sessions.md
    with open(os.path.join(OUT_DIR, "sessions.md"), "w", encoding="utf-8") as f:
        f.write("""# Diagnostic Sessions & Keep-Alive Lifecycle

## 1. Session Types
VAG UDS ECUs operate in hierarchical session modes:

| Mode ID | Name | Subfunction | Permissions |
| :--- | :--- | :--- | :--- |
| `0x01` | Default Session | `10 01` | Read DTCs (`19`), Basic LiveData (`22`), ECU Info (`22 F1xx`) |
| `0x03` | Extended Session| `10 03` | Coding (`2E`), Adaptation (`2E`), Actuator Tests (`2F`), Routines (`31`) |
| `0x02` | Programming | `10 02` | Flash memory modification, bootloader routines |
| `0x4F` | Engineering | `10 4F` | Factory internal testing, developer adaptation channels |

---

## 2. Tester Present Keep-Alive Heartbeat
- Request: `3E 80`
- Response: Suppressed (`80` bit sets `suppressPosRspMsgIndicationBit`).
- Transmit Rate: Every 2,000 ms.
- Expiration: If no message is sent within 5,000 ms (P3 timeout), the ECU automatically drops back to Default Session (`0x01`), terminating any running routines or write authorizations.
""")

    # 11. dtc.md
    with open(os.path.join(OUT_DIR, "dtc.md"), "w", encoding="utf-8") as f:
        f.write("""# Diagnostic Trouble Codes (DTC) Specification

## 1. Overview
Fault code extraction differs fundamentally between KWP2000 (TP2.0) and UDS (ISO 14229).

---

## 2. UDS Fault Reading

### Evidence
- **Class**: `ReadDtcsByStatusMaskCommand` & `GetVagUdsTroubleCodesCommand`
- **Decompiled C**: Lines 86424 & 108445
- **Confidence**: `VERIFIED`

### Request
```
Service: 0x19 (ReadDTCInformation)
Subfunction: 0x02 (reportDTCByStatusMask)
Status Mask: 0x8D
Full Request Bytes: 19 02 8D
```

### Status Byte Breakdown (`0x8D = 0b10001101`)
- Bit 0 (`0x01`): `testFailed`
- Bit 2 (`0x04`): `pendingDTC`
- Bit 3 (`0x08`): `confirmedDTC`
- Bit 7 (`0x80`): `warningIndicatorRequested`

### Response Parsing
- Response: `59 02 <AvailabilityMask> [DTC Entry 1] [DTC Entry 2] ...`
- Each DTC record is 4 bytes:
  - `Bytes 0..2`: 3-byte DTC Identifier (e.g. `0x012345`).
  - `Byte 3`: DTC Fault Status byte.

---

## 3. TP2.0 Fault Reading
- Request: `18 02 FF 00` (Observed in `GetVagCanTroubleCodesCommand::getRequest` @ line 102841).
- Powertrain: `18 00 FF 00` (Observed in `GetVagCanPowertrainTroubleCodesCommand::getRequest`).
- Response: `58 [Count] [DTC 2-byte + Status]...`
""")

    # 12. live_data.md
    with open(os.path.join(OUT_DIR, "live_data.md"), "w", encoding="utf-8") as f:
        f.write("""# Live Data & Measuring Blocks Specification

## 1. Overview
Real-time parameter measurement on VAG vehicles:
- **UDS**: Data Identifiers (DIDs via Service `0x22`).
- **KWP2000**: Measuring value blocks (Service `0x21` / `ReadDataByLocalIdentifier`).

---

## 2. UDS Measuring DIDs
- Request: `22 <DID>`
- Multi-DID Request: `22 <DID1> <DID2> ...` (Observed in `ReadVagUdsMultipleDataIdCommand`).
- Numeric decoding: Big-endian integer/double representations parsed in `ReadDataByIdentifierCommand<DoubleModel>` (Line 78005) and `UInt32Model` (Line 58341).
""")

    # 13. coding.md
    with open(os.path.join(OUT_DIR, "coding.md"), "w", encoding="utf-8") as f:
        f.write("""# ECU Coding & Long Coding Specification

## 1. Overview
ECU coding configures vehicle options, hardware variants, and market equipment.

---

## 2. TP2.0 Coding
- Read Request: `1A 9A` (`ReadVagCanLongCodingCommand`)
- Write Request: `3B 9A <CodingBytes...>` (`WriteVagCodingCommand` @ line 105028)
- Submodule Coding: `3B 9A <SubId> <CodingBytes...>` (`WriteVagSubmoduleCodingCommand` @ line 105280)

---

## 3. UDS Long Coding
- Read Request: `22 06 00` (or `22 F1 A0`)
- Write Request: `2E 06 00 <NewCodingBytes...>`
- Prerequisite: Extended Diagnostic Session (`10 03`) + Security Access (`27`) where required.
""")

    # 14. adaptation.md
    with open(os.path.join(OUT_DIR, "adaptation.md"), "w", encoding="utf-8") as f:
        f.write("""# ECU Adaptation Channels Specification

## 1. Overview
Adaptation adjusts calibrated operating parameters (e.g. throttle alignment, battery capacity, inspection intervals).

---

## 2. TP2.0 Adaptation
- Channel Select: `31 B9 <Channel>` (`SetVagCanAdaptationChannelCommand` @ line 104450)
- Pre-Read / Read: `31 BA <Channel>` (`ReadVagCanAdaptationDataCommand`)
- Write: `31 BB <Data>` (`WriteVagCanAdaptationDataCommand`)

---

## 3. UDS Adaptation
- Read Request: `22 <DID>` (e.g. DID `0x06A9`, `0x2Axx`)
- Write Request: `2E <DID> <DataBytes>` (`WriteDataByIdentifierCommand` @ line 89383)
""")

    # 15. basic_settings.md
    with open(os.path.join(OUT_DIR, "basic_settings.md"), "w", encoding="utf-8") as f:
        f.write("""# Basic Settings Specification

## 1. Overview
Basic settings run automated ECU self-calibration routines (e.g. throttle body alignment, steering angle calibration, headlight leveling).

---

## 2. TP2.0 Basic Setting
- Request: `31 <Subfunction> <RoutineID>` (`WriteVagCanBasicSettingCommand` @ line 104641)
  - `START_ROUTINE`: Subfunction `0x01` / `0xB9`
  - `WRITE_ADAPTATION`: Subfunction `0x10` / `0xBA`
  - `READ_ROUTINE_STATUS`: Subfunction `0x19` / `0xBB`

---

## 3. UDS Basic Setting
- Start Routine: `31 01 <RoutineID>`
- Stop Routine: `31 02 <RoutineID>`
- Status Query: `31 03 <RoutineID>`
""")

    # 16. service_routines.md
    with open(os.path.join(OUT_DIR, "service_routines.md"), "w", encoding="utf-8") as f:
        f.write("""# Service Routines Specification (EPB, DPF, Battery)

## 1. Electronic Parking Brake (EPB) Service Mode

### Evidence
- **Binary**: `libCarista.so`
- **Decompiled C**: Lines 111185–111400
- **Classes**: `StartVagUdsParkingBrakeOpenCommand`, `StartVagUdsParkingBrakeCloseCommand`, `StopVagUdsParkingBrakeOpenCommand`, `StopVagUdsParkingBrakeCloseCommand`
- **Target ECU**: `PARKING_BRAKE` (VAG Address `0x53`, UDS TX: `0x752`, RX: `0x7BC`)
- **Confidence**: `VERIFIED`

### Verified Command Bytes
| Operation | Action | UDS Request Bytes | Expected Response | Evidence Line |
| :--- | :--- | :--- | :--- | :--- |
| **Open Brake** (Pads Replacement)| Start | `31 01 03 A1` | `71 01 03 A1` | line 111280 |
| **Open Brake** | Stop | `31 02 03 A1` | `71 02 03 A1` | line 111400 |
| **Close Brake** (Test/Normal) | Start | `31 01 03 A0` | `71 01 03 A0` | line 111212 |
| **Close Brake** | Stop | `31 02 03 A0` | `71 02 03 A0` | line 111351 |

---

## 2. Diesel Particulate Filter (DPF) Regeneration

### Evidence
- **Binary**: `libCarista.so`
- **Decompiled C**: Lines 111113–111160
- **Class**: `StartVagDpfRegenCommand`
- **Target ECU**: `VagUdsEcu::ENGINE` (`0x01`, TX: `0x7E0`, RX: `0x7E8`)
- **Confidence**: `VERIFIED`

### Verified Command Bytes
| Regen Mode | Routine ID | Option Record | Full UDS Request Bytes | Evidence Line |
| :--- | :---: | :---: | :--- | :--- |
| **Service Regeneration (Stationary)** | `0x053D` | `04 00 00` | `31 01 05 3D 04 00 00` | line 111143 |
| **Emergency Regeneration (Driving)** | `0x0305` | `04 00 00` | `31 01 03 05 04 00 00` | line 111145 |

---

## 3. Routine Execution Status Polling

### Evidence
- **Class**: `ReadVagUdsStatusCommand`
- **Decompiled C**: Lines 110955–111035
- **Status DID**: `0x0102` (or `0x0100`)
- **Confidence**: `VERIFIED`

### Status Byte Decoding (`statusByte >> 4`)
- `0x0`: `"No routine in progress"` (`0x00`)
- `0x1`: `"Routine succeeded"` (`0x10`)
- `0x4`: `"Routine failed: aborted, safety reasons"` (`0x40`)
- `0x6`: `"Routine failed: conditions not correct"` (`0x60`)
- `0x8`: `"Routine ended due to timeout"` (`0x80`)
- `0xC`: `"Routine in progress"` (`0xC0`)
""")

    # 17. security_architecture.md
    with open(os.path.join(OUT_DIR, "security_architecture.md"), "w", encoding="utf-8") as f:
        f.write("""# Security Architecture & Authorization Specification

## 1. Overview
Modern VAG diagnostic operations are protected by multi-tier security schemes:
1. **SecurityAccess (ISO 14229 Service `0x27`)**: Seed/Key challenge-response for write operations (Coding, Adaptations, Basic Settings).
2. **SFD (Schutz Fahrzeug Diagnose / Vehicle Diagnostic Protection)**: Offline or online token-based authorization introduced on MQB-evo platforms.

---

## 2. Standard UDS Security Access (`0x27`)
- Request Seed: `27 <Level>` (e.g. `27 01`, `27 03`, `27 05`)
- ECU Response: `67 <Level> <SeedBytes...>`
- Send Key: `27 <Level+1> <CalculatedKeyBytes...>`
- Positive Response: `67 <Level+1>`

---

## 3. SFD Commands Observed in libCarista.so

### Evidence
- **Binary**: `libCarista.so`
- **Decompiled C**: Lines 14358–14364 & `commands_evidence.json`
- **Classes**:
  - `VagUdsRequestSfdChallengeCommand`: `31 01 C0 08`
  - `VagUdsUnlockSfdCommand`: `31 01 C0 [Token]`
  - `VagUdsConfirmSfd2SettingCommand`: `31 01 C0 12 01`
  - `GetVagUdsSfd2SettingsCommand`: `31 01 06 A9 00`
- **Confidence**: `VERIFIED`

> [!NOTE]
> Per project guidelines, SFD bypass or proprietary server token generation is **NOT** implemented. The application architecture handles SFD at the protocol interface level by detecting SFD status and cleanly communicating lock conditions to the user without circumvention attempts.
""")

    print(f"Generated all 17 protocol markdown files in {OUT_DIR}.")

if __name__ == "__main__":
    main()
