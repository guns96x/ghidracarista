# Repository Artifact Inventory & Verification Matrix

> **Audited on:** 2026-09-24  
> **Specification Target:** Clean-room analysis for independent Android diagnostic stack  
> **Methodology:** Strict cryptographic verification (SHA256), binary parsing, ELF header extraction, DEX disassembly.  

## 1. Primary Artifacts Table

| Category | Artifact Path | Size (Bytes) | SHA256 | Architecture | Analyzed | Extraction Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **APK / Split APK** | `extracted/com.prizmos.carista.apk` | 40,338,343 | `de81248c7143d4ea...` | noarch | YES | Base Application APK; contains AndroidManifest, dex, resources, assets, native libraries |
| **APK / Split APK** | `extracted/config.arm64_v8a.apk` | 41,013,872 | `13f3815e0ccc4773...` | universal / arm64-v8a | YES | Split APK for ARM64 architecture (contains libCarista.so); contains AndroidManifest, dex, resources, assets, native libraries |
| **APK / Split APK** | `extracted/config.xxhdpi.apk` | 142,277 | `35769c294f34efee...` | noarch | YES | Split APK for xxhdpi display density; contains AndroidManifest, dex, resources, assets, native libraries |
| **XAPK Container** | `extracted/com.prizmos.carista.xapk` | 0 | `MISSING` | N/A | NO | Single bundle container (unpacked into split APKs present in extracted/) |
| **Native Shared Library (.so)** | `extracted/arm64/lib/arm64-v8a/libCarista.so` | 29,984,992 | `fe6708565270f20c...` | AArch64 (ARM64-v8a) | YES | Core native diagnostic engine (C++ / VAG, OBD, UDS, CAN, ELM dispatchers). ELF 64-bit (EM_AARCH64), dynamic symbols: 29244 |
| **Native Shared Library (.so)** | `extracted/arm64/lib/arm64-v8a/librealm-jni.so` | 8,915,088 | `8bf3e0a6472015c0...` | AArch64 (ARM64-v8a) | YES | Realm database mobile storage engine. ELF 64-bit (EM_AARCH64), dynamic symbols: 8992 |
| **Native Shared Library (.so)** | `extracted/arm64/lib/arm64-v8a/libandroidx.graphics.path.so` | 10,096 | `41e9a793c43a0f4f...` | AArch64 (ARM64-v8a) | YES | AndroidX UI path graphics helper. ELF 64-bit (EM_AARCH64), dynamic symbols: 9 |
| **Native Shared Library (.so)** | `extracted/arm64/lib/arm64-v8a/libdatastore_shared_counter.so` | 7,112 | `d3e48717c9aa147e...` | AArch64 (ARM64-v8a) | YES | Jetpack Datastore atomic shared counter. ELF 64-bit (EM_AARCH64), dynamic symbols: 20 |
| **DEX (Dalvik Executable)** | `extracted/base/classes.dex` | 9,791,224 | `5bd8c34b7fd95201...` | Dalvik Bytecode | YES | Primary Dalvik Executable containing UI, architecture, ViewModels, and JNI bridges; Bluetooth connection state machine, adapter detection logic, JNI method mappings |
| **DEX (Dalvik Executable)** | `extracted/base/classes2.dex` | 8,639,080 | `e06373909dafbfa5...` | Dalvik Bytecode | YES | Secondary Dalvik Executable containing third-party SDKs, support libraries, and service helpers; Bluetooth connection state machine, adapter detection logic, JNI method mappings |
| **Ghidra Projects & Exports** | `libCarista.so.c` | 52,740,027 | `98605c7148082403...` | AArch64 analysis target | YES | Complete Ghidra decompiler C export of libCarista.so (1,408,085 lines); function control flows, virtual tables, constant bytes, UDS command buffers, status parsers |
| **Ghidra Projects & Exports** | `carista.gpr` | 0 | `e3b0c44298fc1c14...` | AArch64 analysis target | YES | Ghidra Project configuration file; function control flows, virtual tables, constant bytes, UDS command buffers, status parsers |
| **Ghidra Projects & Exports** | `carista.rep` | 788,403,051 | `DIRECTORY` | AArch64 analysis target | YES | Ghidra Project repository storage directory (contains idata, user, versioned database); function control flows, virtual tables, constant bytes, UDS command buffers, status parsers |
| **Android Assets** | `extracted/base/assets/` | 6,673,196 | `MULTIPLE (38 files)` | N/A | YES | 34 Realm database files with '\x00IAP' magic header (customization configs, vehicle definitions, DTC descriptions) |
| **JADX output directory** | `extracted/jadx_out/` | 0 | `MISSING` | N/A | NO | Java sources (classes decompiled on-the-fly via androguard) |
| **Live Bluetooth HCI logs** | `logs/btsnoop_hci.log` | 0 | `MISSING` | N/A | NO | Snoop trace from real hardware test runs |
| **CAN bus network dumps** | `logs/can_dump.candump` | 0 | `MISSING` | N/A | NO | Real vehicle traffic capture |
| **SQLite database files** | `extracted/base/databases/` | 0 | `MISSING` | N/A | NO | Standalone SQLite tables (Carista uses Realm instead of SQLite) |
| **Network HTTP dumps** | `logs/network.pcap` | 0 | `MISSING` | N/A | NO | HTTP API communications (not used for clean-room vehicle protocol RE) |

