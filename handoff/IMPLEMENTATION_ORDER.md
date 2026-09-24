# Recommended Implementation Order for Android Diagnostic Application

This roadmap enables an engineering AI or human developer to implement the complete Carista feature set in logical, testable milestones.

---

## Stage 1: Physical Transport & Protocol Handshake (Days 1–2)
- [x] BLE GATT Characteristic & Bluetooth Classic SPP Socket
- [x] ELM327 / STN / vLinker initialization state machine (`AT Z`, `AT SP 6`, `AT E0`, `AT H1`)
- [x] ISO-TP (ISO 15765-2) Single Frame (SF), First Frame (FF), Flow Control (FC), Consecutive Frame (CF)

## Stage 2: Vehicle & ECU Discovery Engine (Days 3–4)
- [ ] Connect Gateway (`AT SH 710`, `AT CRA 77A`)
- [ ] Read VIN via DID `0xF190`
- [ ] Read Gateway Installation List via DID `0x04A1` (4 bytes per installed module)
- [ ] Poll module identification (DID `0xF187` Part No, DID `0xF189` SW Ver, DID `0xF15B` ASAM ODX)

## Stage 3: Core Diagnostic Capabilities (Days 5–7)
- [ ] Multi-ECU AutoScan (`CheckCodesOperation` / `FullScanOperation`)
- [ ] UDS DTC extraction via Service `0x19 0x02 0x8D`
- [ ] DTC decoding into standard OBD-II (P/C/B/U) and VAG decimal codes
- [ ] DTC clearing via Service `0x14 FF FF FF`

## Stage 4: Service Tools Suite (Days 8–10)
- [ ] EPB Service Retract & Close (`31 01 03 A1` / `31 01 03 A0` on ECU `0x752`)
- [ ] DPF Forced Regeneration (`31 01 05 3D 04 00 00` on ECU `0x7E0`)
- [ ] Battery Registration (Ah, AGM/EFB, serial writing via `2E` on ECU `0x710`)
- [ ] Service Interval Reset (Oil & inspection interval reset on ECU `0x714`)
- [ ] TPMS Sensor ID reading & relearn

## Stage 5: Live Data Monitoring (Days 11–12)
- [ ] Real-time polling engine for engine RPM, coolant, oil temp, boost, battery voltage
- [ ] DPF soot mass live monitoring

## Stage 6: Customizations & Coding Engine (Days 13–16)
- [ ] Long Coding reader & writer (DID `0xF1A3`)
- [ ] Bitwise setting modifier (`Setting::extractValue` & `Setting::setValue`)
- [ ] Whitelist & bounds verification against vehicle configuration
- [ ] Automatic pre-coding backup and rollback engine
