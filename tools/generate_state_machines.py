import os

SM_DIR = r"d:\ghidracarista\research\state_machines"

def main():
    os.makedirs(SM_DIR, exist_ok=True)
    print("Generating State Machine documentation in research/state_machines/...")

    # 1. connection_lifecycle.md
    with open(os.path.join(SM_DIR, "connection_lifecycle.md"), "w", encoding="utf-8") as f:
        f.write("""# Transport & Adapter Connection State Machine

## 1. Overview
The connection state machine models the physical and logical link between the Android host application, the OBD adapter microcontroller (ELM327 / STN / vLinker), and the vehicle's CAN bus.

### Evidence
- **Binary**: `libCarista.so`
- **Class**: `ConnectionManager`
- **Methods**: `establishConnection`, `ensureConnection`, `resetConnection`, `hibernateElmChip` (Lines 1347172–1347445)
- **Confidence**: `VERIFIED`

---

## 2. Mermaid State Diagram

```mermaid
stateDiagram-v2
    [*] --> DISCONNECTED

    DISCONNECTED --> BLUETOOTH_CONNECTING: User selects adapter / Auto-connect
    BLUETOOTH_CONNECTING --> ADAPTER_INIT: RFCOMM Socket / BLE GATT Connected
    BLUETOOTH_CONNECTING --> ERROR_RECOVERY: Connection timeout / GATT 133

    state ADAPTER_INIT {
        [*] --> SEND_RESET: AT Z
        SEND_RESET --> DISABLE_ECHO: AT E0
        DISABLE_ECHO --> CONFIGURE_FORMATTING: AT L0 / AT S0 / AT H1
        CONFIGURE_FORMATTING --> QUERY_ADAPTER_TYPE: ATI / AT @1 / ST DI / AT I
        QUERY_ADAPTER_TYPE --> ADAPTER_READY
    }

    ADAPTER_INIT --> BUS_INIT: Adapter identified (Standard / STN / vLinker / EVO)
    ADAPTER_INIT --> ERROR_RECOVERY: Adapter non-responsive / Unknown clone

    state BUS_INIT {
        [*] --> SET_PROTOCOL: AT SP 6 (11-bit) or AT SP 7 (29-bit)
        SET_PROTOCOL --> TEST_PING: 0100 (OBD2 Ping) or 22 F1 90 (UDS Ping)
        TEST_PING --> BUS_ACTIVE: Bus response received
        TEST_PING --> PROTOCOL_FALLBACK: Bus Init Error / NO DATA
        PROTOCOL_FALLBACK --> SET_PROTOCOL: Try AT SP B (TP2.0) or K-Line
    }

    BUS_INIT --> ECU_COMMUNICATION: Gateway ping successful
    BUS_INIT --> ERROR_RECOVERY: All protocols failed

    state ECU_COMMUNICATION {
        [*] --> ECU_DISCOVERY: Read Gateway List (22 04 A1 / 1A 9F)
        ECU_DISCOVERY --> ECU_IDLE: Target ECU Selected
        ECU_IDLE --> RUN_COMMAND: User/Diagnostic Action
        RUN_COMMAND --> ECU_IDLE: Success
        RUN_COMMAND --> POKE_ECU: No response (P2 timeout)
        POKE_ECU --> ECU_IDLE: Keepalive poke ok
    }

    ECU_COMMUNICATION --> DISCONNECTING: User disconnects / App background
    ECU_COMMUNICATION --> ERROR_RECOVERY: Bus mute / Connection lost

    state ERROR_RECOVERY {
        [*] --> RESET_COMMUNICATOR: Reset buffers
        RESET_COMMUNICATOR --> RECONNECT: Retry count < 3
        RESET_COMMUNICATOR --> HIBERNATE: Retry count >= 3
    }

    ERROR_RECOVERY --> BLUETOOTH_CONNECTING: Retry
    ERROR_RECOVERY --> DISCONNECTED: Abort / Fatal Error

    DISCONNECTING --> HIBERNATE: AT LP (Low Power)
    HIBERNATE --> DISCONNECTED: Socket closed
    DISCONNECTED --> [*]
```

---

## 3. State Invariants & Recovery Policies

| State | Timeout | Retry Policy | Fallback Action |
| :--- | :--- | :--- | :--- |
| `BLUETOOTH_CONNECTING` | 10,000 ms | 2 retries | Abort with `BluetoothConnectionFailed` |
| `ADAPTER_INIT` | 2,000 ms per AT command | 3 retries | Reset via DTR/RTS or close socket |
| `BUS_INIT` | 5,000 ms | Cycle protocols: 6 -> 7 -> B | Fallback to ISO 9141 / KWP K-Line |
| `ECU_COMMUNICATION` | P2 (50ms), P2* (5000ms)| 1 retry on NRC 0x78 | Drop session to Default |
| `ERROR_RECOVERY` | 3,000 ms backoff | Max 3 attempts | Call `hibernateElmChip` and disconnect |
""")

    # 2. uds_session_state_machine.md
    with open(os.path.join(SM_DIR, "uds_session_state_machine.md"), "w", encoding="utf-8") as f:
        f.write("""# UDS Diagnostic Session State Machine

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
""")

    # 3. service_routine_state_machine.md
    with open(os.path.join(SM_DIR, "service_routine_state_machine.md"), "w", encoding="utf-8") as f:
        f.write("""# Service Routine Execution State Machine (EPB / DPF)

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
""")

    print(f"Generated all state machine markdown documents in {SM_DIR}.")

if __name__ == "__main__":
    main()
