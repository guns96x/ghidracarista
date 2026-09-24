# Open Questions & Investigation Log for Next AI Stage

1. **CAN-FD Transport Support on Low-Cost Adapters**:
   - Standard ELM327 does not support CAN-FD (required for some MQB-evo diagnostics).
   - Recommendation: Require vLinker FD / MC+ or OBDLink EX for full MQB-evo access, while falling back to 500k classical CAN on PQ35/MQB.

2. **Submodule LIN Slave Coding**:
   - Slaves (Wiper motor, Rain/Light sensor) on PQ35 are coded via BCM Master (`3B 9A <SubId> <Coding>`). On MQB, slaves are coded via DID `0x0608` / `0x0609`.
   - Need empirical validation on live vehicle for MQB LIN slave write framing.

3. **Battery Registration DID Variants**:
   - Gateway (`0x19`) Battery Adaptation uses DID `0x2A1B` (Serial), `0x2A1C` (Vendor), `0x2A1D` (Capacity) on MQB, whereas older platforms used channel adaptation.
   - Recommended: Implement both channel and DID adaptation paths based on ECU software level.
