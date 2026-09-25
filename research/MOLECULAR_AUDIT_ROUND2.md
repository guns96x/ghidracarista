# Molecular Decomposition Strict Audit — Round 2

Commit audited: `1efbba0c`

Status: **REJECTED AS IMPLEMENTATION SOURCE**

## Key findings

- The generator still contains fallback/default synthesis.
- Command mapping is still produced by generic text rules rather than exact protocol builders.
- Diagnostics/service tools are incorrectly forced into a normal Setting schema.
- ECU transport IDs are partially hard-coded and wrong for multiple ECUs.
- The validation suite hard-codes the expected result of 470 READY / 8 BLOCKED, creating circular validation.

## Concrete bad examples

### AutoScan
The setting index models AutoScan as a coding setting with F1A3/byte0/mask1 metadata. That is structurally false.

### DTC Clear
ClearDiagnosticInformation is an operation, not a coding setting.

### EPB
The command-map generator can produce generic 2204A1/2E04A1 based on string heuristics instead of the directly evidenced RoutineControl commands.

### Engine addressing
The generated ECU transport mapping falls through to generic 0x70E/0x778 for addresses that are not explicitly handled.

## Acceptance rule

A feature is accepted only if its complete mapping is derived from the exact constructor/object/request-builder callsite and argument positions. No fallback/default inference is allowed.

The previous 470 READY / 8 BLOCKED result remains invalid.
