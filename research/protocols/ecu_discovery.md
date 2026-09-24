# ECU Discovery & Gateway Installation List

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
