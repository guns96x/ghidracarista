# Molecular Decomposition Strict Audit — Round 3

Commit audited: `d6b3ac88`

Status: **MAJOR IMPROVEMENT, NOT YET IMPLEMENTATION-READY**

The Round 2 bad cases were substantially improved:
- diagnostics/service tools are separated from the ordinary Setting schema;
- generic ECU fallback was removed;
- counts are no longer the old circular 470/8;
- current reported split is 314 EXACT_RESOLVED / 11 PARTIAL / 147 UNRESOLVED / 6 REJECTED_TEMPLATE.

However, independent validation found remaining correctness defects.

## 1. Synthetic fallback still leaks into EXACT_RESOLVED

`tools/extract_setting_instances.py` still synthesizes values for incomplete constructor arguments.

Concrete confirmed case:
- `FEAT_0086_BRAKE_DISC_DRYING`
- raw banned-ASM callsite: `0x14d0dc0`
- raw stack args: `[3596, null]`
- class: `VagUdsAdaptationSetting`
- current index nevertheless emits DID `0x0E0C`, byte `0`, mask `1` and marks it `EXACT_RESOLVED`.

This must be PARTIAL unless every required argument is actually proven.

## 2. Feature variants are being collapsed

The binary contains multiple legitimate implementations of the same setting key for different platforms/ECUs/whitelists.

Independent count:
- 314 current EXACT_RESOLVED catalog entries.
- **146 / 314** have more than one distinct binary variant.
- Some keys have up to **11 distinct variants**.

Examples:
- `car_setting_single_door_lock_remote`: 11 variants.
- `car_setting_coming_home_duration`: 9 variants.
- `car_setting_seat_belt_warning`: 9 variants.
- `car_setting_remote_with_ignition`: 9 variants.

Current extractor chooses the first “best” evidence and discards the remaining variants. That is incompatible with Carista-class applicability parity.

Required: one feature -> N exact variants, each retaining class, ECU, whitelist/applicability, DID/channel, byte/mask, interpretation and callsite.

## 3. Primary ARM64 register tracking is not control-flow safe

The primary extractor retains W8/W9 state across a huge function and does not prove that each value reaches the factory call on the same control-flow path without clobber.

Independent check found **103 current EXACT_RESOLVED entries** where the selected W8 or W9 assignment is more than 256 bytes before the BL callsite.

Examples:
- `auto_unlock`: selected W9 assignment is ~3760 bytes before call.
- `auto_unlock_parked`: ~5364 bytes.
- `coming_home_req_rls`: ~6788 bytes.

A distant register value is not exact constructor provenance.

Required: backward slice/basic-block dataflow per BL callsite with register-kill/call/branch awareness. If provenance cannot be proved, PARTIAL.

## 4. Command generation is still protocol/class-agnostic

Current mapping turns almost every non-`Channel` identifier into:
- read: `22 <id>`
- write: `2E <id>`

Independent check found **101 current command records** whose class/protocol is KWP/TP2.0/VagCan but command output is UDS `22/2E`.

Concrete example:
- `FEAT_0073_BEEP_ON_LOCK_KEY`
- class: `VagCanLongCodingSetting`
- protocol: KWP2000 / TP2.0 / CAN
- generated: `22F1A3 / 2EF1A3`
- existing direct evidence for TP2.0 long coding uses `1A 9A / 3B 9A`.

Command builders must be selected by concrete setting class/protocol and validated against exact request-builder evidence.

## 5. UDS adaptation DID is still defaulted to F1A3

Current EXACT_RESOLVED set contains **44 `VagUdsAdaptationSetting` entries with DID `0xF1A3`**.

The extractor initializes `did = "0xF1A3"` and leaves it there whenever the currently tracked argument is <=255 or otherwise unresolved.

For adaptation settings, an exact DID/channel must come from the constructor/request path. Do not use F1A3 as a generic fallback.

## 6. Impossible / unresolved values remain EXACT

Current EXACT_RESOLVED records include:
- 2 invalid/suspicious masks:
  - `remember_recirculating_air_state`: mask `-10`
  - `virtual_cockpit_color_1`: mask `65535`
- 4 entries with `UnknownVagSettingClass`
- 1 entry with missing whitelist/applicability source
- 179 entries with missing concrete interpretation/value semantics

A record cannot be implementation-ready if the setting class, applicability or value interpretation is unknown.

## Required remediation

1. Remove every remaining synthetic byte/mask/DID default from exact classification.
2. Introduce `SETTING_VARIANTS_INDEX.json`:
   - one canonical feature key;
   - all binary variants;
   - exact whitelist/applicability binding;
   - exact class/ECU/protocol/arguments/callsite per variant.
3. Do not collapse variants to the first match.
4. Replace global register-state extraction with callsite-local CFG/dataflow/backward slicing.
5. Generate commands by concrete class and exact request-builder behavior, not generic DID formatting.
6. `VagUdsAdaptationSetting` requires an explicitly proven DID; otherwise PARTIAL.
7. `UnknownVagSettingClass` can never be EXACT_RESOLVED.
8. Missing whitelist/applicability or missing value interpretation must block implementation readiness.
9. Validator must fail on:
   - any EXACT record using synthetic fallback;
   - any feature with discarded distinct variants;
   - KWP/TP2.0 class mapped to UDS 22/2E;
   - adaptation with unproven F1A3;
   - invalid mask width/value;
   - Unknown class;
   - missing applicability/value interpretation.

Do not optimize for a high EXACT count. Optimize for ground truth.
