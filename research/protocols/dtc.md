# Diagnostic Trouble Codes (DTC) Specification

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
