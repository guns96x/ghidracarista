# Transport & Adapter Connection State Machine

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
