# Unified Diagnostic Services (ISO 14229 UDS) Specification

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
