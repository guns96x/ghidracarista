# Molecular Decomposition — Round 4 Remediation Report

Responds to `research/MOLECULAR_AUDIT_ROUND4.md` and GitHub issue #4. Issue #3 stays open.

Scope: software/data-pipeline correctness only. No binary was inspected or decompiled by hand, no new protocol
command was derived, and nothing here touches authentication, licensing, SFD or security-access behaviour. Every
value comes from the already-written dataflow extractor (`tools/vag_setting_dataflow.py`, reviewed and corrected
below), from committed evidence (`research/db/diagnostic_evidence.json`, `research/protocols/*.md`), or is left
blocked.

**Lower counts are the correct outcome.** The previous EXACT figures were produced by an extractor that could not be
reproduced. The counts in this document are *generated outputs*, not invariants; no validator asserts them.

## Generated status snapshot (output of the pipeline at this commit)

| Level | State | Count |
|---|---|---|
| Feature | `EXACT_RESOLVED` (exactly one variant, exact) | 31 |
| Feature | `AMBIGUOUS_MULTI_VARIANT` (≥2 variants, ≥1 exact) | 70 |
| Feature | `PARTIAL` | 197 |
| Feature | `UNRESOLVED` (no dataflow-proven callsite) | 174 |
| Feature | `REJECTED_TEMPLATE` (diagnostic/service operation) | 6 |
| Variant | `EXACT_VERIFIED` | 288 |
| Variant | `PARTIAL` | 1119 |
| Variant | `PROTOCOL_CONFLICT` (rejected) | 286 |

* Callsites / raw variants: 1693 (one variant per constructor callsite, none merged).
* Features with more than one variant: 140 — 70 have ≥1 exact variant and are `AMBIGUOUS_MULTI_VARIANT`; the other
  70 have no exact variant and are `PARTIAL`. **All 70 exact-bearing multi-variant features remain ambiguous**
  (no runtime selector exists in committed evidence). 34 features have more than one *exact* variant.
* Protocol conflicts: 286 variants rejected; **0 among exact/executable variants**. 34 features are blocked solely because every variant conflicts.
* Executable variants (command map entries): 161 — 93 `uds_did_rmw`, 68 `tp2_long_coding_rmw`.
* **Executable TP2/KWP adaptation variants: 0.** 113 `VagCanShortAdaptationSetting` variants exist; each is blocked
  (interpretation / channel / offset / mask / applicability argument not dataflow-proven). The ordered
  `31 B9 / 31 BA / modify / 31 BB / 31 BA` flow is attached to the 52 whose channel, byte position and mask *are* proven,
  marked non-executable.

## What changed, per audit item

### 1. Reproducible extraction
* `tools/vag_setting_dataflow.py` (WIP, reviewed) is now the single source of extraction. It records the **BL target
  (helper address)** separately from the PLT slot and GOT slot of the `__shared_ptr_emplace` call; the class and the
  forwarded argument types are parsed from that PLT symbol, so the factory map is evidence, not a lookup table.
* Function bounds come from `.dynsym` (address and size are pinned in `vag_setting_callsites.json`); the binary SHA-256
  (`fe6708565270f20c8622f2e4d0b520f8f4a0c65b2d14c104b1f0550635c13437`) and `extractor_version` are pinned in every artifact.
* `resolved_factories_map.json` is the exact map used (551 helpers, each keyed by its BL target).
* `tools/extract_all_variants_ground_truth.py` is now a pure projection of the two committed artifacts above; it no
  longer touches the binary or a textual window.
* `tests/molecular_reproducibility.py` re-runs the extraction twice and requires byte-identical results, equal to the
  committed files, then regenerates every downstream file and compares. `REPRODUCIBILITY_REPORT.json` pins SHA-256 of
  inputs, generators and outputs (LF-normalised, so checkout line endings do not matter).
* A variant whose factory is absent from the committed map, or whose class differs from the factory's class, gets the blocker
  `factory_not_reproducible_from_committed_map` and cannot be EXACT.

