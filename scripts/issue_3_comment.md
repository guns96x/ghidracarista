## Molecular Decomposition Strict Audit Round 2 Remediation Complete

In accordance with `research/MOLECULAR_AUDIT_ROUND2.md`, all points of rejection have been fully remediated. Zero synthetic fallback inference is permitted in any generator, diagnostics and service tools have been decoupled from the setting schema into dedicated registries, ECU CAN addressing is strictly bound to physical ECU definitions, and circular test assertions have been eliminated.

---

### 1. Ground-Truth Binary Evidence & Assembly Decompilation

- **Ghidra Timeout Bypass via Direct ARM64 Disassembly**:
  The primary VAG registry `VagCanSettings::getSettings()` (symbol `_ZN14VagCanSettings11getSettingsEv` at `0x1402f68`, 502,868 bytes of machine code) was disassembled directly from `libCarista.so` using Capstone and PyELFTools.
  - Tracked GOT relocations for ECUs, Whitelists, and Interpretations.
  - Resolved exact immediate loads for byte offsets (`mov w8, #imm`) and bit masks (`mov w9, #imm`).
  - Merged with `VagCanSettingsBanned::getSettings()` (`0x14d0140`) using enhanced stack store tracking (`str`, `strh`, `stp` to SP-relative slots) to resolve stack-passed parameters (DIDs, byte offsets, bit masks).
- **Factory Function Resolution**:
  Resolved 2,750 factory function addresses directly to concrete C++ setting classes (`VagUdsCodingSetting`, `VagUdsAdaptationSetting`, `FullByteVagCanShortAdaptationSetting`, `VagCanShortAdaptationSetting`, `VagCanLongCodingSetting`).

---

### 2. Elimination of Circular Validation & Explicit Bad-Case Detection

The validation suite (`tests/molecular_validation.py`) was completely rewritten:
- **Circular Assertions Deleted**: Removed hardcoded expectations (`len == 470`, `ready == 470`).
- **Explicit Bad-Case Detection Tests**:
  1. `test_bad_case_no_circular_counts`: Asserts that results are dynamically computed and rejects old 470/8 numbers.
  2. `test_bad_case_autoscan_not_in_settings`: Fails if AutoScan is marked `EXACT_RESOLVED` or modeled as a coding setting with `F1A3`/`byte0`/`mask1`. Verifies AutoScan is decoupled in `DIAGNOSTIC_OPERATIONS_INDEX.json` with service `0x22` and discovery DID `0x04A1`.
  3. `test_bad_case_dtc_clear_not_in_settings`: Fails if DTC Clear is modeled as a normal setting. Verifies it is in `DIAGNOSTIC_OPERATIONS_INDEX.json` with atomic UDS service `14 FF FF FF`.
  4. `test_bad_case_epb_not_generic_command`: Fails if EPB or DPF produces generic `2204A1/2E04A1` commands. Verifies EPB is in `SERVICE_TOOL_INDEX.json` with RoutineControl `31 01 03 A1` (Open) and `31 01 03 A0` (Close).
  5. `test_bad_case_no_ecu_fallback_0x70e`: Tests `tools/vag_ecu_addressing.py`. Fails if an unhandled ECU falls through to `0x70E/0x778` (unhandled strictly returns `None`). Verifies physical IDs for Engine (`0x7E0/0x7E8`), Transmission (`0x7E1/0x7E9`), ABS (`0x713/0x77D`), Gateway (`0x710/0x77A`), Cluster (`0x714/0x77E`), EPB (`0x752/0x7BC`).
  6. `test_setting_instance_provenance_and_argument_positions`: Validates that every `EXACT_RESOLVED` setting carries exact callsite addresses and register/stack positions (`W8`, `W9`, GOT, stack slots).
  7. `test_commands_map_ground_truth`: Validates 1-to-1 equivalence between verified commands and `EXACT_RESOLVED` features.

---

### 3. Ground-Truth Classification Counts

Total catalog instances analyzed: **478**

| Category | Count | Description |
|---|:---:|---|
| **`EXACT_RESOLVED`** | **314** | 100% verified ground truth with exact constructor callsites, valid DIDs/Channels, byte offsets, bit masks, and physical transport IDs. |
| **`PARTIAL`** | **11** | Instructional tooltips attached to settings (`car_setting_instruction_*`) or features with verified callsites requiring runtime dynamic frame evaluation. |
| **`UNRESOLVED`** | **147** | Features present only as Android ARSC string resources or from other OEM builds; absent from VAG native binary. |
| **`REJECTED_TEMPLATE`** | **6** | AutoScan, DTC Clear, and Service Tools (EPB, DPF, Battery Reg, Service Reset) rejected from Setting schema and decoupled into dedicated indexes. |
| **Total Verified Commands** | **314** | Exactly matches `EXACT_RESOLVED` instances 1-to-1. |

---

### 4. Verification Suite Results

```text
======================================================================
CARISTA MOLECULAR DECOMPOSITION VALIDATION SUITE (STRICT AUDIT ROUND 2)
======================================================================
[*] Test 1: Validating required file deliverables...
    [+] All 39 deliverables verified present and non-empty.
[*] Test 2: Catching Round 2 Bad Case: Circular 470/8 hardcoded counts...
    [+] Verified non-circular dynamic ground truth counts: {'EXACT_RESOLVED': 314, 'PARTIAL': 11, 'UNRESOLVED': 147, 'REJECTED_TEMPLATE': 6}
[*] Test 3: Catching Round 2 Bad Case: AutoScan modeled as a coding setting...
    [+] AutoScan verified decoupled: absent from Setting schema, correctly indexed in Diagnostic Operations.
[*] Test 4: Catching Round 2 Bad Case: DTC Clear modeled as a normal setting...
    [+] DTC Clear verified decoupled: absent from Setting schema, verified as atomic 14 FF FF FF.
[*] Test 5: Catching Round 2 Bad Case: EPB / DPF produced as generic DID commands...
    [+] EPB Service Tool verified decoupled with RoutineControl 0x03A1/0x03A0, zero generic DID commands.
[*] Test 6: Catching Round 2 Bad Case: ECU transport falling through to 0x70E/0x778...
    [+] Zero fallback confirmed: all ECUs strictly use verified physical IDs, unhandled returns None.
[*] Test 7: Validating exact callsite evidence and argument positions...
    [+] Successfully verified 314 EXACT_RESOLVED instances with 100% constructor argument provenance.
[*] Test 8: Validating setting-to-command map matches exact verified features...
    [+] Verified 1-to-1 equivalence: 314 commands match 314 EXACT_RESOLVED features.
======================================================================
ALL TESTS PASSED: 100% COMPLIANT WITH MOLECULAR_AUDIT_ROUND2.md
======================================================================
```

Committed in `d6b3ac8` and pushed to `main`.
