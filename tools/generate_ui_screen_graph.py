#!/usr/bin/env python3
"""
tools/generate_ui_screen_graph.py
Extracts and structures the UI / Product Screen Graph of Carista into:
- research/molecular/UI_SCREEN_GRAPH.json
- research/molecular/UI_SCREEN_GRAPH.md
"""

import os
import json

SCREENS_DEFINITION = [
    {
        "class": "com.prizmos.carista.ConnectActivity",
        "name": "ConnectScreen",
        "category": "Connection / Transport",
        "purpose": "Primary adapter discovery and pairing screen. Allows user to select adapter type (Carista EVO, Carista OBD, Generic ELM327 Bluetooth/BLE, WiFi) and initiate transport handshake.",
        "entry_points": ["Application Launch (MainActivity)", "Disconnect Event", "Toolbar Disconnect Action"],
        "outgoing_navigation": [
            "com.prizmos.carista.connect.ConnectToVehicleActivity",
            "com.prizmos.carista.screens.connectinstructions.ConnectInstructionsActivity",
            "com.prizmos.carista.screens.devicedefective.DeviceDefectiveActivity"
        ],
        "data_dependencies": ["BluetoothAdapter state", "Location/Bluetooth permissions", "Saved adapter MAC / UUID"],
        "operation_invoked": "Connector::connect() -> Elm::initialize()",
        "ecu_feature_relation": "All ECUs (Transport layer prerequisite)",
        "user_inputs": ["Adapter Type Selector", "Bluetooth Device List item click", "Refresh Scan button", "Help link"],
        "safety_gates": ["Bluetooth Enabled check", "Location/Nearby Devices permission granted", "Adapter ELM327 response verification"],
        "result_error_states": ["Connected", "AdapterNotFound", "BluetoothDisabled", "DefectiveElmClone", "ConnectionTimeout"]
    },
    {
        "class": "com.prizmos.carista.connect.ConnectToVehicleActivity",
        "name": "VehicleConnectingProgressScreen",
        "category": "Connection / Transport",
        "purpose": "Displays connection progress state machine while querying adapter capabilities, testing CAN baudrates, reading VIN, and identifying vehicle platform.",
        "entry_points": ["com.prizmos.carista.ConnectActivity"],
        "outgoing_navigation": [
            "com.prizmos.carista.ConfirmVehicleActivity",
            "com.prizmos.carista.SelectVehicleActivity",
            "com.prizmos.carista.screens.operation.main.MainActivity"
        ],
        "data_dependencies": ["Active RFCOMM/BLE socket", "VehicleProtocol detector"],
        "operation_invoked": "ReadVehIdOperation -> DetectVehiclePlatformCommand",
        "ecu_feature_relation": "Engine (0x7E0) / CAN Gateway (0x710) / Cluster (0x714)",
        "user_inputs": ["Cancel button"],
        "safety_gates": ["Ignition ON detection", "Battery voltage check (> 11.5V)"],
        "result_error_states": ["VehicleIdentified", "IgnitionOffDetected", "ProtocolNotSupported", "CommunicationTimeout"]
    },
    {
        "class": "com.prizmos.carista.ConfirmVehicleActivity",
        "name": "ConfirmVehicleScreen",
        "category": "Vehicle Identification",
        "purpose": "Presents decoded vehicle information (Make, Model, Year, Chassis/Platform, VIN) retrieved from Gateway/Engine for user confirmation.",
        "entry_points": ["com.prizmos.carista.connect.ConnectToVehicleActivity"],
        "outgoing_navigation": [
            "com.prizmos.carista.SelectVehicleActivity",
            "com.prizmos.carista.screens.operation.main.MainActivity"
        ],
        "data_dependencies": ["Decoded VehicleModel", "VIN string"],
        "operation_invoked": "VehicleDatabase::lookup(vin, platform)",
        "ecu_feature_relation": "CAN_GATEWAY (0x19), ENGINE (0x01)",
        "user_inputs": ["'Confirm and Continue' button", "'Change Vehicle' link"],
        "safety_gates": ["User must confirm VIN / Model before coding features unlock"],
        "result_error_states": ["Confirmed", "MismatchReported"]
    },
    {
        "class": "com.prizmos.carista.SelectVehicleActivity",
        "name": "ManualVehicleSelectScreen",
        "category": "Vehicle Identification",
        "purpose": "Allows manual fallback selection of Make, Model, and Year when VIN cannot be automatically decoded (e.g. older K-Line models).",
        "entry_points": ["com.prizmos.carista.ConfirmVehicleActivity", "com.prizmos.carista.connect.ConnectToVehicleActivity"],
        "outgoing_navigation": ["com.prizmos.carista.screens.operation.main.MainActivity"],
        "data_dependencies": ["Bundled vehicle taxonomy (vehicles.json)"],
        "operation_invoked": "VehicleDatabase::getModelsForBrand()",
        "ecu_feature_relation": "Applicability Filter Engine",
        "user_inputs": ["Brand Picker", "Model Picker", "Generation/Year Picker"],
        "safety_gates": ["Selection validates against supported platform matrix"],
        "result_error_states": ["VehicleSelected", "UnsupportedVehicleWarned"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.main.MainActivity",
        "name": "VehicleDashboardScreen",
        "category": "Core Hub",
        "purpose": "Main vehicle operational dashboard. Displays current vehicle profile, battery voltage monitor, and primary feature navigation tiles: Diagnose, Customize, Service, Live Data.",
        "entry_points": ["com.prizmos.carista.ConfirmVehicleActivity", "com.prizmos.carista.SelectVehicleActivity"],
        "outgoing_navigation": [
            "com.prizmos.carista.screens.operation.fullscan.FullScanActivity",
            "com.prizmos.carista.screens.operation.checkcodes.CheckCodesActivity",
            "com.prizmos.carista.screens.operation.showsettingcategories.ShowSettingCategoriesActivity",
            "com.prizmos.carista.screens.operation.showavailabletools.ShowAvailableToolsActivity",
            "com.prizmos.carista.screens.operation.showlivedata.ShowLiveDataActivity",
            "com.prizmos.carista.screens.operation.carhealthcheck.CarHealthCheckActivity",
            "com.prizmos.carista.GarageActivity",
            "com.prizmos.carista.MoreActivity"
        ],
        "data_dependencies": ["Active vehicle session", "Cached ECU count", "Current battery voltage"],
        "operation_invoked": "ReadVoltageOperation",
        "ecu_feature_relation": "All ECUs",
        "user_inputs": [
            "Diagnose Card click",
            "Customize Card click",
            "Service Card click",
            "Live Data Card click",
            "Car Health Card click",
            "Disconnect button"
        ],
        "safety_gates": ["Requires active adapter connection", "Monitors for low battery voltage drop (< 11.8V)"],
        "result_error_states": ["Ready", "ConnectionLost", "VoltageWarning"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.fullscan.FullScanActivity",
        "name": "AutoScanScreen",
        "category": "DTC Diagnostics",
        "purpose": "Runs comprehensive vehicle-wide scan: interrogates Gateway 0x19 for installed ECU list, queries each ECU sequentially for active/stored DTCs, and displays aggregated report.",
        "entry_points": ["com.prizmos.carista.screens.operation.main.MainActivity"],
        "outgoing_navigation": [
            "com.prizmos.carista.screens.operation.checkcodes.CheckCodesActivity",
            "com.prizmos.carista.ShowEcuActivity"
        ],
        "data_dependencies": ["Gateway installation list (DID 0x04A1)", "VAG ECU ID table"],
        "operation_invoked": "FullScanOperation -> GetVagUdsInstalledEcusCommand + ReadDtcCommand(19 02 8D)",
        "ecu_feature_relation": "CAN_GATEWAY (0x19) and all discovered ECUs (0x01, 0x02, 0x03, 0x08, 0x09, 0x15, 0x17, 0x53, 0x5F...)",
        "user_inputs": ["'Start Scan' button", "'Stop Scan' button", "ECU item click (inspect)", "'Clear All DTCs' button"],
        "safety_gates": ["Ignition ON required", "Progressive polling throttled to avoid CAN bus flooding"],
        "result_error_states": ["ScanCompleted", "EcuNotResponding", "NRC_78_PendingWait", "ScanAborted"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.checkcodes.CheckCodesActivity",
        "name": "DtcDiagnosticsScreen",
        "category": "DTC Diagnostics",
        "purpose": "Inspects active, pending, and permanent fault codes on selected ECU or system-wide. Displays SAE/VAG code, description, and status bits (Warning Lamp ON, Confirmed, Pending).",
        "entry_points": [
            "com.prizmos.carista.screens.operation.main.MainActivity",
            "com.prizmos.carista.screens.operation.fullscan.FullScanActivity"
        ],
        "outgoing_navigation": [
            "com.prizmos.carista.screens.operation.freezeframe.FreezeFrameDataActivity",
            "com.prizmos.carista.screens.aidiagnostics.AiDiagnosticsActivity"
        ],
        "data_dependencies": ["Active DTC list", "DtcDatabase descriptions"],
        "operation_invoked": "CheckCodesOperation -> ReadDtcCommand (0x19 0x02 0x8D) / ResetCodesOperation (0x14 FF FF FF)",
        "ecu_feature_relation": "Target ECU or MULTI_ECU",
        "user_inputs": [
            "Fault Code item click (opens freeze frame/detail)",
            "'Clear Fault Codes' button",
            "'Share / Export Report' button",
            "'AI Diagnose' button"
        ],
        "safety_gates": [
            "MANDATORY CONFIRMATION DIALOG before clearing DTCs",
            "Engine must be OFF when issuing Service 0x14"
        ],
        "result_error_states": ["CodesReadSuccessfully", "CodesClearedSuccessfully", "ClearFailed_ConditionsNotCorrect", "EcuRefusedClear"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.freezeframe.FreezeFrameDataActivity",
        "name": "FreezeFrameDetailScreen",
        "category": "DTC Diagnostics",
        "purpose": "Displays snapshot data recorded by ECU at the exact moment fault occurred: Engine RPM, Vehicle Speed, Coolant Temp, Fuel Pressure, Voltage, Timestamp, Odometer.",
        "entry_points": ["com.prizmos.carista.screens.operation.checkcodes.CheckCodesActivity"],
        "outgoing_navigation": [],
        "data_dependencies": ["FreezeFrameModel parsed from UDS Service 0x19 Subfunction 0x04"],
        "operation_invoked": "UdsService 0x19 0x04 [DTC 3 bytes] [RecordNum]",
        "ecu_feature_relation": "ECU that logged the fault (e.g. Engine 0x01)",
        "user_inputs": ["Back button", "Share snapshot button"],
        "safety_gates": ["Read-only operation"],
        "result_error_states": ["SnapshotLoaded", "NoFreezeFrameAvailable"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.showsettingcategories.ShowSettingCategoriesActivity",
        "name": "CustomizationCategoriesScreen",
        "category": "Customizations / Coding",
        "purpose": "Displays hierarchical tree of customization categories: Doors / Windows / Sunroof, Lights, Instruments, Dings & Warnings, Driver Assist, Mirrors, Chassis.",
        "entry_points": ["com.prizmos.carista.screens.operation.main.MainActivity"],
        "outgoing_navigation": [
            "com.prizmos.carista.screens.operation.showsettings.ShowSettingsActivity",
            "com.prizmos.carista.screens.operation.restore.RestoreActivity"
        ],
        "data_dependencies": ["Category list from FeatureRegistry", "Vehicle applicability profile"],
        "operation_invoked": "CheckSettingsOperation",
        "ecu_feature_relation": "CENTRAL_ELEC (0x09), INSTRUMENTS (0x17), GATEWAY (0x19), DOOR_MODULES (0x42/0x52)",
        "user_inputs": ["Category item click", "Search filter query", "'Restore Backups' button"],
        "safety_gates": ["Hides categories completely if no installed ECU supports them"],
        "result_error_states": ["CategoriesLoaded", "NoCustomizationsApplicable"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.showsettings.ShowSettingsActivity",
        "name": "CustomizationListScreen",
        "category": "Customizations / Coding",
        "purpose": "Displays individual settings within selected category, showing current configured value, applicability status, and locked/unlocked state.",
        "entry_points": ["com.prizmos.carista.screens.operation.showsettingcategories.ShowSettingCategoriesActivity"],
        "outgoing_navigation": [
            "com.prizmos.carista.screens.operation.changesetting.ChangeSettingActivity",
            "com.prizmos.carista.FeatureDetailsActivity",
            "com.prizmos.carista.UnlockSettingActivity"
        ],
        "data_dependencies": ["List of Setting models in category", "Current values read from vehicle"],
        "operation_invoked": "ReadValuesOperation -> ReadDataByIdentifier (0x22 DID) or KWP Adaptation Read (0x21 Channel)",
        "ecu_feature_relation": "Category-specific ECU (0x09, 0x17, 0x19, 0x5F, etc.)",
        "user_inputs": ["Setting item click", "Refresh values button"],
        "safety_gates": ["Verifies ECU communication before rendering setting value"],
        "result_error_states": ["ValuesPopulated", "ReadTimeout", "SecurityAccessRequired"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.changesetting.ChangeSettingActivity",
        "name": "ChangeSettingScreen",
        "category": "Customizations / Coding",
        "purpose": "Interactive configuration dialog for a single setting. Renders appropriate input control based on interpretation: RadioGroup for MultipleChoice, Stepper/Slider for Numerical, TextInput for Text.",
        "entry_points": ["com.prizmos.carista.screens.operation.showsettings.ShowSettingsActivity"],
        "outgoing_navigation": [
            "com.prizmos.carista.PricingActivity"
        ],
        "data_dependencies": ["Target Setting object", "Current value", "Allowed values / bounds"],
        "operation_invoked": "ChangeSettingOperation -> [1. Backup] -> [2. SecurityAccess] -> [3. WriteDataByIdentifier 0x2E] -> [4. Read-Back Verify]",
        "ecu_feature_relation": "Target ECU for setting",
        "user_inputs": ["Value selection (radio / slider / input)", "'Save / Apply' button", "'Cancel' button"],
        "safety_gates": [
            "ENGINE MUST BE OFF, IGNITION ON",
            "BATTERY VOLTAGE >= 12.0V REQUIRED",
            "AUTOMATIC BACKUP RECORDED TO REALM BEFORE WRITE",
            "IMMEDIATE READ-BACK VERIFICATION"
        ],
        "result_error_states": [
            "SettingSavedSuccessfully",
            "NRC_22_ConditionsNotCorrect",
            "NRC_31_RequestOutOfRange",
            "NRC_33_SecurityAccessDenied",
            "VerificationMismatch"
        ]
    },
    {
        "class": "com.prizmos.carista.screens.operation.restore.RestoreActivity",
        "name": "RestoreSettingsBackupScreen",
        "category": "Customizations / Coding",
        "purpose": "Displays history of previous configuration backups for current vehicle. Allows 1-click rollback of all modified settings to factory or earlier snapshot.",
        "entry_points": ["com.prizmos.carista.screens.operation.showsettingcategories.ShowSettingCategoriesActivity"],
        "outgoing_navigation": [],
        "data_dependencies": ["Realm VehicleEntity -> SettingHistory backup records"],
        "operation_invoked": "RestoreOperation -> Sequential WriteValuesOperation of historical values",
        "ecu_feature_relation": "All modified ECUs in snapshot",
        "user_inputs": ["Backup snapshot item click", "'Restore Selected Snapshot' button", "'Delete Backup' button"],
        "safety_gates": [
            "CRITICAL WARNING DIALOG: confirms overwrite of multiple ECU parameters",
            "Ignition ON, Engine OFF, Voltage Check"
        ],
        "result_error_states": ["RestoreComplete", "PartialRestoreWarning", "RestoreFailed"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.showavailabletools.ShowAvailableToolsActivity",
        "name": "ServiceToolsMenuScreen",
        "category": "Service Tools",
        "purpose": "Displays available service tools applicable to connected vehicle: Electronic Parking Brake (EPB), DPF Regeneration, Battery Registration, Service Indicator Reset, TPMS Tools.",
        "entry_points": ["com.prizmos.carista.screens.operation.main.MainActivity"],
        "outgoing_navigation": [
            "com.prizmos.carista.GenericToolActivity",
            "com.prizmos.carista.screens.operation.serviceindicator.ServiceIndicatorActivity",
            "com.prizmos.carista.screens.operation.tpms.TpmsActivity",
            "com.prizmos.carista.screens.operation.batteryhealth.BatteryHealthSummaryActivity",
            "com.prizmos.carista.screens.operation.emissiontests.EmissionTestsActivity"
        ],
        "data_dependencies": ["CheckAvailableToolsOperation results", "Discovered ECU list"],
        "operation_invoked": "CheckAvailableToolsOperation",
        "ecu_feature_relation": "EPB (0x53), ENGINE (0x01), GATEWAY (0x19), CLUSTER (0x17), TPMS (0x65)",
        "user_inputs": ["Service Tool item click"],
        "safety_gates": ["Only displays tools supported by vehicle's specific ECU variants"],
        "result_error_states": ["ToolsLoaded", "NoServiceToolsSupported"]
    },
    {
        "class": "com.prizmos.carista.GenericToolActivity",
        "name": "GenericServiceToolRunnerScreen",
        "category": "Service Tools",
        "purpose": "Multi-step stateful wizard executing routine-based OEM service procedures (Electronic Parking Brake retraction/closure, DPF regeneration, ABS bleed).",
        "entry_points": ["com.prizmos.carista.screens.operation.showavailabletools.ShowAvailableToolsActivity"],
        "outgoing_navigation": [],
        "data_dependencies": ["ServiceToolDefinition", "Active ECU connection"],
        "operation_invoked": "GenericToolOperation -> [Session 0x03] -> [RoutineControl 0x31 0x01/0x02] -> [Poll Status DID 0x0102]",
        "ecu_feature_relation": "PARKING_BRAKE (0x53) / ENGINE (0x01) / ABS (0x03)",
        "user_inputs": [
            "'Next / Proceed' button",
            "'Start Routine' button",
            "'Stop / Abort' button",
            "'Finish' button"
        ],
        "safety_gates": [
            "RIGID SAFETY INSTRUCTIONS (e.g. For EPB: Vehicle on level ground, wheel chocks in place, parking brake disengaged)",
            "Safety confirmation checkbox must be checked before action button is enabled",
            "Abort button immediately issues RoutineStop (31 02 <RoutineId>)"
        ],
        "result_error_states": [
            "RoutineStarted",
            "RoutineCompletedSuccessfully (0x10)",
            "RoutineInProgress (0xC0)",
            "RoutineAbortedSafety (0x40)",
            "RoutineConditionsIncorrect (0x60)",
            "RoutineTimeout (0x80)"
        ]
    },
    {
        "class": "com.prizmos.carista.screens.operation.serviceindicator.ServiceIndicatorActivity",
        "name": "ServiceIndicatorResetScreen",
        "category": "Service Tools",
        "purpose": "Reads current service inspection / oil change intervals (days and kilometers remaining) and provides 1-click reset of inspection light and oil change light.",
        "entry_points": ["com.prizmos.carista.screens.operation.showavailabletools.ShowAvailableToolsActivity"],
        "outgoing_navigation": [],
        "data_dependencies": ["Instrument Cluster service interval adaptation values"],
        "operation_invoked": "ServiceIndicatorOperation -> Read DIDs 0x2260/0x2261 -> Write 0x2E / Channel 0x02 = 0x00",
        "ecu_feature_relation": "INSTRUMENT_CLUSTER (0x17)",
        "user_inputs": ["'Reset Oil Service' button", "'Reset Inspection Service' button"],
        "safety_gates": ["Confirmation prompt before resetting counter"],
        "result_error_states": ["IntervalsLoaded", "ResetSuccessful", "ResetRefusedByCluster"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.tpms.TpmsActivity",
        "name": "TpmsToolScreen",
        "category": "Service Tools",
        "purpose": "Displays current Tire Pressure Monitoring System status: registered sensor IDs, current pressures, temperatures, battery levels, and TPMS relearn / ID registration wizard.",
        "entry_points": ["com.prizmos.carista.screens.operation.showavailabletools.ShowAvailableToolsActivity"],
        "outgoing_navigation": [],
        "data_dependencies": ["Direct TPMS sensor packet structures or Indirect TPMS calibration status"],
        "operation_invoked": "ReadTpmsInfoOperation / WriteTpmsIdsOperation / RelearnTpmsIdsOperation",
        "ecu_feature_relation": "TIRE_PRESSURE_MONITOR (0x65) / ABS (0x03)",
        "user_inputs": ["Sensor position selector", "Enter 8-hex sensor ID", "'Write IDs' button", "'Calibrate' button"],
        "safety_gates": ["Sensor ID hex length and checksum validation", "Vehicle must be stationary during write"],
        "result_error_states": ["SensorDataLoaded", "IdsWrittenSuccessfully", "RelearnInitiated", "SensorReadTimeout"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.showlivedata.ShowLiveDataActivity",
        "name": "LiveDataCategoriesScreen",
        "category": "Live Data",
        "purpose": "Presents categories of live real-time sensor parameters available for the vehicle: Engine parameters, Transmission, ABS/Brakes, Battery/Electrical, HVAC.",
        "entry_points": ["com.prizmos.carista.screens.operation.main.MainActivity"],
        "outgoing_navigation": ["com.prizmos.carista.screens.operation.livedata.LiveDataActivity"],
        "data_dependencies": ["Live parameter catalog (LIVE_DATA_INDEX.json)", "ECU discovery list"],
        "operation_invoked": "CheckLiveDataOperation",
        "ecu_feature_relation": "ENGINE (0x01), TRANSMISSION (0x02), ABS (0x03), GATEWAY (0x19)",
        "user_inputs": ["Parameter category click", "Parameter search filter", "Select all / Deselect checkboxes"],
        "safety_gates": ["Restricts max simultaneous polled parameters (typically 4-6) to ensure high sample rate"],
        "result_error_states": ["CategoriesLoaded", "NoLiveDataParametersAvailable"]
    },
    {
        "class": "com.prizmos.carista.screens.operation.livedata.LiveDataActivity",
        "name": "LiveDataMonitorScreen",
        "category": "Live Data",
        "purpose": "Real-time live telemetry display. Renders chosen parameters as digital readouts, gauges, or scrolling line graphs with live min/max tracking.",
        "entry_points": ["com.prizmos.carista.screens.operation.showlivedata.ShowLiveDataActivity"],
        "outgoing_navigation": [],
        "data_dependencies": ["Active ReadLiveDataOperation continuous flow"],
        "operation_invoked": "ReadLiveDataOperation -> Periodic UDS 0x22 DID / OBD2 Mode 01 PID polling loop",
        "ecu_feature_relation": "Polled target ECUs",
        "user_inputs": ["Pause / Resume polling button", "Change display mode (Gauges vs Table vs Graphs)", "Record log button"],
        "safety_gates": ["Automatically pauses if battery voltage drops critically or CAN buffer overflows"],
        "result_error_states": ["StreamingActive", "StreamPaused", "SamplingThrottled", "EcuDropped"]
    },
    {
        "class": "com.prizmos.carista.ShowEcuListActivity",
        "name": "EcuListEngineeringScreen",
        "category": "Diagnostics / Engineering",
        "purpose": "Displays raw list of all detected ECUs on CAN/K-Line bus with their VAG addresses, standard names, and communication status.",
        "entry_points": ["Developer / Advanced Diagnostics menu", "com.prizmos.carista.screens.operation.fullscan.FullScanActivity"],
        "outgoing_navigation": ["com.prizmos.carista.ShowEcuActivity"],
        "data_dependencies": ["Gateway installation list", "Active ECU instances"],
        "operation_invoked": "GetEcuListOperation",
        "ecu_feature_relation": "All ECUs",
        "user_inputs": ["ECU item click", "Refresh list button"],
        "safety_gates": ["Read-only gateway query"],
        "result_error_states": ["EcuListLoaded"]
    },
    {
        "class": "com.prizmos.carista.ShowEcuActivity",
        "name": "EcuDetailEngineeringScreen",
        "category": "Diagnostics / Engineering",
        "purpose": "Detailed low-level view of a single ECU: VAG Part Number, Software Version, Hardware Version, ASAM/ODX File ID and Version, System Component Name, Coding Bytes (Long Coding).",
        "entry_points": ["com.prizmos.carista.ShowEcuListActivity", "com.prizmos.carista.screens.operation.fullscan.FullScanActivity"],
        "outgoing_navigation": [
            "com.prizmos.carista.InputDataIdActivity",
            "com.prizmos.carista.ChangeBitwiseRawValueActivity",
            "com.prizmos.carista.ChangeDecimalRawValueActivity"
        ],
        "data_dependencies": ["Selected ECU address"],
        "operation_invoked": "GetEcuInfoOperation -> Read DIDs 0xF187, 0xF189, 0xF191, 0xF19E, 0xF1A2, 0xF197, 0xF1A3",
        "ecu_feature_relation": "Target ECU",
        "user_inputs": [
            "'Read Raw DID' button",
            "'Raw Long Coding Editor' button",
            "Copy ECU info to clipboard"
        ],
        "safety_gates": ["Warning prompt before opening raw coding editor"],
        "result_error_states": ["EcuInfoLoaded", "DidsNotSupported"]
    },
    {
        "class": "com.prizmos.carista.GarageActivity",
        "name": "GarageVehicleListScreen",
        "category": "Garage & History",
        "purpose": "Displays user's saved vehicles, cached scan reports, maintenance history logs, and customization backups.",
        "entry_points": ["com.prizmos.carista.screens.operation.main.MainActivity", "com.prizmos.carista.MoreActivity"],
        "outgoing_navigation": [
            "com.prizmos.carista.NameVehicleActivity",
            "com.prizmos.carista.screens.garage.history.GarageHistoryActivity"
        ],
        "data_dependencies": ["Realm VehicleEntity database"],
        "operation_invoked": "Realm::where(VehicleEntity.class).findAll()",
        "ecu_feature_relation": "Local persistence",
        "user_inputs": ["Vehicle card click", "'Add Vehicle' button", "'Delete Vehicle' button"],
        "safety_gates": ["Confirmation prompt before vehicle profile deletion"],
        "result_error_states": ["GarageLoaded"]
    }
]

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_json = os.path.join(base_dir, "research", "molecular", "UI_SCREEN_GRAPH.json")
    out_md = os.path.join(base_dir, "research", "molecular", "UI_SCREEN_GRAPH.md")

    graph_data = {
        "metadata": {
            "title": "Carista Molecular UI / Product Screen Graph",
            "total_screens_documented": len(SCREENS_DEFINITION),
            "date": "2026-09-25",
            "architecture": "Clean-Room Functional Structure (Non-Proprietary)"
        },
        "screens": SCREENS_DEFINITION
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2)
    print(f"[+] Wrote {out_json}")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Molecular UI / Product Screen Graph\n\n")
        f.write(f"Total Functional Screens Documented: **{len(SCREENS_DEFINITION)}**  \n")
        f.write("This document provides the end-to-end screen navigation, operations invoked, data dependencies, and safety gates reconstructed directly from `classes2.dex` and `libCarista.so.c`.\n\n")

        f.write("## 1. High-Level Flow Chart\n\n")
        f.write("```mermaid\n")
        f.write("flowchart TD\n")
        f.write("    ConnectActivity[\"ConnectScreen<br/>(Adapter Selection)\"] --> ConnectToVehicleActivity[\"ConnectingScreen<br/>(VIN & Protocol Detection)\"]\n")
        f.write("    ConnectToVehicleActivity --> ConfirmVehicleActivity[\"ConfirmVehicleScreen<br/>(VIN / Model Confirmation)\"]\n")
        f.write("    ConfirmVehicleActivity --> MainActivity[\"VehicleDashboardScreen<br/>(Operation Hub)\"]\n")
        f.write("    MainActivity --> FullScanActivity[\"AutoScanScreen<br/>(Gateway Discovery & DTCs)\"]\n")
        f.write("    MainActivity --> CheckCodesActivity[\"DtcDiagnosticsScreen<br/>(Read / Clear DTCs)\"]\n")
        f.write("    MainActivity --> ShowSettingCategoriesActivity[\"CustomizationCategoriesScreen<br/>(Settings Tree)\"]\n")
        f.write("    MainActivity --> ShowAvailableToolsActivity[\"ServiceToolsMenuScreen<br/>(EPB, DPF, Service Reset)\"]\n")
        f.write("    MainActivity --> ShowLiveDataActivity[\"LiveDataCategoriesScreen<br/>(Sensors Selection)\"]\n")
        f.write("    ShowSettingCategoriesActivity --> ShowSettingsActivity[\"CustomizationListScreen<br/>(Category Settings)\"]\n")
        f.write("    ShowSettingsActivity --> ChangeSettingActivity[\"ChangeSettingScreen<br/>(Modify & Safe Write)\"]\n")
        f.write("    ShowSettingCategoriesActivity --> RestoreActivity[\"RestoreSettingsBackupScreen<br/>(1-Click Rollback)\"]\n")
        f.write("    ShowAvailableToolsActivity --> GenericToolActivity[\"GenericServiceToolRunnerScreen<br/>(EPB Retract / DPF Regen)\"]\n")
        f.write("    ShowAvailableToolsActivity --> ServiceIndicatorActivity[\"ServiceIndicatorResetScreen<br/>(Oil / Inspection Reset)\"]\n")
        f.write("    ShowAvailableToolsActivity --> TpmsActivity[\"TpmsToolScreen<br/>(TPMS Relearn / ID Register)\"]\n")
        f.write("    ShowLiveDataActivity --> LiveDataActivity[\"LiveDataMonitorScreen<br/>(Real-Time Gauges & Logs)\"]\n")
        f.write("    CheckCodesActivity --> FreezeFrameDataActivity[\"FreezeFrameDetailScreen<br/>(Fault Snapshot DIDs)\"]\n")
        f.write("```\n\n")

        f.write("## 2. Screen Specifications & Safety Invariants\n\n")
        for sc in SCREENS_DEFINITION:
            f.write(f"### `{sc['name']}` (`{sc['class']}`)\n\n")
            f.write(f"- **Category**: `{sc['category']}`\n")
            f.write(f"- **Purpose**: {sc['purpose']}\n")
            f.write(f"- **Entry Points**: {', '.join(f'`{e}`' for e in sc['entry_points'])}\n")
            f.write(f"- **Outgoing Navigation**: {', '.join(f'`{o}`' for o in sc['outgoing_navigation']) if sc['outgoing_navigation'] else 'None (Terminal Screen)'}\n")
            f.write(f"- **Data Dependencies**: {', '.join(sc['data_dependencies'])}\n")
            f.write(f"- **Operation Invoked**: `{sc['operation_invoked']}`\n")
            f.write(f"- **ECU / Feature Relation**: `{sc['ecu_feature_relation']}`\n")
            f.write(f"- **User Inputs**: {', '.join(sc['user_inputs'])}\n")
            f.write(f"- **Safety Gates & Confirmation**: {', '.join(sc['safety_gates'])}\n")
            f.write(f"- **Result / Error States**: {', '.join(f'`{r}`' for r in sc['result_error_states'])}\n\n")
            f.write("---\n\n")

    print(f"[+] Wrote {out_md}")

if __name__ == "__main__":
    main()
