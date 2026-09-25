# Molecular Native & JNI Call Graph

Total JNI Bridge Exported Functions: **170**  
Source Binary: `lib/arm64-v8a/libCarista.so` (ELF 64-bit ARMv8)  

## 1. High-Level Native Architecture

The Carista native library (`libCarista.so`) implements the entire OBD2, UDS (ISO 14229), KWP2000, and VAG TP2.0 transport state machine in C++.
Java/Kotlin operates primarily as a declarative presentation layer, delegating protocol execution and parameter encoding to native routines.

```mermaid
flowchart LR
    subgraph Android DEX Layer
        Operation["Operation (Java)"]
        FullScan["FullScanOperation"]
        ChangeSetting["ChangeSettingOperation"]
        GenericTool["GenericToolOperation"]
    end

    subgraph JNI Boundary
        JNI_Exec["Operation_execute()<br/>0xe1d4ac"]
        JNI_Scan["FullScanOperation_RichState_make()<br/>0xe29cc8"]
        JNI_Tool["GenericToolOperation_onButtonClicked()<br/>0xe3ca48"]
    end

    subgraph Native C++ Core (libCarista.so)
        ProtoEng["VehicleProtocol Engine"]
        UdsComm["VagUdsCommunicator"]
        Tp20Comm["VagTp20Communicator"]
        EcuMgr["EcuManager & Gateway Parser"]
        SettingEng["Setting::extractValue() / setValue()"]
    end

    Operation --> JNI_Exec --> ProtoEng
    FullScan --> JNI_Scan --> EcuMgr
    ChangeSetting --> JNI_Exec --> SettingEng
    GenericTool --> JNI_Tool --> UdsComm
    ProtoEng --> UdsComm
    ProtoEng --> Tp20Comm
```

## 2. Key JNI Bridge Operations

