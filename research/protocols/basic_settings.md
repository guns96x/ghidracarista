# Basic Settings Specification

## 1. Overview
Basic settings run automated ECU self-calibration routines (e.g. throttle body alignment, steering angle calibration, headlight leveling).

---

## 2. TP2.0 Basic Setting
- Request: `31 <Subfunction> <RoutineID>` (`WriteVagCanBasicSettingCommand` @ line 104641)
  - `START_ROUTINE`: Subfunction `0x01` / `0xB9`
  - `WRITE_ADAPTATION`: Subfunction `0x10` / `0xBA`
  - `READ_ROUTINE_STATUS`: Subfunction `0x19` / `0xBB`

---

## 3. UDS Basic Setting
- Start Routine: `31 01 <RoutineID>`
- Stop Routine: `31 02 <RoutineID>`
- Status Query: `31 03 <RoutineID>`
