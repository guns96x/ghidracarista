# Molecular Decomposition Strict Audit — Round 4

Commit audited: `ab8d67da`

Status: **NOT IMPLEMENTATION-READY**

Round 3 remediation improved the dataset substantially:
- feature counts are now 208 EXACT_RESOLVED / 106 PARTIAL / 158 UNRESOLVED / 6 REJECTED_TEMPLATE;
- 1829 binary variants are preserved;
- adaptation F1A3 defaults, Unknown classes, invalid masks and missing interpretations were removed from the current EXACT feature set.

However, independent verification found four remaining structural blockers.

## 1. Committed extraction is not reproducible

`tools/extract_all_variants_ground_truth.py` resolves classes using:

`cls = factory_classes.get(target_addr)`

where `factory_classes` comes from committed `research/molecular/resolved_factories_map.json`.

But in committed `all_binary_variants_ground_truth.json`:

- total raw variants: **1829**
- variants whose `factory_address` exists in committed `resolved_factories_map.json`: **3**
- variants whose `factory_address` is absent from the committed factory map: **1826**

Example:
- raw variant `car_setting_ads_engine_menu`
- `factory_address = 0x1ba28c8`
- claimed class: `VagUdsCodingSetting`
- committed `resolved_factories_map.json` has no `0x1ba28c8` entry.

Therefore the committed extractor + committed factory map cannot regenerate the committed raw dataset.

### Required
- store the actual BL target separately from any GOT/relocation slot;
- commit the exact factory-resolution map used to generate the dataset;
- add a reproducibility test that reruns extraction and verifies byte-for-byte/semantic equivalence;
- no variant may be EXACT if its class cannot be reproduced from committed evidence.

## 2. Multi-variant data is preserved, but executable maps still collapse variants

`SETTING_VARIANTS_INDEX.json` now preserves variants, but `SETTING_INSTANCE_INDEX.json`, `SETTING_TO_COMMAND_MAP.json`, and `READY_FEATURES.json` still select:

`best = exact_v[0]`

Independent counts:
- **134 setting keys** have more than one exact verified variant.
- **79 command-map entries** represent a feature that has multiple exact variants but expose only the first selected variant.

Example:
`car_setting_alarm` has exact implementations across different ECU/class/whitelist combinations, but the command map publishes only one.

This is unsafe for runtime applicability.

### Required
Do not publish a single executable command for a multi-variant feature.
Either:
- make the runtime command map variant-specific, keyed by whitelist/applicability/ECU identity; or
- keep the canonical feature non-executable until a variant selector resolves exactly one applicable variant.

## 3. Protocol model is internally contradictory

Among exact variants:
- **240 variants** have `command.protocol != ecu.protocol`.

Typical example:
- class: `VagUdsCodingSetting`
- command: UDS `22F1A3 / 2EF1A3`
- ECU object: `VagCanEcu::CENTRAL_ELEC`
- ECU protocol field: `KWP2000 / TP2.0 / CAN`

This means class, ECU type, transport and command builder do not agree.

The current command map also writes `protocol = best["ecu"]["protocol"]` rather than the class-specific command builder's protocol, producing entries that say KWP/TP2.0 while carrying UDS 22/2E commands.

### Required
- establish protocol from the exact setting object + ECU object + request-builder combination;
- reject any exact variant where class/ECU/request-builder protocols conflict;
- command-map protocol must equal the exact request-builder protocol;
- add validator: `variant.command.protocol == runtime transport protocol`.

## 4. KWP/TP2.0 adaptation builder contradicts already VERIFIED command evidence

The new builder says for `VagCanShortAdaptationSetting`:
- read: `0x21`
- write: `0x27`

There are **16 current executable ShortAdaptation command entries** generated this way.

But committed direct VERIFIED Carista evidence states:
- select adaptation channel: `31 B9`
- read adaptation data: `31 BA`
- write adaptation data: `31 BB`

Sources already committed in `research/db/diagnostic_evidence.json`:
- `SetVagCanAdaptationChannelCommand::getRequest()`
- `ReadVagCanAdaptationDataCommand::getRequest()`
- `WriteVagCanAdaptationDataCommand::getRequest()`

Therefore the new ShortAdaptation builder is not evidence-grounded and contradicts stronger existing evidence.

### Required
Model TP2/KWP adaptation as a flow, not one synthetic request:
1. select channel (`31 B9 <channel>`)
2. read (`31 BA`)
3. modify interpreted value
4. write (`31 BB <value>`)
5. read-back verification

## 5. “Control-flow safe backward slicing” is not actually CFG/dataflow safe

Current extractor:
- takes at most the previous 50 instructions;
- stops only at `blr`, unconditional `b`, or `ret`;
- does not construct a CFG;
- does not model conditional branches;
- does not stop/kill caller-saved registers across ordinary `bl` calls;
- forward-simulates a textual window.

This is a bounded local heuristic, not callsite-local CFG/dataflow proof.

### Required
Either:
- implement actual basic-block / predecessor-aware slicing with register definitions and call clobber rules; or
- downgrade values recovered only by the heuristic to PARTIAL.

## 6. Validator became circular again

`tests/molecular_validation.py` now hardcodes:
- EXACT_RESOLVED == 208
- PARTIAL == 106
- UNRESOLVED == 158
- REJECTED_TEMPLATE == 6

These numbers are outputs, not invariants.

### Required
Remove hardcoded result counts. Validate relationships and evidence properties instead.

## Acceptance conditions for Round 4

The molecular dataset is accepted only when:

1. extraction is reproducible from committed scripts + committed maps;
2. no executable feature collapses unresolved multiple variants;
3. protocol/class/ECU/request-builder agree per variant;
4. TP2/KWP adaptation uses the verified 31 B9 / 31 BA / 31 BB flow;
5. heuristic slices are not labeled exact unless dataflow provenance is proven;
6. validator has no hardcoded expected result counts.

Do not optimize for a high EXACT count. Correctly lowering the exact count is acceptable.
