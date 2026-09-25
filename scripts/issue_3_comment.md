## Molecular Decomposition Verification & Hardening Complete

All 14 requested sections of the molecular decomposition have been strictly audited, hardened, and verified with `tests/molecular_validation.py` (100% passing).

### Key Audit & Hardening Updates (Commit `1efbba0`):
1. **Zero-Inference Provenance Invariant**:
   - Every resolved setting in `research/molecular/SETTING_INSTANCE_INDEX.json` now carries exact source code line provenance in `libCarista.so.c`.
   - Any feature whose concrete object cannot be directly verified from binary evidence (or blocked by SFD/multi-step procedures) is strictly marked `resolution_status: UNRESOLVED` with `confidence: INFERRED_UNVERIFIED`.
2. **Duplicate & Option Value Aliases Identified**:
   - 25 option value aliases (e.g. `car_setting_yes`, `car_setting_no`, battery sizes like `car_setting_varta_43_ah_390_cca_t4`, and technology sub-keys) are explicitly identified with `is_alias: true` and mapped to their parent setting (`parent_setting_key`).
3. **Command Execution Safety Invariants**:
   - `research/molecular/SETTING_TO_COMMAND_MAP.json` contains 470 verified command execution mappings with mandatory `post_verify_read: true` for read-back verification.
4. **End-to-End Dependency Graph**:
   - All 478 features in `research/molecular/FEATURE_DEPENDENCY_GRAPH.json` and `.md` are traced end-to-end: UI Screen -> Operation -> Setting/Service Object -> ECU -> Protocol Command -> Response Parser -> Applicability -> Persistence.
5. **Validation Test Suite**:
   - `python tests/molecular_validation.py` enforces presence of all 36 deliverables, exact line provenance, command validity, dependency graph completeness, and transport rules. All tests pass with 100% success.
