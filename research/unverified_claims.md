# Unverified & Deprecated Claims Log

This archive records claims from prior drafts or general internet sources that **lack binary verification** in `libCarista.so` or were proven incorrect during reverse engineering.

---

## 1. EPB Routine IDs `0x0010`, `0x0011`, `0x0012`
- **Origin**: Common internet forum conjecture for generic OBD tools.
- **Status**: `REFUTED`
- **Reason**: Disassembly of `StartVagUdsParkingBrakeOpenCommand` (@ `0x111280`) and `StartVagUdsParkingBrakeCloseCommand` (@ `0x111212`) definitively proves that VAG UDS uses Routine IDs **`0x03A1`** (Open) and **`0x03A0`** (Close).

---

## 2. BCM CAN ID `0x709` / `0x773`
- **Origin**: Outdated draft documentation.
- **Status**: `REFUTED`
- **Reason**: Central Electronics in VAG UDS is assigned transmitter ID **`0x70E`** and receiver ID **`0x778`** (`VagUdsEcu::initialize` line 583389). CAN ID `0x709` does not route to BCM on standard MQB architecture.

---

## 3. Oil Reset Adaptation DIDs `0x2260` & `0x2261`
- **Origin**: Model-specific cluster adaptation note.
- **Status**: `UNVERIFIED / HYPOTHESIS`
- **Reason**: While present on some Siemens/VDO cluster variants, modern MQB clusters utilize WSC channel routines or DIDs under `0x05xx` / `0x2Axx`. Must not be written without target vehicle cluster verification.
