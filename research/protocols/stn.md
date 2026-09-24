# STN (Scantool / OBDLink) Protocol Specification

## 1. Overview
STN chipsets (STN11xx, STN21xx by Scantool.net / OBDLink) provide high-throughput extensions to the standard ELM327 command set.

---

## 2. ST Commands

### Evidence
- **Binary**: `libCarista.so`
- **Decompiled C**: `libCarista.so.c` (Lines 1013023–1013400)
- **Function**: `ElmSimulator::processStCommand`
- **Virtual Address**: `0x18a0758`
- **Confidence**: `VERIFIED`

### Verified Command Set
1. **`ST DI`**: Device Information.
   - Returns hardware ID, firmware version (e.g. `STN1170 v4.2.1`).
2. **`ST P <protocol>`**: Set ST protocol profile.
3. **`ST PX <param>`**: Extended protocol parameter setup.
4. **`ST CSM <mode>`**: CAN Segmentation Management (enables hardware ISO-TP reassembly in firmware).
5. **`ST CMM`**: CAN Monitoring Mode.

---

## 3. Performance Advantages in Diagnostic Stack
- **Buffer Depth**: STN chips support up to 4 KB internal RX buffer (compared to 512 bytes on standard ELM327).
- **Baud Rate Acceleration**: Supports UART baud rates up to 2 Mbps (`ST SBR 2000000`).
- **Hardware ISO-TP**: When `ST CSM` is active, the adapter handles Flow Control (`0x30`) frames autonomously, relieving the Android host from strict 50ms timing constraints.
