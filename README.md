# Ghidra Carista Reverse Engineering & VAG OBD2 Specification

Дослідницький репозиторій аналізу архітектури діагностичного додатку Carista OBD та детальна специфікація для реалізації власного чистого діагностичного стеку (VAG UDS / ISO-TP / CAN / ELM327).

---

## 🗺️ Карта реверсу: Що де шукати (Reverse Engineering Map)

Якщо ви або ШІ шукаєте конкретну функцію чи алгоритм, ось точна карта розміщення компонентів між шарами:

```
Carista XAPK
├── Java / Kotlin (DEX: classes.dex) -> [JADX] UI, Bluetooth сокет, моделі екранів
├── Native ELF (libCarista.so)       -> [Ghidra] UDS диспетчери, розрахунки, протоколи
├── Encrypted Assets (*.iap)        -> [PairIP] Зашифровані конфігурації
└── Remote Backend (api.carista.com)-> [REST API] SFD токени, ODX описи під VIN
```

### 1. Рівень Java/Kotlin (Аналіз у JADX через `jadx-gui`)
Відкривати файл: `extracted/com.prizmos.carista.apk`

| Що шукаємо | Де знаходиться (Java-пакет / клас) | Що саме реверсити |
|---|---|---|
| **Bluetooth / BLE підключення** | `com.prizmos.carista.library.connection` | Пошук адаптерів, створення BluetoothSocket RFCOMM (UUID `00001101...`), обробка відключення |
| **Фільтрація та типи адаптерів** | `AndroidDevice`, `DeviceLatestInfo` | Списки підтримуваних імен (Carista, OBDLink, Kiwi, vLinker) та перевірка на дефектні клони ELM (`isDefectiveNative`) |
| **Список функцій кодування (UI)** | `com.prizmos.carista.library.model.Setting*` | Категорії налаштувань (`SettingCategory`), текстові описи, дисклеймери безпеки |
| **Назви блоків та опис помилок** | `res/values/strings.xml` | Локалізовані назви блоків керування (01 Двигун, 03 ABS...), коди помилок та тексти попереджень |

---

### 2. Рівень нативного коду C++ (Аналіз у Ghidra через `carista.gpr`)
Відкривати програму: `libCarista.so` (або текстовий лістинг `libCarista.so.c`)

| Функціонал | Ключові класи / Символи у C++ | Що саме реверсити |
|---|---|---|
| **Діагностика VAG CAN/UDS** | `VagUdsCommunicator`, `VagCanCommunicator` | Точні послідовності байтів для відправки UDS команд: сесії `10 03`, Keep-alive `3E 80`, читання `22`, запис `2E` |
| **Зчитування помилок DTC** | `VagUdsTroubleCode`, `VagCanTroubleCode` | Маска запиту `19 02 09`, парсинг 3-байтового коду несправності та байта статусу (Pending/Confirmed) |
| **Розведення колодок EPB** | `VagBasicSettingTool`, `BmwECanEpbOperation` | Номери рутин сервісу `0x31` (RoutineControl) для відкриття супортів, зведення та адаптації |
| **Скидання сервісу оливи (WIV)** | `VagServiceIndicator`, `ServiceIndicatorModel` | Номери каналів адаптацій та DID (`0x2260`, `0x2261`) для скидання пробігу і днів після ТО |
| **Прописка акумулятора** | `VagUdsBatteryRegOperation`, `BatteryRegOperation` | Послідовність запису ємності АКБ (Ah), технології (AGM/EFB) та серійного номера |
| **Регенерація сажового фільтра** | `VagCanDpfTool`, `BmwFDpfTool` | Сервіси моніторингу маси сажі/золи в грамах та запуск примусової регенерації на ходу/місці |
| **Довге кодування (Long Coding)**| `VagUdsCodingSetting`, `VagCanCodingSetting` | Читання DID `F1A3`, бітові маски активації прихованих функцій (тест стрілок, DRL, звук замків) |

---

### 3. Специфікація та База Доказів (Clean-Room Evidence Base)
Усі константи та структури даних на 100% верифіковані проти бінарного файлу `libCarista.so` та лістингу `libCarista.so.c`:
- 📦 **[research/INVENTORY.md](research/INVENTORY.md)** — Криптографічний опис усіх 19 артефактів із хешами SHA-256.
- 📋 **[research/SPEC_AUDIT.md](research/SPEC_AUDIT.md)** — Детальний аудит попередньої специфікації: виправлення критичних помилок адресації (EPB 0x752 vs HVAC 0x746, BCM 0x70E, рутини 0x03A1/0x03A0).
- 📚 **[research/protocols/](research/protocols/)** — 17 повних технічних специфікацій протоколів (ELM327, STN, CAN, ISO-TP, KWP2000, UDS, адресація VAG, сесії, DTC, Live Data, кодування, адаптації, базові налаштування, сервісні процедури, безпека).
- 🗄️ **[research/db/](research/db/)** — Машиночитані бази даних: `diagnostic_evidence.json`, `diagnostic_evidence.csv`, `vag_ecus.json` (17 блоків керування).
- 🔄 **[research/state_machines/](research/state_machines/)** — Стейт-машини життєвого циклу підключення, UDS сесій та сервісних процедур у форматі Mermaid.
- 🚀 **[handoff/](handoff/)** — Повний пакет передачі для розробки Android додатку на Kotlin (ChatGPT handoff):
  - `handoff/IMPLEMENTATION_BRIEF.md` — Технічне завдання та інструкція для імплементації.
  - `handoff/VERIFIED_COMMANDS.json` — Готовий JSON зі 100% верифікованими байтами команд.
  - `handoff/OPEN_QUESTIONS.md` — Відкриті архітектурні питання та roadmap.

---

## 🛠️ Інструменти аналізу в репозиторії
У папці `tools/` зібрано інструменти вилучення метаданих та генерації документації:
- `tools/generate_inventory.py` — генерація матриці артефактів із хешами.
- `tools/export_ghidra_evidence.py` — вилучення 12,667 символів та 477 класів команд із `libCarista.so.c`.
- `tools/generate_protocol_docs.py` — автогенерація 17 файлів специфікацій протоколів.
- `tools/generate_databases.py` — компіляція реляційних баз знань (`diagnostic_evidence.json`, `vag_ecus.json`).
- `tools/generate_state_machines.py` — побудова Mermaid діаграм станів.
- `tools/generate_spec_audit.py` — компіляція звіту аудиту специфікацій та непідтверджених гіпотез.
- `tools/generate_handoff.py` — складання підсумкового брифа та верифікованих команд для наступного агента.
- `tests/verify_protocol.py` — набір автоматизованих тестів симулятора протоколу (8/8 тестів успішно).
- `ghidra_scripts/ExportEvidence.java` — офіційний Java-скрипт експорту символів та RTTI для Ghidra GUI/Headless.