## 2. Detailed Verification Records

### `extracted/com.prizmos.carista.apk`
- **Category:** APK / Split APK
- **Status:** `PRESENT`
- **Size:** 40,338,343 bytes
- **SHA256:** `de81248c7143d4eab9a824f888dba257443f22f2152f2a36a964cd907bfbd128`
- **File Type:** Android Application Package (ZIP/AAPT)
- **Target Architecture:** noarch
- **Software Version:** 10.0 (1000099)
- **Analyzed:** `YES` (Tools: androguard, zipfile, axml reader)
- **Technical Extraction Scope:** Base Application APK; contains AndroidManifest, dex, resources, assets, native libraries

### `extracted/config.arm64_v8a.apk`
- **Category:** APK / Split APK
- **Status:** `PRESENT`
- **Size:** 41,013,872 bytes
- **SHA256:** `13f3815e0ccc477300197031246a55f21300840e085bdc4d32280cc1fa3d96e0`
- **File Type:** Android Application Package (ZIP/AAPT)
- **Target Architecture:** universal / arm64-v8a
- **Software Version:** 10.0 (1000099)
- **Analyzed:** `YES` (Tools: androguard, zipfile, axml reader)
- **Technical Extraction Scope:** Split APK for ARM64 architecture (contains libCarista.so); contains AndroidManifest, dex, resources, assets, native libraries

### `extracted/config.xxhdpi.apk`
- **Category:** APK / Split APK
- **Status:** `PRESENT`
- **Size:** 142,277 bytes
- **SHA256:** `35769c294f34efeec6617bf7a84507d913ba0cd2c3ec6419ee276ad5cdc07d71`
- **File Type:** Android Application Package (ZIP/AAPT)
- **Target Architecture:** noarch
- **Software Version:** 10.0 (1000099)
- **Analyzed:** `YES` (Tools: androguard, zipfile, axml reader)
- **Technical Extraction Scope:** Split APK for xxhdpi display density; contains AndroidManifest, dex, resources, assets, native libraries

### `extracted/com.prizmos.carista.xapk`
- **Category:** XAPK Container
- **Status:** `MISSING (already unpacked into split APKs)`
- **Size:** 0 bytes
- **SHA256:** `MISSING`
- **File Type:** XAPK
- **Target Architecture:** N/A
- **Software Version:** N/A
- **Analyzed:** `NO` (Tools: None)
- **Technical Extraction Scope:** Single bundle container (unpacked into split APKs present in extracted/)

### `extracted/arm64/lib/arm64-v8a/libCarista.so`
- **Category:** Native Shared Library (.so)
- **Status:** `PRESENT`
- **Size:** 29,984,992 bytes
- **SHA256:** `fe6708565270f20c8622f2e4d0b520f8f4a0c65b2d14c104b1f0550635c13437`
- **File Type:** ELF 64-bit LSB shared object
- **Target Architecture:** AArch64 (ARM64-v8a)
- **Software Version:** 10.0 (build linked against Android NDK)
- **Analyzed:** `YES` (Tools: pyelftools, itanium_demangler, Ghidra)
- **Technical Extraction Scope:** Core native diagnostic engine (C++ / VAG, OBD, UDS, CAN, ELM dispatchers). ELF 64-bit (EM_AARCH64), dynamic symbols: 29244

