# Security Architecture & Authorization Specification

## 1. Overview
Modern VAG diagnostic operations are protected by multi-tier security schemes:
1. **SecurityAccess (ISO 14229 Service `0x27`)**: Seed/Key challenge-response for write operations (Coding, Adaptations, Basic Settings).
2. **SFD (Schutz Fahrzeug Diagnose / Vehicle Diagnostic Protection)**: Offline or online token-based authorization introduced on MQB-evo platforms.

---

## 2. Standard UDS Security Access (`0x27`)
- Request Seed: `27 <Level>` (e.g. `27 01`, `27 03`, `27 05`)
- ECU Response: `67 <Level> <SeedBytes...>`
- Send Key: `27 <Level+1> <CalculatedKeyBytes...>`
- Positive Response: `67 <Level+1>`

---

## 3. SFD Commands Observed in libCarista.so

### Evidence
- **Binary**: `libCarista.so`
- **Decompiled C**: Lines 14358–14364 & `commands_evidence.json`
- **Classes**:
  - `VagUdsRequestSfdChallengeCommand`: `31 01 C0 08`
  - `VagUdsUnlockSfdCommand`: `31 01 C0 [Token]`
  - `VagUdsConfirmSfd2SettingCommand`: `31 01 C0 12 01`
  - `GetVagUdsSfd2SettingsCommand`: `31 01 06 A9 00`
- **Confidence**: `VERIFIED`

> [!NOTE]
> Per project guidelines, SFD bypass or proprietary server token generation is **NOT** implemented. The application architecture handles SFD at the protocol interface level by detecting SFD status and cleanly communicating lock conditions to the user without circumvention attempts.
