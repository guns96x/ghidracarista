# Strict Feature Validation — Current Ground Truth

Date: 2026-09-25

## Result

The existing claim that all 478 catalog features are VERIFIED / Production-Ready is invalid.

### Catalog construction audit

`tools/build_feature_catalog.py` creates the catalog as follows:

- 6 explicit core operations are manually defined.
- 472 `FEAT_*` customization entries are generated from `car_setting_*` string literals.
- For those 472 entries, ECU assignment is inferred from feature-name keywords in `determine_ecu()`.
- Vehicle models, years, protocols, sessions, prerequisites, write/read operations, allowed values, scaling and confidence are filled from generic templates.
- Every generated customization is then assigned `confidence = VERIFIED` and `status = Production-Ready`.

Therefore the 472 generated customization records prove only that the corresponding internal setting-name literal exists in the analyzed Carista binary/resources. They do NOT prove the per-feature ECU, coding/adaptation offset, DID/channel, value map, applicability, prerequisites or write sequence.

`scripts/generate_ready_blocked.py` also does not validate evidence. It marks nearly every entry READY unless it matches a small hard-coded blocker list. Consequently the previous 470 READY / 8 BLOCKED split is not an evidence-backed readiness result.

## Strict status of the six explicit core operations

| Feature | Strict static status | What is directly supported |
|---|---|---|
| DIAG_AUTOSCAN | CONFIRMED_CORE | Gateway discovery `22 04 A1` / TP2.0 `1A 9F`, DTC read evidence exists |
| DIAG_CLEAR_DTC | CONFIRMED_CORE | UDS clear `14 FF FF FF` with direct evidence |
| TOOL_EPB_SERVICE | PARTIALLY_CONFIRMED | Open/close/stop routine requests and ECU addressing are directly evidenced; full prerequisites/applicability still require proof/live validation |
| TOOL_DPF_REGENERATION | PARTIALLY_CONFIRMED | Stationary/driving routine request bytes are directly evidenced; full prerequisite/DID/security/applicability flow is not fully proven |
| TOOL_BATTERY_REGISTRATION | EXISTS_NOT_IMPLEMENTATION_READY | BatteryRegOperation / VagUdsBatteryRegOperation classes exist, but current evidence export does not prove complete per-platform DIDs/value mapping/write flow |
| TOOL_SERVICE_RESET | EXISTS_NOT_IMPLEMENTATION_READY | ServiceIndicatorOperation exists, but current evidence export does not prove a complete VAG reset command matrix for all variants |

## Directly evidenced protocol primitives

The current `research/db/diagnostic_evidence.json` directly supports, among others:

- Gateway UDS discovery: `22 04 A1`
- Gateway TP2.0 discovery: `1A 9F`
- UDS DTC read: `19 02 8D`
- TP2.0 DTC reads: `18 02 FF 00`, `18 00 FF 00`
- UDS clear DTC: `14 FF FF FF`
- EPB open/close/stop routines: `31 01/02 03 A1/A0`
- Routine status: `22 01 02`
- DPF stationary regen: `31 01 05 3D 04 00 00`
- DPF driving regen: `31 01 03 05 04 00 00`
- ECU identification DIDs currently listed in the evidence DB
- TP2.0 long coding read/write primitives
- TP2.0 adaptation select/read/write primitives
- Extended diagnostic session and TesterPresent

These primitives do not automatically prove all 472 named customizations.

## Requirement for confirming every customization

A generated `FEAT_*` entry becomes implementation-confirmed only when its exact Carista setting object is resolved to evidence for:

1. exact ECU / submodule;
2. exact protocol variant;
3. exact read source (coding byte/bit, DID, adaptation channel, routine, local identifier, etc.);
4. exact write source;
5. byte/bit offset or DID/channel/routine ID;
6. value enum/range/scaling;
7. applicability rules (part number/SW/HW/ASAM/whitelist);
8. required session/security;
9. prerequisites for dangerous operations;
10. response/read-back validation;
11. source location/XREF or extracted asset record.

No generic inference from the setting name is acceptable.

## App implementation gate

Until the per-feature proof exists:

- use confirmed protocol primitives and confirmed core read operations;
- show unproven customizations in the research catalog only;
- do not enable their write actions in the Android app;
- never treat `READY_FEATURES.json` as authoritative.

The source of truth for app enablement must become a newly generated strict feature index based on per-feature evidence.
