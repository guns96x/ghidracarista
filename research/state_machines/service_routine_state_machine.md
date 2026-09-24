# Service Routine Execution State Machine (EPB / DPF)

## 1. Overview
High-stakes actuator service routines (Electronic Parking Brake pad replacement and DPF regeneration) require strict sequential phase transitions, safety prerequisite checks, and polling loops.

### Evidence
- **Binary**: `libCarista.so`
- **Classes**: `StartVagUdsParkingBrakeOpenCommand`, `StartVagDpfRegenCommand`, `ReadVagUdsStatusCommand`
- **Decompiled C Lines**: 110955–111400
- **Confidence**: `VERIFIED`

---

## 2. Mermaid State Diagram

```mermaid
sequenceDiagram
    autonumber
    participant App as Android Diagnostic Stack
    participant Transport as ConnectionManager
    participant ECU as Target ECU (0x53 EPB / 0x01 Engine)

    Note over App,ECU: Phase 1: Session & Safety Preconditions
    App->>Transport: Ensure Extended Session (10 03)
    Transport->>ECU: 10 03
    ECU-->>Transport: 50 03 (Extended Session Active)
    App->>Transport: Read Fault Codes (19 02 8D)
    Transport->>ECU: 19 02 8D
    ECU-->>Transport: 59 02 (DTC List)
    Note over App: Check: No active hydraulic / actuator fault codes

    Note over App,ECU: Phase 2: Start Routine Execution
    App->>Transport: Start Routine (e.g. EPB Open: 31 01 03 A1)
    Transport->>ECU: 31 01 03 A1
    ECU-->>Transport: 71 01 03 A1 (Routine Accepted)

    Note over App,ECU: Phase 3: Status Polling Loop
    loop Every 500ms until Complete or Abort
        App->>Transport: Read Routine Status (22 01 02)
        Transport->>ECU: 22 01 02
        ECU-->>Transport: 62 01 02 <StatusByte>
        Note over App: Decode StatusByte >> 4:<br/>0x0: None<br/>0xC: In Progress<br/>0x1: Succeeded<br/>0x4: Aborted (Safety)<br/>0x6: Conditions Incorrect<br/>0x8: Timeout
    end

    alt Status == 0x01 (Succeeded)
        Note over App,ECU: Phase 4a: Graceful Completion
        App->>Transport: Stop Routine (31 02 03 A1)
        Transport->>ECU: 31 02 03 A1
        ECU-->>Transport: 71 02 03 A1 (Routine Stopped)
        Note over App: Display "Pads in Service Position"
    else Status in (0x40, 0x60, 0x80) or Error
        Note over App,ECU: Phase 4b: Abort & Recovery
        App->>Transport: Emergency Stop (31 02 03 A1)
        Transport->>ECU: 31 02 03 A1
        ECU-->>Transport: 71 02 03 A1
        Note over App: Display Specific Error & Preconditions
    end
```