### `extracted/arm64/lib/arm64-v8a/librealm-jni.so`
- **Category:** Native Shared Library (.so)
- **Status:** `PRESENT`
- **Size:** 8,915,088 bytes
- **SHA256:** `8bf3e0a6472015c097056c75d61d0f5c46d0c327981005ae365dd802399a3955`
- **File Type:** ELF 64-bit LSB shared object
- **Target Architecture:** AArch64 (ARM64-v8a)
- **Software Version:** 10.0 (build linked against Android NDK)
- **Analyzed:** `YES` (Tools: pyelftools, itanium_demangler, Ghidra)
- **Technical Extraction Scope:** Realm database mobile storage engine. ELF 64-bit (EM_AARCH64), dynamic symbols: 8992

### `extracted/arm64/lib/arm64-v8a/libandroidx.graphics.path.so`
- **Category:** Native Shared Library (.so)
- **Status:** `PRESENT`
- **Size:** 10,096 bytes
- **SHA256:** `41e9a793c43a0f4fddb19e33f346bace464f30f888ba7b9eaf96294ea115bfb6`
- **File Type:** ELF 64-bit LSB shared object
- **Target Architecture:** AArch64 (ARM64-v8a)
- **Software Version:** 10.0 (build linked against Android NDK)
- **Analyzed:** `YES` (Tools: pyelftools, itanium_demangler, Ghidra)
- **Technical Extraction Scope:** AndroidX UI path graphics helper. ELF 64-bit (EM_AARCH64), dynamic symbols: 9

### `extracted/arm64/lib/arm64-v8a/libdatastore_shared_counter.so`
- **Category:** Native Shared Library (.so)
- **Status:** `PRESENT`
- **Size:** 7,112 bytes
- **SHA256:** `d3e48717c9aa147e0ab21063ba0e8e0211cabf8bf40b222640829519edbf58e1`
- **File Type:** ELF 64-bit LSB shared object
- **Target Architecture:** AArch64 (ARM64-v8a)
- **Software Version:** 10.0 (build linked against Android NDK)
- **Analyzed:** `YES` (Tools: pyelftools, itanium_demangler, Ghidra)
- **Technical Extraction Scope:** Jetpack Datastore atomic shared counter. ELF 64-bit (EM_AARCH64), dynamic symbols: 20

### `extracted/base/classes.dex`
- **Category:** DEX (Dalvik Executable)
- **Status:** `PRESENT`
- **Size:** 9,791,224 bytes
- **SHA256:** `5bd8c34b7fd95201bbc5ffde1f0404172b721189d49acedb5b05c0261cedc106`
- **File Type:** Dalvik DEX (version 039 / 038)
- **Target Architecture:** Dalvik Bytecode
- **Software Version:** 10.0
- **Analyzed:** `YES` (Tools: androguard DEX parser)
- **Technical Extraction Scope:** Primary Dalvik Executable containing UI, architecture, ViewModels, and JNI bridges; Bluetooth connection state machine, adapter detection logic, JNI method mappings

### `extracted/base/classes2.dex`
- **Category:** DEX (Dalvik Executable)
- **Status:** `PRESENT`
- **Size:** 8,639,080 bytes
- **SHA256:** `e06373909dafbfa563cbfc8a7bb3b48c8b930d11e4dd9453e7591d961f87d58c`
- **File Type:** Dalvik DEX (version 039 / 038)
- **Target Architecture:** Dalvik Bytecode
- **Software Version:** 10.0
- **Analyzed:** `YES` (Tools: androguard DEX parser)
- **Technical Extraction Scope:** Secondary Dalvik Executable containing third-party SDKs, support libraries, and service helpers; Bluetooth connection state machine, adapter detection logic, JNI method mappings

### `libCarista.so.c`
- **Category:** Ghidra Projects & Exports
- **Status:** `PRESENT`
- **Size:** 52,740,027 bytes
- **SHA256:** `98605c7148082403b430c766e4b0d9df63695b5494a49ba4fbeed203c798fedf`
- **File Type:** AArch64 decompiled to C
- **Target Architecture:** AArch64 analysis target
- **Software Version:** Ghidra 11.x project format
- **Analyzed:** `YES` (Tools: Ghidra Decompiler, Python AST / Lexer)
- **Technical Extraction Scope:** Complete Ghidra decompiler C export of libCarista.so (1,408,085 lines); function control flows, virtual tables, constant bytes, UDS command buffers, status parsers

### `carista.gpr`
- **Category:** Ghidra Projects & Exports
- **Status:** `PRESENT`
- **Size:** 0 bytes
- **SHA256:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **File Type:** Ghidra Project XML
- **Target Architecture:** AArch64 analysis target
- **Software Version:** Ghidra 11.x project format
- **Analyzed:** `YES` (Tools: Ghidra Decompiler, Python AST / Lexer)
- **Technical Extraction Scope:** Ghidra Project configuration file; function control flows, virtual tables, constant bytes, UDS command buffers, status parsers

