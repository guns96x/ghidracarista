# Controller Area Network (CAN) Specification

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
