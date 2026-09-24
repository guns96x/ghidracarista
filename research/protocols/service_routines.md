# Service Routines Specification (EPB, DPF, Battery)

## 1. Electronic Parking Brake (EPB) Service Mode

### Evidence
- **Binary**: `libCarista.so`
- **Decompiled C**: Lines 111185–111400
- **Classes**: `StartVagUdsParkingBrakeOpenCommand`, `StartVagUdsParkingBrakeCloseCommand`, `StopVagUdsParkingBrakeOpenCommand`, `StopVagUdsParkingBrakeCloseCommand`
- **Target ECU**: `PARKING_BRAKE` (VAG Address `0x53`, UDS TX: `0x752`, RX: `0x7BC`)
- **Confidence**: `VERIFIED`

### Verified Command Bytes
| Operation | Action | UDS Request Bytes | Expected Response | Evidence Line |
| :--- | :--- | :--- | :--- | :--- |
| **Open Brake** (Pads Replacement)| Start | `31 01 03 A1` | `71 01 03 A1` | line 111280 |
| **Open Brake** | Stop | `31 02 03 A1` | `71 02 03 A1` | line 111400 |
| **Close Brake** (Test/Normal) | Start | `31 01 03 A0` | `71 01 03 A0` | line 111212 |
| **Close Brake** | Stop | `31 02 03 A0` | `71 02 03 A0` | line 111351 |

---

## 2. Diesel Particulate Filter (DPF) Regeneration

### Evidence
- **Binary**: `libCarista.so`
- **Decompiled C**: Lines 111113–111160
- **Class**: `StartVagDpfRegenCommand`
- **Target ECU**: `VagUdsEcu::ENGINE` (`0x01`, TX: `0x7E0`, RX: `0x7E8`)
- **Confidence**: `VERIFIED`

### Verified Command Bytes
| Regen Mode | Routine ID | Option Record | Full UDS Request Bytes | Evidence Line |
| :--- | :---: | :---: | :--- | :--- |
| **Service Regeneration (Stationary)** | `0x053D` | `04 00 00` | `31 01 05 3D 04 00 00` | line 111143 |
| **Emergency Regeneration (Driving)** | `0x0305` | `04 00 00` | `31 01 03 05 04 00 00` | line 111145 |

---

## 3. Routine Execution Status Polling

### Evidence
- **Class**: `ReadVagUdsStatusCommand`
- **Decompiled C**: Lines 110955–111035
- **Status DID**: `0x0102` (or `0x0100`)
- **Confidence**: `VERIFIED`

### Status Byte Decoding (`statusByte >> 4`)
- `0x0`: `"No routine in progress"` (`0x00`)
- `0x1`: `"Routine succeeded"` (`0x10`)
- `0x4`: `"Routine failed: aborted, safety reasons"` (`0x40`)
- `0x6`: `"Routine failed: conditions not correct"` (`0x60`)
- `0x8`: `"Routine ended due to timeout"` (`0x80`)
- `0xC`: `"Routine in progress"` (`0xC0`)