| Java Calling Class | Method | Native Symbol Address | Functional Category |
|---|---|---|---|
| `com.prizmos.carista.library.operation.ServiceIndicatorOperation$RichState` | `make` | `0x0xe346b4` | **Service Tools** |
| `com.prizmos.carista.library.operation.Operation` | `getStateInternal` | `0x0xe1e084` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.ReadValuesOperation` | `getAvailableItems` | `0x0xe30324` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.RestoreOperation` | `initNative` | `0x0xe23bf4` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.Operation` | `execute` | `0x0xe1d4ac` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.resources.OneSignalCredentials` | `getAppId` | `0x0xe3ed14` | **Native Utilities** |
| `com.prizmos.carista.library.operation.GenericToolOperation` | `onButtonClickedInternal` | `0x0xe3ca48` | **Service Tools** |
| `com.prizmos.carista.library.resources.PlacesApi` | `getApiKey` | `0x0xe3e234` | **Backend API Client** |
| `com.prizmos.carista.library.operation.Operation` | `getManufacturerSpecificProtocol` | `0x0xe1e650` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.Operation` | `unregisterStatusListener` | `0x0xe1d0f8` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.EmissionTestsOperation` | `initNative` | `0x0xe2889c` | **Operation Core Engine** |
| `com.prizmos.carista.library.model.Vin` | `getObfuscatedVinInternal` | `0x0xe36980` | **Native Utilities** |
| `com.prizmos.carista.library.operation.CheckLiveDataOperation` | `getContentControl` | `0x0xe23850` | **Live Data** |
| `com.prizmos.carista.library.operation.FullScanOperation$RichState` | `make` | `0x0xe29cc8` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.GenericToolOperation$RichState` | `make` | `0x0xe3c350` | **Service Tools** |
| `com.prizmos.carista.library.operation.ReadTpmsInfoOperation` | `initNative` | `0x0xe2ed20` | **Service Tools** |
| `com.prizmos.carista.library.connection.DeviceLatestInfo` | `isDefectiveNative` | `0x0xe1a960` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.PlaygroundOperation$RichState` | `make` | `0x0xe208f0` | **Operation Core Engine** |
| `com.prizmos.carista.networking.ApiService$URL` | `baseUrl` | `0x0xe177a0` | **Service Tools** |
| `com.prizmos.carista.library.operation.Operation$RichState` | `NONE` | `0x0xe1c338` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.Operation$OnStateUpdateListener` | `initNative` | `0x0xe1bd84` | **Operation Core Engine** |
| `com.prizmos.carista.App` | `initNative` | `0x0xe16fc4` | **Native Utilities** |
| `com.prizmos.carista.library.operation.CheckSettingsOperation` | `initNative` | `0x0xe269f4` | **Settings / Customizations** |
| `com.prizmos.carista.library.connection.State$OnStateUpdateListener` | `onStateUpdate` | `0x0xe1859c` | **Native Utilities** |
| `com.prizmos.carista.library.operation.GetEcuInfoOperation` | `getCodingRawAddress` | `0x0xe2ab64` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.CheckCodesOperation` | `initNativeWithEcus` | `0x0xe25684` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.ReadValuesOperation` | `isExperimental` | `0x0xe319ac` | **Operation Core Engine** |
| `com.prizmos.carista.library.model.Ecu` | `isObd2Native` | `0x0xe3732c` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.Operation` | `destroyNative` | `0x0xe1ca2c` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.Operation` | `reportsProgress` | `0x0xe1dae0` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.CheckSettingsOperation` | `getItemContentControl` | `0x0xe27180` | **Settings / Customizations** |
| `com.prizmos.carista.library.connection.SimulatorDevice` | `getName` | `0x0xe1b70c` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.ReadRawValuesOperation` | `getRawValue` | `0x0xe33040` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.Operation` | `registerStatusListener` | `0x0xe1cca4` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.ReadValuesOperation` | `hasSettingValue` | `0x0xe30d40` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.EmissionTestsOperation$RichState` | `make` | `0x0xe2863c` | **Operation Core Engine** |
| `com.prizmos.carista.library.resources.ZendeskCredentials` | `getAppId` | `0x0xe3e7a4` | **Native Utilities** |
| `com.prizmos.carista.library.operation.CheckCodesOperation` | `generateRichState` | `0x0xe25dc8` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.ReadLiveDataOperation$RichState` | `make` | `0x0xe2db24` | **Live Data** |
| `com.prizmos.carista.library.connection.AndroidDevice.NAME.1OBDLINK` | `1CX` | `0x0xe1b454` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.PlaygroundOperation` | `initNative` | `0x0xe20b50` | **Operation Core Engine** |
| `com.prizmos.carista.library.connection.DeviceLatestInfo` | `isCaristaNative` | `0x0xe19970` | **Transport & Hardware** |
| `com.prizmos.carista.library.model.Ecu` | `getNameResId` | `0x0xe37004` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.Operation` | `onIgnitionCycled` | `0x0xe1f74c` | **Operation Core Engine** |
| `com.prizmos.carista.util.Log` | `d` | `0x0xe44b28` | **Native Utilities** |
| `com.prizmos.carista.util.Log` | `e` | `0x0xe45080` | **Native Utilities** |
| `com.prizmos.carista.library.operation.CheckCodesOperation$RichState` | `NONE` | `0x0xe24038` | **Operation Core Engine** |
| `com.prizmos.carista.util.Log` | `w` | `0x0xe44dd4` | **Native Utilities** |
| `com.prizmos.carista.library.connection.SimulatorDevice` | `getAddress` | `0x0xe1ba48` | **Transport & Hardware** |
| `com.prizmos.carista.library.model.SettingDto` | `getFromServiceToolInternal` | `0x0xe3a194` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.CheckLiveDataOperation` | `initNative` | `0x0xe22394` | **Live Data** |
| `com.prizmos.carista.library.operation.Operation` | `cancel` | `0x0xe1e938` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.GetEcuInfoOperation` | `getAdaptationRawAddress` | `0x0xe2a884` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.CheckCodesOperation` | `getContentControl` | `0x0xe26640` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.CheckAvailableToolsOperation` | `initNative` | `0x0xe21414` | **Service Tools** |
| `com.prizmos.carista.library.resources.ZendeskCredentials` | `getClientId` | `0x0xe3ea5c` | **Backend API Client** |
| `com.prizmos.carista.library.operation.GetEcuInfoOperation` | `supportsDiagnostics` | `0x0xe2b4ac` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.ReadTpmsInfoOperation$RichState` | `NONE` | `0x0xe2dd84` | **Service Tools** |
| `com.prizmos.carista.library.operation.Operation` | `getDevices` | `0x0xe1fa38` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.ServiceIndicatorOperation` | `resetIndicator` | `0x0xe34dd8` | **Service Tools** |
| `com.prizmos.carista.library.model.SettingRef` | `isLegalDisclaimerRequired` | `0x0xe39144` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.Operation` | `onDeviceTypeSelected` | `0x0xe1eef8` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.ReadRawValuesOperation` | `initNative` | `0x0xe324c0` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.Operation` | `onDeviceSelected` | `0x0xe1f1e4` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.ChangeSettingOperation` | `initNative` | `0x0xe20e78` | **Settings / Customizations** |
| `com.prizmos.carista.App` | `getDebugMode` | `0x0xe16aa8` | **Native Utilities** |
| `com.prizmos.carista.library.operation.FullScanOperation` | `initNative` | `0x0xe29f28` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.GetEcuListOperation` | `initNative` | `0x0xe2c1dc` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.ReadVoltageOperation` | `initNative` | `0x0xe2529c` | **Live Data** |
| `com.prizmos.carista.library.operation.CheckAvailableToolsOperation` | `getContentControl` | `0x0xe2184c` | **Service Tools** |
| `com.prizmos.carista.library.operation.CollectDebugInfoOperation$RichState` | `NONE` | `0x0xe275d0` | **Operation Core Engine** |
| `com.prizmos.carista.library.model.SettingRef` | `getInstruction` | `0x0xe39418` | **Settings / Customizations** |
| `com.prizmos.carista.App` | `getBetaMode` | `0x0xe16aa0` | **Native Utilities** |
| `com.prizmos.carista.library.operation.ServiceIndicatorOperation` | `initNative` | `0x0xe34914` | **Service Tools** |
| `com.prizmos.carista.library.operation.Operation$RichState` | `make` | `0x0xe1c7cc` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.EvHybridBatteryHealthOperation$RichState` | `NONE` | `0x0xe2f98c` | **Operation Core Engine** |
| `com.prizmos.carista.library.model.SettingDto` | `getFromInternal` | `0x0xe39e24` | **Settings / Customizations** |
| `com.prizmos.carista.library.model.SettingCategory` | `getIconResIdInternal` | `0x0xe37cf0` | **Settings / Customizations** |
| `com.prizmos.carista.library.resources.MixpanelCredentials` | `getToken` | `0x0xe3efcc` | **Native Utilities** |
| `com.prizmos.carista.library.connection.State` | `isErrorInternal` | `0x0xe18be0` | **Native Utilities** |
| `com.prizmos.carista.library.operation.RelearnTpmsIdsOperation` | `initNative` | `0x0xe333e4` | **Service Tools** |
| `com.prizmos.carista.library.operation.EvHybridBatteryHealthOperation` | `initNative` | `0x0xe2fcac` | **Operation Core Engine** |
| `com.prizmos.carista.library.connection.DeviceLatestInfo` | `isKiwi3Native` | `0x0xe19fd0` | **Transport & Hardware** |
| `com.prizmos.carista.library.model.GetNumTroubleCodesModel` | `getAvailableTests` | `0x0xe38040` | **DTC Diagnostics** |
| `com.prizmos.carista.library.connection.DeviceLatestInfo` | `isVLinkerNative` | `0x0xe1a630` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.CollectDebugInfoOperation` | `initNative` | `0x0xe27d4c` | **Operation Core Engine** |
| `com.prizmos.carista.library.simulator.src.Simulators` | `setAdapterType` | `0x0xe3fbe4` | **Native Utilities** |
| `com.prizmos.carista.util.StringUtils` | `getBytes` | `0x0xe3df58` | **Native Utilities** |
| `com.prizmos.carista.library.model.SettingRef` | `getEcu` | `0x0xe38b64` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.WriteRawValuesOperation` | `initNative` | `0x0xe351ac` | **Operation Core Engine** |
| `com.prizmos.carista.library.resources.ZendeskCredentials` | `getUrl` | `0x0xe3e4ec` | **Native Utilities** |
| `com.prizmos.carista.library.operation.WriteTpmsIdsOperation` | `initNative` | `0x0xe359ac` | **Service Tools** |
| `com.prizmos.carista.library.operation.GenericToolOperation` | `isExperimentalInternal` | `0x0xe3d204` | **Service Tools** |
| `com.prizmos.carista.library.operation.CarHealthCheckAvailabilityOperation` | `initNative` | `0x0xe2277c` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.CarHealthCheckOperation$RichState` | `NONE` | `0x0xe22bb4` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.ReadVehIdOperation` | `initNative` | `0x0xe2f1e4` | **Operation Core Engine** |
| `com.prizmos.carista.library.network.AndroidHttpClient$ResponseHandler` | `run` | `0x0xe0417c` | **Backend API Client** |
| `com.prizmos.carista.library.operation.Operation` | `didGetAnyResponseFromVehicle` | `0x0xe1fdac` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.GenericToolOperation` | `onSettingUpdate` | `0x0xe3d4e4` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.GetEcuInfoOperation` | `supportsAdaptation` | `0x0xe2bea4` | **Settings / Customizations** |
| `com.prizmos.carista.library.resources.AdjustCredentials` | `getAppToken` | `0x0xe3f5a4` | **Native Utilities** |
| `com.prizmos.carista.library.connection.DeviceLatestInfo` | `getLastKnownNameForTrackingNative` | `0x0xe19638` | **Transport & Hardware** |
| `com.prizmos.carista.library.model.SettingRef` | `getNameResIdNative` | `0x0xe38e54` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.ServiceIndicatorOperation$RichState` | `NONE` | `0x0xe338a8` | **Service Tools** |
| `com.prizmos.carista.library.operation.GetEcuInfoOperation` | `getEcu` | `0x0xe2b128` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.Operation` | `getAvailableBackupId` | `0x0xe20080` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.CheckCodesOperation$RichState` | `make` | `0x0xe24c4c` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.GetEcuInfoOperation` | `isValueInterpretedAsDecimal` | `0x0xe2ae44` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.service.Session` | `setConnectorNative` | `0x0xe17f7c` | **Service Tools** |
| `com.prizmos.carista.library.connection.DeviceLatestInfo` | `isCaristaEvoNative` | `0x0xe19ca0` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.GetEcuInfoOperation` | `initNative` | `0x0xe2a40c` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.model.SettingRef` | `getInterpretation` | `0x0xe39a80` | **Settings / Customizations** |
| `com.prizmos.carista.library.resources.AdaptyCredentials` | `getApiKey` | `0x0xe3f2ec` | **Backend API Client** |
| `com.prizmos.carista.library.operation.CheckAvailableToolsOperation` | `getItemContentControl` | `0x0xe21c88` | **Service Tools** |
| `com.prizmos.carista.library.model.Vin` | `getPlaceholderVin` | `0x0xe366b0` | **Native Utilities** |
| `com.prizmos.carista.library.operation.CheckSettingsOperation` | `getContentControl` | `0x0xe26ddc` | **Settings / Customizations** |
| `com.prizmos.carista.library.connection.State$Set` | `getObd2NegativeResponseStates` | `0x0xe1889c` | **Native Utilities** |
| `com.prizmos.carista.library.operation.ReadTpmsInfoOperation$RichState` | `make` | `0x0xe2eac0` | **Service Tools** |
| `com.prizmos.carista.library.operation.WriteTpmsIdsOperation` | `isValidId` | `0x0xe36178` | **Service Tools** |
| `com.prizmos.carista.library.operation.FullScanOperation$RichState` | `NONE` | `0x0xe28d74` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.GenericToolOperation$RichState` | `NONE` | `0x0xe3a884` | **Service Tools** |
| `com.prizmos.carista.library.model.Vin` | `isPlaceholderVin` | `0x0xe36414` | **Native Utilities** |
| `com.prizmos.carista.library.operation.PlaygroundOperation$RichState` | `NONE` | `0x0xe203d4` | **Operation Core Engine** |
| `com.prizmos.carista.library.model.SettingCategory` | `getNameResIdInternal` | `0x0xe379a0` | **Settings / Customizations** |
| `com.prizmos.carista.util.LogServerUrlProvider$URL` | `baseUrl` | `0x0xe17a44` | **Native Utilities** |
| `com.prizmos.carista.App` | `getDeviceLatestInfo` | `0x0xe16ab0` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.GenericToolOperation` | `initNative` | `0x0xe3c5b0` | **Service Tools** |
| `com.prizmos.carista.library.operation.ReadValuesOperation` | `getSettingValue` | `0x0xe31128` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.Operation` | `getProgress` | `0x0xe1ddb4` | **Operation Core Engine** |
| `com.prizmos.carista.library.model.TestResult` | `isReadyNative` | `0x0xe3889c` | **Native Utilities** |
| `com.prizmos.carista.App` | `getSeed` | `0x0xe16d24` | **Native Utilities** |
| `com.prizmos.carista.library.connection.State` | `isFinishedInternal` | `0x0xe190a0` | **Native Utilities** |
| `com.prizmos.carista.library.connection.AndroidDevice.NAME` | `1CARISTA` | `0x0xe1ac2c` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.GenericToolOperation` | `isSettingValueValid` | `0x0xe3d91c` | **Settings / Customizations** |
| `com.prizmos.carista.service.Session` | `stopConnectionManagerNative` | `0x0xe17cf0` | **Service Tools** |
| `com.prizmos.carista.library.resources.RefinerCredentials` | `getProjectId` | `0x0xe3f8c4` | **Native Utilities** |
| `com.prizmos.carista.library.operation.CollectDebugInfoOperation$RichState` | `make` | `0x0xe27aec` | **Operation Core Engine** |
| `com.prizmos.carista.library.model.TextInterpretation` | `getUserDisplayableValueStatic` | `0x0xe3dc74` | **Transport & Hardware** |
| `com.prizmos.carista.library.connection.DeviceLatestInfo` | `isObdLinkNative` | `0x0xe1a300` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.CheckCodesOperation` | `resetCodesNative` | `0x0xe261d4` | **Operation Core Engine** |
| `com.prizmos.carista.library.connection.AndroidDevice.NAME.1KIWI` | `13` | `0x0xe1aee4` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.Operation` | `onSfdConfirmationNative` | `0x0xe1e354` | **SFD / Security Auth** |
| `com.prizmos.carista.library.model.SettingRef` | `toEventStringNative` | `0x0xe39758` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.Operation` | `getId` | `0x0xe1d7b8` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.EvHybridBatteryHealthOperation$RichState` | `make` | `0x0xe2f4bc` | **Operation Core Engine** |
| `com.prizmos.carista.library.model.TestResult` | `getDescriptionResourceIdNative` | `0x0xe385b8` | **Native Utilities** |
| `com.prizmos.carista.library.operation.GetEcuInfoOperation` | `supportsMultiCoding` | `0x0xe2bb6c` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.GenericToolOperation` | `onCheckBoxUpdateInternal` | `0x0xe3ce1c` | **Service Tools** |
| `com.prizmos.carista.library.operation.EmissionTestsOperation$RichState` | `NONE` | `0x0xe28134` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.ReadRawValuesOperation` | `getRawAddresses` | `0x0xe32b58` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.GetEcuInfoOperation` | `supportsSingleCoding` | `0x0xe2b834` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.ReadLiveDataOperation` | `initNative` | `0x0xe2c970` | **Live Data** |
| `com.prizmos.carista.library.connection.AndroidDevice.NAME.1OBDLINK.1MX` | `1PLUS` | `0x0xe1b19c` | **Transport & Hardware** |
| `com.prizmos.carista.util.Log` | `getLogStringNative` | `0x0xe4532c` | **Native Utilities** |
| `com.prizmos.carista.library.connection.State` | `isFatalError` | `0x0xe18e40` | **Native Utilities** |
| `com.prizmos.carista.library.operation.ReadLiveDataOperation$RichState` | `NONE` | `0x0xe2d21c` | **Live Data** |
| `com.prizmos.carista.library.operation.ReadValuesOperation` | `getConnectedChassisId` | `0x0xe31d94` | **Operation Core Engine** |
| `com.prizmos.carista.library.connection.DeviceLatestInfo` | `getNameForTrackingNative` | `0x0xe19300` | **Transport & Hardware** |
| `com.prizmos.carista.library.model.Ecu` | `getObd2Instance` | `0x0xe36d1c` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.EvoFirmwareUpdateOperation` | `initNative` | `0x0xe3004c` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.CheckCodesOperation` | `initNative` | `0x0xe24eac` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.GetEcuListOperation` | `getEcuList` | `0x0xe2c4b4` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.operation.Operation` | `onConnectionHardwareTurnedOn` | `0x0xe1ec0c` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.CarHealthCheckOperation$RichState` | `make` | `0x0xe231b8` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.CarHealthCheckOperation` | `initNative` | `0x0xe23418` | **Operation Core Engine** |
| `com.prizmos.carista.library.operation.ReadValuesOperation` | `getConnectedEcuTag` | `0x0xe31550` | **AutoScan & ECU Discovery** |
| `com.prizmos.carista.library.model.NumericalInterpretation` | `getUserDisplayableValueInternal` | `0x0xe3a504` | **Transport & Hardware** |
| `com.prizmos.carista.library.operation.ReadValuesOperation` | `isSfd1Protected` | `0x0xe320e0` | **SFD / Security Auth** |
| `com.prizmos.carista.library.model.SettingCategory` | `valuesNative` | `0x0xe37608` | **Settings / Customizations** |
| `com.prizmos.carista.library.operation.Operation$OnStateUpdateListener` | `destroyNative` | `0x0xe1c05c` | **Operation Core Engine** |

## 3. Native Request Builders & Response Parsers

### UDS Gateway ECU Discovery
- **C++ Function**: `GetVagUdsInstalledEcusCommand::processPayload` (`libCarista.so.c` line 108420)
- **Request**: `22 04 A1` (ReadDataByIdentifier Gateway Installation List)
- **Payload Parser**: 4-byte records per ECU. Byte 2 bit 2 indicates active ECU.

### UDS Fault Memory Extraction
- **C++ Function**: `ReadDtcCommand::processPayload` (`libCarista.so.c` line 108450)
- **Request**: `19 02 8D` (ReadDTCInformation reportDTCByStatusMask)
- **Response**: `59 02 [Mask] [3-byte DTC] [1-byte Status]`

### EPB Caliper Retraction & Status Polling
- **C++ Function**: `VagEpbController::executeOpen` (`libCarista.so.c` line 111280)
- **Routine Start**: `31 01 03 A1`
- **Status Query**: `22 01 02` (DID 0x0102 status byte: 0x10 SUCCEEDED, 0xC0 IN_PROGRESS)
- **Routine Stop**: `31 02 03 A1`

