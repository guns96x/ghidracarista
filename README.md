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

### 3. Специфікація для власної реалізації
Повний архітектурний опис із чистими прикладами реалізації на Kotlin знаходиться у файлі:
📄 **[VAG_OBD_Diagnostic_Specification.md](VAG_OBD_Diagnostic_Specification.md)**

---

## 🛠️ Інструменти аналізу в репозиторії
У папці `tools/` зібрано допоміжні Python-скрипти швидкого вилучення метаданих:
- `analyze_so.py` — пошук JNI функцій, AT-команд та C++ RTTI типів.
- `inspect_deep.py` — аналіз OEM-підсистем (VAG, BMW, Toyota, Ford) та мережевих ендпоінтів.
- `extract_architecture.py` — витяг станів та UDS-сервісів.
- `extract_routines.py` — пошук рутин RoutineControl, ReadDataByIdentifier та BasicSetting.
- `extract_epb.py` — детальний зріз класів EPB, DPF та скидання сервісу.
