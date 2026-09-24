# Product Functional Architecture Map (Carista Clean-Room)

## 1. Top-Level Functional Structure

The application is structured into four primary operational modes:

```
Carista Core Product Map
├── 1. Connect & Detect Mode
│   ├── Adapter Discovery (BLE GATT & Classic RFCOMM)
│   ├── Vehicle Bus Detection (CAN 500k / TP2.0 / K-Line)
│   └── Vehicle Identification (VIN 0xF190 & Gateway List 0x04A1)
│
├── 2. Diagnostics Mode
│   ├── Full Vehicle AutoScan (Multi-ECU query)
│   ├── DTC Inspector (P/C/B/U standard + VAG decimal code + symptom)
│   ├── Freeze Frame Data Viewer (Snapshot values at time of failure)
│   └── DTC Clear (14 FF FF FF across all modules)
│
├── 3. Customizations (Coding & Adaptations) Mode
│   ├── Categories Screen (29 functional categories)
│   ├── Setting Details Screen (Current value read & choices)
│   ├── Value Change & Write (Live byte patching & verification)
│   └── Backup & Restore Manager (Saved customization rollback)
│
├── 4. Service Tools Mode
│   ├── Electronic Parking Brake (EPB service mode retract & close)
│   ├── DPF Regeneration (Stationary & emergency driving regen)
│   ├── Battery Registration (Ah, AGM/EFB, brand, serial)
│   ├── Service Indicator Reset (Oil & inspection intervals)
│   └── TPMS Tool (Read sensor IDs, pressures & relearn)
│
└── 5. Live Data Mode
    ├── Parameter Selection (Engine, Transmission, Battery, Turbo, DPF)
    ├── Real-Time Polling Engine (Periodic 0x22 / Mode 01 requests)
    └── Gauge / Graph Display
```

---

## 2. Safety Interlocks & Confirmation Dialogs

For safety-critical service operations, the application enforces prerequisite gates:

| Service Tool | Mandatory Prerequisites | Confirmation Dialog Message |
|---|---|---|
| **EPB Caliper Retract** | 1. Vehicle stationary<br>2. Level surface<br>3. Handbrake switch OFF<br>4. Battery voltage > 12.4V | "Warning: Caliper motors will physically move. Keep hands away from brake assembly. Do not press brake pedal during procedure." |
| **DPF Forced Regeneration** | 1. Engine coolant > 70°C<br>2. Fuel level > 25%<br>3. Vehicle outdoors (extreme exhaust heat)<br>4. Hood closed | "Caution: Exhaust gas temperature will exceed 650°C. Ensure vehicle is parked outside away from dry grass or flammable materials." |
| **Clear All DTCs** | 1. Ignition ON<br>2. Engine OFF | "Engine must be turned off before clearing diagnostic memory to avoid ECU communication refusal." |
| **Coding Write** | 1. Battery voltage > 12.0V<br>2. Pre-write backup verified | "Writing new configuration to ECU. Do not turn off ignition or disconnect adapter." |
