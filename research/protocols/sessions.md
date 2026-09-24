# Diagnostic Sessions & Keep-Alive Lifecycle

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
