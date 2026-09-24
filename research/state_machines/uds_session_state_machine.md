# UDS Diagnostic Session State Machine

## 1. Overview
Models diagnostic session transitions (ISO 14229 Service `0x10`), security access authorization (`0x27`), and tester present keep-alive loops (`0x3E`).

### Evidence
- **Binary**: `libCarista.so`
- **Classes**: `VagUdsEcu`, `TesterPresentCommand`
- **Confidence**: `VERIFIED`

---

## 2. Mermaid State Diagram

```mermaid
stateDiagram-v2
    [*] --> DEFAULT_SESSION: Physical Link Established (10 01)

    state DEFAULT_SESSION {
        [*] --> IDLE_DEFAULT
        IDLE_DEFAULT --> READ_DTC: 19 02 8D
        IDLE_DEFAULT --> READ_IDENTIFICATION: 22 F1 8C / F1 89 / F1 9E
        IDLE_DEFAULT --> READ_LIVE_DATA: 22 <DID>
    }

    DEFAULT_SESSION --> EXTENDED_SESSION: Request 10 03 (Extended Diagnostic)
    
    state EXTENDED_SESSION {
        [*] --> SESSION_ACTIVE
        SESSION_ACTIVE --> KEEP_ALIVE_LOOP: Start Timer (2000ms)
        KEEP_ALIVE_LOOP --> KEEP_ALIVE_LOOP: Send 3E 80
        
        SESSION_ACTIVE --> SECURITY_LOCKED: Requires Privileged Access
        
        state SECURITY_LOCKED {
            [*] --> REQUEST_SEED: 27 01 / 27 03 / 27 05
            REQUEST_SEED --> AWAIT_SEED: 67 <Level> <Seed>
            AWAIT_SEED --> SEND_KEY: 27 <Level+1> <Key>
            SEND_KEY --> SECURITY_UNLOCKED: 67 <Level+1> (Success)
            SEND_KEY --> REQUEST_SEED: NRC 0x35 / 0x36 (Failed / Delay)
        }

        SECURITY_UNLOCKED --> WRITE_CODING: 2E 06 00 <Bytes>
        SECURITY_UNLOCKED --> WRITE_ADAPTATION: 2E <DID> <Bytes>
        SECURITY_UNLOCKED --> START_ROUTINE: 31 01 <RoutineID>
        
        START_ROUTINE --> ROUTINE_RUNNING: 71 01 <RoutineID>
        ROUTINE_RUNNING --> ROUTINE_RUNNING: Poll 22 01 02
        ROUTINE_RUNNING --> ROUTINE_FINISHED: Status == 0x10 (Success)
        ROUTINE_RUNNING --> ROUTINE_ERROR: Status in (0x40, 0x60, 0x80)
    }

    EXTENDED_SESSION --> DEFAULT_SESSION: 10 01 (Explicit exit) or P3 Timeout (No 3E 80 for 5000ms)
    EXTENDED_SESSION --> PROGRAMMING_SESSION: Request 10 02 (Firmware update)
```

---

## 3. Session Keep-Alive Invariants
- When in `EXTENDED_SESSION` (`0x03`), the background dispatcher **must** dispatch `3E 80` every 2,000 ms.
- If an active diagnostic command is currently awaiting a response from the ECU, the TesterPresent packet is deferred until the bus is free.
- On receiving Negative Response Code `0x78` (`requestCorrectlyReceived-ResponsePending`), the P2 timer is extended to `P2*` (5,000 ms).
