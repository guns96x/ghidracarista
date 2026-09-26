# Molecular Feature Dependency Graph

Features traced: **478**. States: `AMBIGUOUS_MULTI_VARIANT`=70, `EXACT_RESOLVED`=31, `PARTIAL`=197, `REJECTED_TEMPLATE`=6, `UNRESOLVED`=174  

## 1. Trace architecture

```mermaid
flowchart LR
    UI["1. UI Screen"] --> OP["2. Operation"]
    OP --> JNI["3. JNI Bridge"]
    JNI --> FEAT["4. Feature"]
    FEAT --> VAR["5. Variant[] (callsite-proven)"]
    VAR --> ECU["6. ECU + protocol (must agree)"]
    ECU --> FLOW["7. Ordered request flow"]
```

A feature with several variants is `AMBIGUOUS_MULTI_VARIANT`: each executable variant is listed with its own ECU/whitelist identity and no single command stands for the feature.

## 2. Representative traces

### `DIAG_AUTOSCAN`: Full Diagnostic Scan (AutoScan) (REJECTED_TEMPLATE)

- **UI Screen**: `AutoScanScreen` (`com.prizmos.carista.screens.operation.fullscan.FullScanActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.FullScanOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_FullScanOperation_00024RichState_make`
- **Native Function**: `GetVagUdsInstalledEcusCommand::processPayload`
- **Setting classes**: `n/a`

---

### `DIAG_CLEAR_DTC`: Clear Fault Codes (DTC Reset) (REJECTED_TEMPLATE)

- **UI Screen**: `DtcDiagnosticsScreen` (`com.prizmos.carista.screens.operation.checkcodes.CheckCodesActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.ResetCodesOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_Operation_execute`
- **Native Function**: `ClearAllDtcsCommand::getRequest`
- **Setting classes**: `n/a`

---

### `TOOL_EPB_SERVICE`: Electronic Parking Brake (EPB) Retract / Close (REJECTED_TEMPLATE)

- **UI Screen**: `GenericServiceToolRunnerScreen` (`com.prizmos.carista.GenericToolActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.GenericToolOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_GenericToolOperation_onButtonClickedInternal`
- **Native Function**: `VagEpbController::executeOpen`
- **Setting classes**: `n/a`

---

### `TOOL_DPF_REGENERATION`: DPF Regeneration (Service / Emergency) (REJECTED_TEMPLATE)

- **UI Screen**: `GenericServiceToolRunnerScreen` (`com.prizmos.carista.GenericToolActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.GenericToolOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_GenericToolOperation_onButtonClickedInternal`
- **Native Function**: `VagDpfController::startStationary`
- **Setting classes**: `n/a`

---

### `TOOL_BATTERY_REGISTRATION`: Battery Registration (New Battery Coding) (REJECTED_TEMPLATE)

- **UI Screen**: `GenericServiceToolRunnerScreen` (`com.prizmos.carista.GenericToolActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.GenericToolOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_Operation_execute`
- **Native Function**: `VagBatteryRegController::executeWrite`
- **Setting classes**: `n/a`

---

### `TOOL_SERVICE_RESET`: Service Indicator Reset (Oil & Inspection) (REJECTED_TEMPLATE)

- **UI Screen**: `GenericServiceToolRunnerScreen` (`com.prizmos.carista.GenericToolActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.ServiceIndicatorOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_ServiceIndicatorOperation_00024RichState_make`
- **Native Function**: `VagServiceIndicatorController::executeReset`
- **Setting classes**: `n/a`

---

### `FEAT_0013_ALLOW_CONFIG_SOUND_ON_LOCK_UNLOCK_REMOTE`: Allow Config Sound On Lock Unlock Remote (EXACT_RESOLVED)

- **UI Screen**: `ChangeSettingScreen` (`com.prizmos.carista.screens.operation.changesetting.ChangeSettingActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.ChangeSettingOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_Operation_execute`
- **Native Function**: `Setting::setValue`
- **Setting classes**: `VagCanLongCodingSetting`
- **Variant** `car_setting_allow_config_sound_on_lock_unlock_remote@0x14d3ccc`: `TP2.0/KWP2000` flow `tp2_long_coding_rmw` on `VagCanEcu::CENTRAL_CONVENIENCE` (byte `10`, mask `0x80`, selection_required=False)

---

### `FEAT_0003_ACC_OVERTAKING_ON_RIGHT`: Adaptive cruise control overtaking on the right (AMBIGUOUS_MULTI_VARIANT)

- **UI Screen**: `ChangeSettingScreen` (`com.prizmos.carista.screens.operation.changesetting.ChangeSettingActivity`)
- **Operation Class**: `com.prizmos.carista.library.operation.ChangeSettingOperation`
- **JNI Bridge**: `Java_com_prizmos_carista_library_operation_Operation_execute`
- **Native Function**: `Setting::setValue`
- **Setting classes**: `VagUdsCodingSetting`
- **Variant** `car_setting_acc_overtaking_on_right@0x140ab20`: `UDS` flow `uds_did_rmw` on `VagUdsEcu::AUTO_DIST_REG` (byte `2`, mask `0x20`, selection_required=True)

---

