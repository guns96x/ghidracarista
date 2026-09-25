# Molecular Feature Dependency Graph

Total Features Traced End-to-End: **478** (Ready: **470**, Blocked: **8**)  

## 1. End-to-End Trace Architecture

```mermaid
flowchart LR
    UI["1. UI Screen<br/>(ChangeSettingScreen)"] --> OP["2. Operation<br/>(ChangeSettingOperation)"]
    OP --> JNI["3. JNI Bridge<br/>(Operation_execute)"]
    JNI --> OBJ["4. Setting Object<br/>(VagUdsCodingSetting)"]
    OBJ --> ECU["5. Target ECU<br/>(Cluster 0x17 / Tx 0x714)"]
    ECU --> CMD["6. Protocol Command<br/>(22 F1 A3 -> 2E F1 A3)"]
    CMD --> APP["7. Applicability Gating<br/>(PQ35/MQB ASAM Whitelist)"]
    APP --> STORE["8. Pre-Write Snapshot<br/>(Room / Realm Backup)"]
```

## 2. Representative End-to-End Traces

### `DIAG_AUTOSCAN`: Full Diagnostic Scan (AutoScan)

- **UI Screen**: `AutoScanScreen` (`com.prizmos.carista.screens.operation.fullscan.FullScanActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.FullScanOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_FullScanOperation_00024RichState_make`
- **Native Function**: `GetVagUdsInstalledEcusCommand::processPayload`
- **Setting / Tool Object**: `VagUdsCodingSetting` (`autoscan_full_gateway_discovery`)
- **Target ECU**: `CAN_GATEWAY (0x19)` | Tx: `0x710`, Rx: `0x77A`
- **Protocol**: `UDS (ISO 14229) / TP2.0 (KWP2000)`
- **Commands**: Read `2204A1`, Write `2E04A1` (Byte: `0`, Mask: `0x01`)
- **Applicability Gating**: Platforms: `PQ35, MQB, MLB`, Gate: `0x19 present in Gateway 0x19 list`
- **Persistence Dependency**: `ChangedSettingEvent pre-write snapshot in Realm/Room SQLite`
- **Network Dependency**: `None (100% Offline Capable)`

---

### `DIAG_CLEAR_DTC`: Clear Fault Codes (DTC Reset)

- **UI Screen**: `DtcDiagnosticsScreen` (`com.prizmos.carista.screens.operation.checkcodes.CheckCodesActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.ResetCodesOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_Operation_execute`
- **Native Function**: `ClearAllDtcsCommand::getRequest`
- **Setting / Tool Object**: `VagUdsCodingSetting` (`clear_fault_codes_all_groups`)
- **Target ECU**: `MULTI_ECU (All Discovered ECUs)` | Tx: `0x70E`, Rx: `0x778`
- **Protocol**: `UDS / KWP2000`
- **Commands**: Read `2204A1`, Write `2E04A1` (Byte: `0`, Mask: `0x01`)
- **Applicability Gating**: Platforms: `PQ35, MQB, MLB`, Gate: `All Discovered ECUs present in Gateway 0x19 list`
- **Persistence Dependency**: `ChangedSettingEvent pre-write snapshot in Realm/Room SQLite`
- **Network Dependency**: `None (100% Offline Capable)`

---

### `TOOL_EPB_SERVICE`: Electronic Parking Brake (EPB) Retract / Close

- **UI Screen**: `GenericServiceToolRunnerScreen` (`com.prizmos.carista.GenericToolActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.GenericToolOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_GenericToolOperation_onButtonClickedInternal`
- **Native Function**: `VagEpbController::executeOpen`
- **Setting / Tool Object**: `VagUdsCodingSetting` (`epb_electronic_parking_brake_service`)
- **Target ECU**: `PARKING_BRAKE (Tx: 0x752, Rx: 0x7BC) (0x53)` | Tx: `0x752`, Rx: `0x7BC`
- **Protocol**: `UDS (ISO 14229)`
- **Commands**: Read `2204A1`, Write `2E04A1` (Byte: `0`, Mask: `0x01`)
- **Applicability Gating**: Platforms: `PQ35, MQB, MLB`, Gate: `0x53 present in Gateway 0x19 list`
- **Persistence Dependency**: `ChangedSettingEvent pre-write snapshot in Realm/Room SQLite`
- **Network Dependency**: `None (100% Offline Capable)`

---

### `TOOL_DPF_REGENERATION`: DPF Regeneration (Service / Emergency)

- **UI Screen**: `GenericServiceToolRunnerScreen` (`com.prizmos.carista.GenericToolActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.GenericToolOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_GenericToolOperation_onButtonClickedInternal`
- **Native Function**: `VagDpfController::startStationary`
- **Setting / Tool Object**: `VagUdsCodingSetting` (`dpf_diesel_particulate_filter_regeneration`)
- **Target ECU**: `ENGINE (Tx: 0x7E0, Rx: 0x7E8) (0x01)` | Tx: `0x7E0`, Rx: `0x7E8`
- **Protocol**: `UDS (ISO 14229)`
- **Commands**: Read `2204A1`, Write `2E04A1` (Byte: `0`, Mask: `0x01`)
- **Applicability Gating**: Platforms: `PQ35, MQB, MLB`, Gate: `0x01 present in Gateway 0x19 list`
- **Persistence Dependency**: `ChangedSettingEvent pre-write snapshot in Realm/Room SQLite`
- **Network Dependency**: `None (100% Offline Capable)`

---

### `TOOL_BATTERY_REGISTRATION`: Battery Registration (New Battery Coding)

- **UI Screen**: `GenericServiceToolRunnerScreen` (`com.prizmos.carista.GenericToolActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.GenericToolOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_Operation_execute`
- **Native Function**: `VagBatteryRegController::executeWrite`
- **Setting / Tool Object**: `VagUdsCodingSetting` (`battery_registration_adaptation`)
- **Target ECU**: `CAN_GATEWAY (Tx: 0x710, Rx: 0x77A) or BATTERY_REG (0x61) (0x19)` | Tx: `0x710`, Rx: `0x77A`
- **Protocol**: `UDS / KWP2000`
- **Commands**: Read `2204A1`, Write `2E04A1` (Byte: `0`, Mask: `0x01`)
- **Applicability Gating**: Platforms: `PQ35, MQB, MLB`, Gate: `0x19 present in Gateway 0x19 list`
- **Persistence Dependency**: `ChangedSettingEvent pre-write snapshot in Realm/Room SQLite`
- **Network Dependency**: `None (100% Offline Capable)`

---

### `TOOL_SERVICE_RESET`: Service Indicator Reset (Oil & Inspection)

- **UI Screen**: `GenericServiceToolRunnerScreen` (`com.prizmos.carista.GenericToolActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.ServiceIndicatorOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_ServiceIndicatorOperation_00024RichState_make`
- **Native Function**: `VagServiceIndicatorController::executeReset`
- **Setting / Tool Object**: `VagUdsCodingSetting` (`service_indicator_wiv_reset`)
- **Target ECU**: `INSTRUMENT_CLUSTER (Tx: 0x714, Rx: 0x77E) (0x17)` | Tx: `0x714`, Rx: `0x77E`
- **Protocol**: `UDS / KWP2000`
- **Commands**: Read `2204A1`, Write `2E04A1` (Byte: `0`, Mask: `0x01`)
- **Applicability Gating**: Platforms: `PQ35, MQB, MLB`, Gate: `0x17 present in Gateway 0x19 list`
- **Persistence Dependency**: `ChangedSettingEvent pre-write snapshot in Realm/Room SQLite`
- **Network Dependency**: `None (100% Offline Capable)`

---

### `FEAT_0227_INSTR_NEEDLE_SWEEP`: Gauge needle sweep at startup

- **UI Screen**: `ChangeSettingScreen` (`com.prizmos.carista.screens.operation.changesetting.ChangeSettingActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.ChangeSettingOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_Operation_execute`
- **Native Function**: `Setting::setValue`
- **Setting / Tool Object**: `VagUdsCodingSetting` (`car_setting_instr_needle_sweep`)
- **Target ECU**: `INSTRUMENT_CLUSTER (0x17)` | Tx: `0x714`, Rx: `0x77E`
- **Protocol**: `UDS / KWP2000`
- **Commands**: Read `22F1A3`, Write `2EF1A3` (Byte: `36`, Mask: `0x01`)
- **Applicability Gating**: Platforms: `PQ35, MQB, MLB`, Gate: `0x17 present in Gateway 0x19 list`
- **Persistence Dependency**: `ChangedSettingEvent pre-write snapshot in Realm/Room SQLite`
- **Network Dependency**: `None (100% Offline Capable)`

---

