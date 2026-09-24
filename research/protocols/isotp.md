# ISO-TP (ISO 15765-2) Transport Protocol Specification

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
