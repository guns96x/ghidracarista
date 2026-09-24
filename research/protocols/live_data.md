# Live Data & Measuring Blocks Specification

## 1. Overview
Real-time parameter measurement on VAG vehicles:
- **UDS**: Data Identifiers (DIDs via Service `0x22`).
- **KWP2000**: Measuring value blocks (Service `0x21` / `ReadDataByLocalIdentifier`).

---

## 2. UDS Measuring DIDs
- Request: `22 <DID>`
- Multi-DID Request: `22 <DID1> <DID2> ...` (Observed in `ReadVagUdsMultipleDataIdCommand`).
- Numeric decoding: Big-endian integer/double representations parsed in `ReadDataByIdentifierCommand<DoubleModel>` (Line 78005) and `UInt32Model` (Line 58341).