### 2. No first-variant collapse
* Canonical model is `Feature -> Variant[]`. `best = exact_v[0]` is gone. A feature is executable (`READY`) only if it has
  exactly one variant and it is exact.
* `SETTING_TO_COMMAND_MAP.json` (schema v2) has one entry **per exact variant**, carrying `variant_id`, the applicability
  identity (class, ECU object, whitelist, applicability list), ECU identity and `selection_required`. Nothing is chosen by
  source order, array order or id. Reordering the input is tested to change nothing.

### 3. Protocol consistency
* Per variant, four protocols must agree: setting class family, ECU object class (`VagUdsEcu`/`VagCanEcu`), ECU table
  entry, request builder. Disagreement ⇒ `PROTOCOL_CONFLICT`, non-executable. The command map's `protocol` is the request
  builder's; validators require it to equal the runtime transport protocol.
* Every conflict is a UDS-family class built on a `VagCanEcu` object: `VagUdsCodingSetting` (282) and `VagUdsOverCanSubmoduleCodingSetting` (4).
* `vag_ecu_addressing.resolve_ecu_transport` no longer attaches a same-named UDS ECU's CAN IDs to a KWP/TP2.0 ECU.

### 4. TP2/KWP adaptation flow
* Modelled as an ordered flow whose bytes are read from committed VERIFIED entries (`vag_tp20_set_adaptation_channel`
  `31 B9`, `vag_tp20_read_adaptation_data` `31 BA`, `vag_tp20_write_adaptation_data` `31 BB`): select channel → read →
  decode/modify → write → read-back verify. The synthetic `0x21/0x27` builder is removed and a validator rejects it.
* Judgement call: `research/protocols/adaptation.md` documents a `<Channel>` operand on `31 BA`; VERIFIED evidence only
  asserts the prefix, so no operand is emitted for it. The read-back repeats the `31 BA` read; re-selecting the channel is not evidenced.

### 5. CFG / dataflow provenance
Review of the WIP found one real defect, fixed here: predecessor queries evaluated the value at `p + 1` using the block
of `p + 1` instead of the predecessor's own block, so every cross-block query degenerated to `loop_in_definition_chain`.
It was *sound but blind* (never a false PROVEN). It now walks each predecessor's block, records every reaching
definition in the chain, and reports `merge_conflict` when they disagree. Also: unmodelled store forms (`st1`, …)
make a stack slot UNPROVEN instead of being ignored. Kept from the WIP: basic blocks + predecessor edges (conditional
branches), reaching definitions, caller-saved clobbering at `bl`/`blr`, stack-slot reaching stores with overlap detection, explicit
UNPROVEN reasons, `def_chain` per proven argument. Synthetic AArch64 tests cover each case, and the
cross-block test is shown to fail on the pre-fix code.

Rule: **every** constructor argument of a callsite must be PROVEN for the variant to be EXACT; anything else is
PARTIAL with the reason kept.

### 6. Validators
`tests/molecular_validation.py` has no expected result counts. `tools/molecular_invariants.py` checks relationships
(callsite ↔ variant ↔ factory ↔ index ↔ instance ↔ command map ↔ READY/BLOCKED) and recomputes every total.
A test lints the validators themselves for count-like integer comparisons. `tests/test_molecular_model.py` proves each
validator **fails** on corrupted copies: first-variant collapse, protocol mismatch, synthetic 0x21/0x27, missing factory,
heuristic (chain-less) EXACT, fabricated/borrowed ECU IDs, AutoScan as a setting, promoting an ambiguous feature to READY.

## Evidence tiers used for request builders
| Class | Flow | Evidence |
|---|---|---|
| `VagCanShortAdaptationSetting` | `tp2_adaptation_channel_flow` | `diagnostic_evidence.json` VERIFIED: 31 B9 / 31 BA / 31 BB |
| `VagCanLongCodingSetting` | `tp2_long_coding_rmw` | VERIFIED: `1A 9A` read, `3B 9A` write |
| `VagUdsCodingSetting` | `uds_did_rmw` | `protocols/uds.md` (22/2E, cites `WriteDataByIdentifierCommand::getRequest`) + `protocols/coding.md` (`22 06 00`) bound to the constructor's fixed id 0x600 — documentation tier, not the VERIFIED table |
| `VagUdsAdaptationSetting` | `uds_did_rmw` | `protocols/uds.md`; DID from the constructor argument |

