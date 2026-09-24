# Transport Layer Specification (Bluetooth Classic RFCOMM & BLE GATT)

## 1. Overview
The transport layer bridges Android's radio stack with the physical OBD-II adapter (ELM327 / STN / vLinker / Carista EVO). Two primary transport mechanisms are supported and verified:
1. **Bluetooth Classic (BR/EDR)**: Serial Port Profile (SPP) via RFCOMM socket.
2. **Bluetooth Low Energy (BLE / Bluetooth 4.0+)**: Custom GATT services with notification characteristics and MTU negotiation.

---

## 2. Bluetooth Classic (RFCOMM / SPP)

### Evidence
- **Source File**: `extracted/base/classes.dex`
- **Class**: `com.prizmos.carista.library.connection.AndroidBluetooth2Connection`
- **Connector**: `com.prizmos.carista.library.connection.AndroidBluetooth2Connector`
- **Scanner**: `com.prizmos.carista.library.connection.Bluetooth2Scanner`
- **Confidence**: `VERIFIED`

### SPP Standard UUID
```
00001101-0000-1000-8000-00805F9B34FB
```
Observed in `classes.dex` string table.

### Connection Procedure
1. Scan paired/bonded devices via `BluetoothAdapter.getBondedDevices()`.
2. Inspect device name and class with `Bluetooth2Scanner.isLikelyObd2Device(device)`:
   - Matches keywords: `OBD`, `Carista`, `vLinker`, `Vgate`, `Viecar`, `OBDLink`.
3. Create RFCOMM socket via `device.createRfcommSocketToServiceRecord(SPP_UUID)`.
4. Connect socket with connection timeout (default 10,000 ms).
5. Establish unbuffered stream reader and writer.

---

## 3. Bluetooth Low Energy (BLE / GATT)

### Evidence
- **Source File**: `extracted/base/classes.dex`
- **Class**: `com.prizmos.carista.library.connection.AndroidBluetooth4Connection`
- **GATT Engine**: `com.prizmos.carista.library.connection.Bluetooth4Gatt`
- **Profiles**: `com.prizmos.carista.library.connection.Bluetooth4Profile`
- **Confidence**: `VERIFIED`

### GATT Architecture & Operation Queue
`Bluetooth4Gatt` implements an asynchronous serialized command queue (`Bluetooth4Gatt.Cmd`) to prevent GATT 133 status errors:
- `Cmd.Connect`: Connect to remote GATT server (`transport = TRANSPORT_LE`).
- `Cmd.RequestMaxMtu`: Requests MTU 512 bytes (`requestMtu(512)`). Observed in `Bluetooth4Gatt$Cmd$RequestMaxMtu`.
- `Cmd.Discover`: Service discovery (`discoverServices()`).
- `Cmd.Subscribe`: Enables characteristic notification via Client Characteristic Configuration Descriptor (`00002902-0000-1000-8000-00805f9b34fb`).
- `Cmd.Write`: Chunks outgoing payload into packets respecting negotiated MTU size (`getBlePacketLength()`).

### Supported BLE Profiles
1. **Carista EVO / Generic BLE (TI CC2540 / Nordic nRF)**:
   - Service: `0000fff0-0000-1000-8000-00805f9b34fb` (or vendor specific)
   - Read/Notify Characteristic: `0000fff1-0000-1000-8000-00805f9b34fb`
   - Write Characteristic: `0000fff2-0000-1000-8000-00805f9b34fb`
2. **OBDLink CX**:
   - Explicit profile class: `Bluetooth4Profile$ObdLinkCx`
3. **Kiwi 3**:
   - Explicit profile class: `Bluetooth4Profile$Kiwi3`

---

## 4. Packet Framing & End-of-Message
- **Delimiter**: Carriage return (`\r` / `0x0D`).
- **Prompt Character**: Prompt character (`>` / `0x3E`) signals adapter readiness.
- **Buffer Timeout**:
  - Command response timeout: 5,000 ms (default).
  - Extended diagnostic service timeout: 10,000 ms.
