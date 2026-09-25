# Molecular Network & Backend Boundary Analysis

This document identifies the boundary between **local vehicle diagnostic operations** and **remote cloud backend dependencies** in Carista.

---

## 1. Architectural Boundary Map

```mermaid
flowchart TD
    subgraph Vehicle & Local Phone Boundary (100% Offline Capable)
        Adapter["OBD2 Adapter (ELM327 / BLE / RFCOMM)"]
        ProtoCore["Protocol Engine (ISO-TP, UDS, TP2.0, KWP)"]
        AutoScan["AutoScan & Gateway Discovery (DID 0x04A1)"]
        DTC["Fault Code Read & Clear (19 02 8D / 14 FF FF FF)"]
        Service["Service Tools (EPB 03A1, DPF 053D, Battery Reg, Reset)"]
        Coding["Customizations & Coding (PQ35, MQB pre-2020, MLB)"]
        LiveSensors["Live Telemetry Gauges (PIDs / DIDs)"]
        LocalDB["Local Cache & Coding Backups (Realm / Room SQLite)"]
        
        Adapter <--> ProtoCore
        ProtoCore <--> AutoScan
        ProtoCore <--> DTC
        ProtoCore <--> Service
        ProtoCore <--> Coding
        ProtoCore <--> LiveSensors
        LocalDB <--> Coding
        LocalDB <--> DTC
    end

    subgraph Remote Cloud Boundary (Internet Connection Required)
        BackendAPI["Carista Backend (api.caristaapp.com / io.caristaapp.com)"]
        SFDServer["Volkswagen AG SFD Backend (Online Token Authority)"]
        BillingAPI["Subscription & Paywall (Adapty / Google Play Billing)"]
        AnalyticsAPI["Telemetry (Mixpanel, Firebase, Adjust, OneSignal)"]
        
        BackendAPI <--> SFDServer
    end

    Coding -.->|"SFD Token Request (MQB2020+ Only)"| BackendAPI
    Coding -.->|"Subscription Check (Commercial Lock)"| BillingAPI
    AutoScan -.->|"Uncached DTC Text Lookup"| BackendAPI
    AutoScan -.->|"Event Telemetry"| AnalyticsAPI
```

---

## 2. Feature Independence Matrix

| Feature Area | Execution Context | Network Dependency | Can Operate Completely Offline? | Fallback / Remediation |
|---|---|---|---|---|
| **Adapter Connection** | Local Bluetooth / BLE / WiFi | None | **YES (100%)** | No network needed |
| **Vehicle Detection & VIN** | Local CAN / UDS 0xF190 | None | **YES (100%)** | Decoded from VIN characters locally |
| **Gateway Discovery** | Local UDS 0x04A1 | None | **YES (100%)** | Raw 4-byte installation record parsing |
| **DTC Read & Clear** | Local UDS 0x19 / 0x14 | Optional (text descriptions) | **YES (100%)** | Bundle standard SAE/VAG fault code dictionary locally |
| **EPB Caliper Retract** | Local Routine 0x03A1 | None (on pre-SFD) | **YES (100%)** | Direct UDS routine control |
| **DPF Emergency Regen** | Local Routine 0x053D | None | **YES (100%)** | Uses standard login codes (27971 / 12233) |
| **Battery Registration** | Local Gateway Adaptation | None | **YES (100%)** | Direct UDS 0x2E adaptation |
| **Service Reset** | Local Cluster Adaptation | None | **YES (100%)** | Direct cluster write |
| **Standard Customizations** | Local UDS Long Coding | Commercial Paywall | **YES (100%)** | Free / open implementation without subscription check |
| **MQB2020+ SFD Coding** | Hybrid Local / Cloud | **MANDATORY (Online Token)** | **NO** | Volkswagen Group SFD requires cryptographically signed end-to-end token from VW servers. Gated/blocked in UI. |
| **Account & Profiles** | Cloud Server | Mandatory for Carista Cloud | **YES (100% via Local Room DB)** | Autonomous app uses local SQLite database for vehicle profiles |

---

## 3. Remote Backend API Endpoints Discovered

1. **`https://api.caristaapp.com`**:
   - `CaristaApiClient::requestSfd2Token`: Exchanges VIN, controller address, and diagnostic request for signed SFD2 unlock token.
   - `CaristaApiClient::requestTroubleCodeDescriptions`: Fetches proprietary OEM DTC descriptions by ECU part number and fault code.
   - `CaristaApiClient::checkSubscription`: Verifies user tier before enabling "Save" button in UI.
2. **`https://io.caristaapp.com`**:
   - Telemetry ingestion and diagnostic session log upload (`UploadLogActivity`).
3. **Third-Party Services**:
   - `api.mixpanel.com`: User funnel telemetry.
   - `api.onesignal.com`: Push notifications.
   - `firebaseremoteconfig.googleapis.com`: Dynamic feature flags.

---

## 4. Architectural Rules for Autonomous Implementation

1. **Zero External Server Dependency for Core Diagnostics**:
   - All protocol handling, DTC decoding, AutoScan, Service Tools, and standard Long Coding must execute 100% offline on the Android device.
2. **Offline Fault Code Dictionary**:
   - The app must bundle an offline VAG/SAE trouble code database so DTC descriptions display without network connectivity.
3. **SFD Invariant**:
   - Do NOT attempt to fabricate, crack, or fake SFD unlock tokens. If an ECU on MQB2020+ reports SFD protection active (NRC `0x33` SecurityAccessDenied or SFD state detected), gracefully display: `"Feature requires Volkswagen AG SFD unlock token (MQB2020+ platform protection)."`
