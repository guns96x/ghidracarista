# ECU Coding & Long Coding Specification

## 1. Overview
ECU coding configures vehicle options, hardware variants, and market equipment.

---

## 2. TP2.0 Coding
- Read Request: `1A 9A` (`ReadVagCanLongCodingCommand`)
- Write Request: `3B 9A <CodingBytes...>` (`WriteVagCodingCommand` @ line 105028)
- Submodule Coding: `3B 9A <SubId> <CodingBytes...>` (`WriteVagSubmoduleCodingCommand` @ line 105280)

---

## 3. UDS Long Coding
- Read Request: `22 06 00` (or `22 F1 A0`)
- Write Request: `2E 06 00 <NewCodingBytes...>`
- Prerequisite: Extended Diagnostic Session (`10 03`) + Security Access (`27`) where required.