The old `22 F1 A3 / 2E F1 A3` for UDS coding is dropped: the constructor's fixed id is 0x600 and `coding.md` documents
`22 06 00`; F1A3 has no committed support. Other classes have no committed builder evidence and stay blocked
(`no_request_builder_evidence[...]`). Security Access/SFD needs are not established; the flows carry a `security_note`
and model no unlock.

## Known limits (deliberately not papered over)
* Extraction is conservative: a stack temporary is UNPROVEN when any call sits between its store and its use, which
  blocks many integer arguments. Interpretations/applicability lists passed on the stack are UNPROVEN by construction.
  This is why the TP2 adaptation set is empty of executable variants. Relaxing it needs escape analysis, i.e. new analysis, not new guesses.
* The new extractor reproduces 1693 callsites; the previous, non-reproducible dataset listed 1829. 150 old callsites
  (mostly `FullByteVagCanShortAdaptationSetting` and classes named only in the old map, with values such as
  `Channel 63 / byte 255 / mask 1` taken from a textual window) are **not** reproduced, and 61 old keys appear nowhere in
  the new data. Those features moved to `UNRESOLVED` (`NO_PROVEN_CALLSITE`) — absence of proof, not proof of absence.
  Whether they are genuine factories the extractor's helper rule rejects is a question for the Round 5 audit.
* `CLASS_SEMANTICS` (int-role order per class) is taken as-is from the WIP's cited decompile locations; it was not re-verified here.
* No runtime variant selector is specified in committed evidence, so multi-variant features stay ambiguous.

## Compatibility / deprecation
* `SETTING_TO_COMMAND_MAP.json`: schema v2. v1 keys `read_command_hex`, `write_command_hex`, `ecu_address`,
  `ecu_tx_id`, `ecu_rx_id`, `service_read`, `service_write` are removed; entries are per variant (`request_flow`, `ecu`,
  `applicability_identity`). v1 entries were per feature and collapsed variants.
* `SETTING_INSTANCE_INDEX.json`: `resolution_status` gains `AMBIGUOUS_MULTI_VARIANT`; `variant_ids` lists every variant.
* `READY_FEATURES.json` now means "executable with no variant selection"; `BLOCKED_FEATURES.json` gains `state`, `blocking_class`
  (`BLOCKED_EVIDENCE`, `AMBIGUOUS_VARIANT_SELECTION`, `PROTOCOL_CONFLICT_REJECTED`, `NO_PROVEN_CALLSITE`, `NOT_A_SETTING`) and `blocker_summary`.
* The generator no longer reads READY/BLOCKED as its own catalog input (it was circular); the feature list comes from `research/features/FEATURE_CATALOG.json`.
* `FEATURE_DEPENDENCY_GRAPH.*` is regenerated variant-aware with no defaulted ECU/DID/whitelist/platform values.
* Deprecated (hard-exit stubs): `tools/extract_setting_instances.py`, `tools/build_ground_truth_setting_index.py`,
  `scripts/generate_ready_blocked.py`.

## Exact regeneration commands
```
python tools/vag_setting_dataflow.py                       # needs extracted/arm64/lib/arm64-v8a/libCarista.so (SHA-256 pinned)
python tools/extract_all_variants_ground_truth.py
python tools/build_variants_and_settings_index.py
python tools/generate_feature_dependency_graph.py
python tests/molecular_reproducibility.py --write-report   # then rerun without the flag
python tests/molecular_validation.py
python tests/test_molecular_model.py
```
Without the binary, `molecular_reproducibility.py --allow-missing-binary` verifies every downstream step from committed
inputs and says explicitly that binary re-extraction was skipped.