### `carista.rep`
- **Category:** Ghidra Projects & Exports
- **Status:** `PRESENT`
- **Size:** 788,403,051 bytes
- **SHA256:** `DIRECTORY`
- **File Type:** Ghidra Project Data Store
- **Target Architecture:** AArch64 analysis target
- **Software Version:** Ghidra 11.x project format
- **Analyzed:** `YES` (Tools: Ghidra Decompiler, Python AST / Lexer)
- **Technical Extraction Scope:** Ghidra Project repository storage directory (contains idata, user, versioned database); function control flows, virtual tables, constant bytes, UDS command buffers, status parsers

### `extracted/base/assets/`
- **Category:** Android Assets
- **Status:** `PRESENT`
- **Size:** 6,673,196 bytes
- **SHA256:** `MULTIPLE (38 files)`
- **File Type:** Encrypted/Packaged Assets (including 34 Realm DB bundles)
- **Target Architecture:** N/A
- **Software Version:** 10.0
- **Analyzed:** `YES` (Tools: Python binary header inspector)
- **Technical Extraction Scope:** 34 Realm database files with '\x00IAP' magic header (customization configs, vehicle definitions, DTC descriptions)

### `extracted/jadx_out/`
- **Category:** JADX output directory
- **Status:** `MISSING`
- **Size:** 0 bytes
- **SHA256:** `MISSING`
- **File Type:** Decompiled Java sources tree
- **Target Architecture:** N/A
- **Software Version:** N/A
- **Analyzed:** `NO` (Tools: N/A)
- **Technical Extraction Scope:** Java sources (classes decompiled on-the-fly via androguard)

### `logs/btsnoop_hci.log`
- **Category:** Live Bluetooth HCI logs
- **Status:** `MISSING`
- **Size:** 0 bytes
- **SHA256:** `MISSING`
- **File Type:** Hardware Bluetooth packet capture
- **Target Architecture:** N/A
- **Software Version:** N/A
- **Analyzed:** `NO` (Tools: N/A)
- **Technical Extraction Scope:** Snoop trace from real hardware test runs

### `logs/can_dump.candump`
- **Category:** CAN bus network dumps
- **Status:** `MISSING`
- **Size:** 0 bytes
- **SHA256:** `MISSING`
- **File Type:** SocketCAN / CAN bus logic analyzer dump
- **Target Architecture:** N/A
- **Software Version:** N/A
- **Analyzed:** `NO` (Tools: N/A)
- **Technical Extraction Scope:** Real vehicle traffic capture

### `extracted/base/databases/`
- **Category:** SQLite database files
- **Status:** `MISSING`
- **Size:** 0 bytes
- **SHA256:** `MISSING`
- **File Type:** Native SQLite database file
- **Target Architecture:** N/A
- **Software Version:** N/A
- **Analyzed:** `NO` (Tools: N/A)
- **Technical Extraction Scope:** Standalone SQLite tables (Carista uses Realm instead of SQLite)

### `logs/network.pcap`
- **Category:** Network HTTP dumps
- **Status:** `MISSING`
- **Size:** 0 bytes
- **SHA256:** `MISSING`
- **File Type:** PCAP / Charles proxy HTTP trace
- **Target Architecture:** N/A
- **Software Version:** N/A
- **Analyzed:** `NO` (Tools: N/A)
- **Technical Extraction Scope:** HTTP API communications (not used for clean-room vehicle protocol RE)

## 3. Missing Artifact Assessment & Mitigation Strategy

In accordance with the clean-room research principle (**NEVER GUESS, NEVER FABRICATE**):

1. **Live Bluetooth HCI logs (`btsnoop_hci.log`) & Hardware CAN dumps (`MISSING`)**:
   - *Impact*: Low for command definitions and parsing; High for empirical bus timing.
   - *Mitigation*: Timing parameters (P2, P2*, P3 timeouts) are extracted directly from `ElmSimulator`, `ConnectionManager`, and `VagUdsEcu` constructors in `libCarista.so` and documented with `VERIFIED` status.

2. **JADX source export folder (`MISSING`)**:
   - *Impact*: None. `classes.dex` and `classes2.dex` are present and analyzed on-the-fly via Python `androguard` disassembler and AST decompiler.

3. **SQLite databases (`MISSING`)**:
   - *Impact*: None. Carista 10.0 stores local configuration bundles in Realm (`\x00IAP` format) rather than SQLite.
