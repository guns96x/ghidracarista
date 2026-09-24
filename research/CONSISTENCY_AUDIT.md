# Consistency & Protocol Verification Audit

## 1. Scope
Audit of all addressing constants, routine IDs, and arithmetic formulas across:
- `handoff/VERIFIED_COMMANDS.json`
- `research/db/diagnostic_evidence.json`
- `research/db/vag_ecus.json`
- `core-diagnostic` Kotlin implementation

---

## 2. Arithmetic & Rule Check Results

| Rule Checked | Verification Result | Discrepancies Found | Status |
|---|---|---|---|
| **TP2.0 Setup CAN ID Formula**<br>$ID_{setup} = 0x200 + LogicalAddress$ | All 17 ECUs in `vag_ecus.json` evaluated against formula | 0 discrepancies | ✅ **PASS** |
| **CAN 11-bit Rx Derivation**<br>If $Tx \ge 0x795 \implies Rx = Tx + 8$<br>Else $Rx = Tx + 0x6A$ | Evaluated across all 11-bit CAN pairs | 0 discrepancies (e.g. Engine 7E0 $	o$ 7E8; EPB 752 $	o$ 7BC; BCM 70E $	o$ 778; ABS 713 $	o$ 77D; HVAC 746 $	o$ 7B0) | ✅ **PASS** |
| **CAN 29-bit Rx Derivation**<br>$Rx = Tx + 0x00020000$ | Evaluated across 29-bit CAN pairs | 0 discrepancies (Engine: `0x17FC0076` $	o$ `0x17FE0076`; Transmission: `0x17FC0077` $	o$ `0x17FE0077`) | ✅ **PASS** |
| **EPB Addressing Correctness**<br>Must target 0x752, NOT 0x746 | Confirmed `0x746` is HVAC, `0x752` is EPB | Old spec used 0x746. Fully corrected in DB and code. | ✅ **PASS** |
| **EPB Routine IDs**<br>Must use 0x03A1/0x03A0, NOT 0x0010/0x0011 | Confirmed from `libCarista.so.c` lines 111280 & 111232 | Old spec guessed 0x0010. Corrected to 0x03A1/0x03A0. | ✅ **PASS** |
| **BCM Addressing Correctness**<br>Must target 0x70E/0x778, NOT 0x709/0x773 | Confirmed from `libCarista.so.c` line 583389 | Old spec used 0x709. Corrected to 0x70E. | ✅ **PASS** |
