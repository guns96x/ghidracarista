# Molecular Local Data & Configuration Formats

Comprehensive reverse-engineering report on all local storage, database, asset, and configuration formats used by Carista.

## 1. Asset Inventory & Format Classifications

| Asset Path | Size (Bytes) | Magic Header | Format Type | Reverse Engineering Status |
|---|---|---|---|---|
| `1TrbQPfd7xYPDryL` | 207,591 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `5bgvDyZWg6hkxFFq` | 153,739 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `6MenowszWNfnvb6a` | 354,786 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `7C5MBOBd0PhPaa4D` | 159,983 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `7yOwujq4i9HdNipM` | 248,557 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `A9tABTPD9aKkvZUc` | 150,732 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `Dak4BY3C0ljDnDw1` | 283,938 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `DEUgkyVSTcYbP5d2` | 268,658 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `dptro4s2eyMgAsiP` | 155,384 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `EmeHpsFHkxc9qDcL` | 157,368 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `FHb79TQgYf5zo9PS` | 155,965 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `FHCuFw3ZIlnP7MtG` | 156,406 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `G6bUqOQdHdi2OyfG` | 155,311 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `gI1sG9Ko06stVEex` | 118,660 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `hDZhZmbyheBPU91Q` | 155,964 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `help_center_article_style.css` | 8,231 | `0x2f2a3d3d` (`/*======`) | **UNKNOWN_BINARY** | Analyzed |
| `hLPxNj2a6qOa1NFo` | 210,374 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `hTzJdMXedZUctgKE` | 151,225 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `HYDEdcgpZXLjIITW` | 250,100 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `I4p6E3VR3Ut8QetQ` | 285,585 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `JOKKzfWuormYc7TI` | 245,660 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `nFmnqUWBzBvV64Xj` | 152,663 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `PHf7Rqd0EFLJ5qX4` | 270,457 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `PL1DZGYLln2s8YF0` | 159,187 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `PublicSuffixDatabase.list` | 132,737 | `0x00020602` (`....*.00`) | **UNKNOWN_BINARY** | Analyzed |
| `pXiD9OWHt3eOOKNT` | 166,765 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `pxIjn61XWbdlZKv2` | 160,976 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `QvztvemRypB816KB` | 150,963 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `qxn7jsJPp9cOBjWV` | 210,475 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `R4O6xDwPW9bkRlV4` | 159,239 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `RcKwOiWVw1bR4q9R` | 152,669 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `sHhqwtQy8HAeYjEi` | 245,580 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `V9kmXpjp2jz4Wrwz` | 158,359 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `WyoMVpic6IDmgnES` | 161,832 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `yyFHTYb7krl2HQJd` | 208,391 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `z50XDfY4JF8r9Dmv` | 148,686 | `0x00494150` (`.IAP....`) | **PAIRIP_ENCRYPTED_DEX** | Analyzed |
| `dexopt/baseline.prof` | 17,644 | `0x70726f00` (`pro.010.`) | **UNKNOWN_BINARY** | Analyzed |
| `dexopt/baseline.profm` | 2,180 | `0x70726d00` (`prm.002.`) | **UNKNOWN_BINARY** | Analyzed |

## 2. Deep Dive: Google Play PairIP (.iap)

- **Magic Header**: `00 49 41 50 02` (`\x00IAP\x02`)
- **Role**: Google Play App Signing & Play Integrity anti-tamper runtime virtualization payload.
- **Mechanism**: Encrypted Dalvik bytecode fragments dynamically decrypted and executed in-memory by `libVMRunner.so` / PairIP stub.
- **Significance for Diagnostics**: **Zero**. Does NOT contain automotive parameters, DIDs, or coding tables. The entire vehicle parameter database is stored in C++ structures within `libCarista.so`.

## 3. Deep Dive: Realm Local Database

- **Engine**: Realm Core (via `librealm-jni.so` and `io.realm.*`)
- **Location on Device**: `/data/data/com.prizmos.carista/files/default.realm`
- **Schema Entities Identified in DEX**:
  - `VehicleEntity`: Stores paired vehicle profiles, VIN, make, model, year, chassis platform.
  - `CheckCodesEvent`: Diagnostic history logs (DTCs found, timestamp, odometer).
  - `ServiceToolEvent`: Service procedure history (EPB retract, DPF regen records).
  - `ChangedSettingEvent`: Pre-write configuration snapshots for 1-click restore/rollback.
  - `LiveDataEvent`: Recorded sensor telemetry sessions.

## 4. Deep Dive: Telemetry & Protobuf Schemas

- **Files**: `client_analytics.proto`, `messaging_event.proto`, `messaging_event_extension.proto`
- **Role**: Serialization format for Firebase Analytics, Google Play Services, and in-app messaging events.

## 5. Clean-Room Replacement Formats in New App

To ensure total independence, maintainability, and clean architecture, the new autonomous app replaces all proprietary formats with standard, human-readable, schema-validated JSON and Android Room SQLite:

- `READY_FEATURES.json`: Replaces native C++ setting tables.
- `vehicles.json` & `ecu_variants.json`: Replaces vehicle taxonomy tables.
- Android Room SQLite: Replaces Realm for vehicle profiles, scan history, and coding rollback snapshots.

