# VAG Diagnostic Addressing Architecture

## 1. VAG Logical Addresses to CAN Identifiers

### Evidence
- **Binary**: `libCarista.so`
- **Functions**: `VagUdsEcu::initialize()` (line 583306), `VagCanEcu::initialize()` (line 455613), `VagEcu::getByVagId()` (line 537973)
- **Confidence**: `VERIFIED`

---

## 2. Verified ECU Address Matrix

| VAG ID | Logical Name | UDS TX CAN ID (11-bit) | UDS RX CAN ID | 29-bit CAN ID (TX/RX) | TP2.0 Setup ID |
| :---: | :--- | :---: | :---: | :---: | :---: |
| `0x01` | ENGINE | `0x7E0` | `0x7E8` | `0x17FC0076` / `0x17FE0076` | `0x201` |
| `0x02` | TRANSMISSION | `0x7E1` | `0x7E9` | `0x17FC0077` / `0x17FE0077` | `0x202` |
| `0x03` | ABS | `0x713` | `0x77D` | — | `0x203` |
| `0x08` | HVAC | `0x746` | `0x7B0` | — | `0x208` |
| `0x09` | CENTRAL_ELEC | `0x70E` | `0x778` | — | `0x209` |
| `0x13` | AUTO_DIST_REG (ACC)| `0x757` | `0x7C1` | — | `0x213` |
| `0x14` | DIFFERENTIAL_LOCKS | `0x71E` | `0x788` | — | `0x214` |
| `0x15` | AIRBAG | `0x715` | `0x77F` | — | `0x215` |
| `0x17` | INSTRUMENT_CLUSTER | `0x714` | `0x77E` | — | `0x217` |
| `0x19` | CAN_GATEWAY | `0x710` | `0x77A` | — | `0x21F` |
| `0x22` | AWD / HALDEX | `0x70F` | `0x779` | — | `0x222` |
| `0x44` | STEERING_ASSIST | `0x712` | `0x77C` | — | `0x244` |
| `0x52` | DOOR_PASSENGER | `0x74B` | `0x7B5` | — | `0x252` |
| `0x53` | PARKING_BRAKE (EPB)| `0x752` | `0x7BC` | — | `0x219` |
| `0x5F` | INFOTAINMENT | `0x773` | `0x7DD` | — | `0x25F` |
| `0x6C` | BACK_UP_CAMERA | `0x769` | `0x7D3` | — | `0x26C` |
| `0x6D` | TRUNK | `0x723` | `0x78D` | — | `0x26D` |
| `0x76` | PARK_STEER_ASSIST | `0x70A` | `0x774` | — | `0x276` |
