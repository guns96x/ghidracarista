# ECU Adaptation Channels Specification

## 1. Overview
Adaptation adjusts calibrated operating parameters (e.g. throttle alignment, battery capacity, inspection intervals).

---

## 2. TP2.0 Adaptation
- Channel Select: `31 B9 <Channel>` (`SetVagCanAdaptationChannelCommand` @ line 104450)
- Pre-Read / Read: `31 BA <Channel>` (`ReadVagCanAdaptationDataCommand`)
- Write: `31 BB <Data>` (`WriteVagCanAdaptationDataCommand`)

---

## 3. UDS Adaptation
- Read Request: `22 <DID>` (e.g. DID `0x06A9`, `0x2Axx`)
- Write Request: `2E <DID> <DataBytes>` (`WriteDataByIdentifierCommand` @ line 89383)
