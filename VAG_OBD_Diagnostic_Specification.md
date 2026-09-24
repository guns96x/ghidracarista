# Специфікація та Архітектурний Blueprint: Автомобільна діагностика VAG (UDS / ISO-TP / ELM327)

> Цей документ є повною практичною інструкцією та технічним стандартом для розробника (або ШІ-агента), який дозволяє створити власний автономний діагностичний додаток без сторонніх пропрієтарних бібліотек.

---

## 1. Загальна Архітектура Системи (System Topology)

```mermaid
flowchart TD
    subgraph APP [Рівень Додатка (Kotlin / Compose)]
        UI[UI Screens: AutoScan, LiveData, ServiceTools, Coding]
        VM[ViewModels & StateFlow State Machine]
        DB[(Room DB: DTC базa, логи, кеш блоків)]
    end

    subgraph PROTOCOL [Рівень Протоколів (core-protocol)]
        UDS[UdsCommunicator: ISO 14229]
        ISOTP[IsoTpHandler: ISO 15765-2 Segmentation]
        KWP[Kwp2000Handler: Для старих блоків VAG]
    end

    subgraph TRANSPORT [Рівень Транспорту (core-transport)]
        AT[Elm327Engine: Черга AT-команд, парсинг, тайм-аути]
        BT[BluetoothManager: Classic SPP / BLE GATT]
    end

    subgraph HARDWARE [Апаратний Рівень]
        Adapter[Адаптер ELM327 v1.5 / vLinker MC / OBDLink]
        CarBus[CAN шина 500 kbps / Блоки ECU]
    end

    UI --> VM
    VM --> UDS
    VM --> DB
    UDS --> ISOTP
    ISOTP --> AT
    AT --> BT
    BT <-->|Bluetooth RFCOMM / BLE| Adapter
    Adapter <-->|ISO 15765-4 11-bit CAN| CarBus
```

---

## 2. Адаптер та Транспортний Рівень (ELM327 / STN / vLinker)

### 2.1 Послідовність ініціалізації (Handshake Sequence)
При підключенні до Bluetooth-сокета (SPP UUID: `00001101-0000-1000-8000-00805F9B34FB`) виконується наступний ланцюжок команд:

| Крок | Команда | Очікувана відповідь | Опис призначення |
|:---:|:---:|:---:|---|
| 1 | `AT WS` або `AT Z` | `ELM327 v...` | Повне перезавантаження мікроконтролера адаптера |
| 2 | `AT E0` | `OK` | Вимкнення відлуння (Echo Off) — прибирає введений текст із відповіді |
| 3 | `AT L0` | `OK` | Вимкнення символу переводу рядка (Linefeeds Off) |
| 4 | `AT S0` | `OK` | Вимкнення пробілів між байтами (значно прискорює парсинг) |
| 5 | `AT H1` | `OK` | Увімкнення заголовків (Headers On) — дозволяє бачити CAN ID відправника |
| 6 | `AT AL` | `OK` | Дозволити довгі повідомлення (Allow Long messages > 7 байт) |
| 7 | `AT SP 6` | `OK` | Фіксація протоколу: **ISO 15765-4 CAN (11 bit ID, 500 kbaud)** |

> [!NOTE]
> Для адаптерів **vLinker** або **OBDLink** рекомендується додати команду `STP 33` або `AT PB 0000`, що переводить чіп у високошвидкісний режим буферизації.

---

## 3. Адресація блоків керування VAG (ECU Addressing)

Для роботи з конкретним блоком відправляються дві команди конфігурації фільтра адаптера:
1. `AT SH <TxID>` — встановлення заголовка відправника (Tx).
2. `AT CRA <RxID>` — встановлення фільтра прийому тільки від цього блока (Rx).

### Таблиця основних блоків VAG (Платформи PQ35, MQB, MLB):

| Назва блока | Номер | Tx CAN ID | Rx CAN ID | Команди перемикання |
|---|:---:|:---:|:---:|---|
| **Двигун (Engine ECU)** | `01` | `0x7E0` | `0x7E8` | `AT SH 7E0` <br> `AT CRA 7E8` |
| **АКПП (Transmission TCU)** | `02` | `0x7E1` | `0x7E9` | `AT SH 7E1` <br> `AT CRA 7E9` |
| **Гальмівна система (ABS/ESP)** | `03` | `0x713` | `0x77D` | `AT SH 713` <br> `AT CRA 77D` |
| **Блок комфорту / Електроніка (BCM)** | `09` | `0x709` | `0x773` | `AT SH 709` <br> `AT CRA 773` |
| **Панель приладів (Instrument Cluster)** | `17` | `0x714` | `0x77E` | `AT SH 714` <br> `AT CRA 77E` |
| **Діагностичний шлюз (CAN Gateway)** | `19` | `0x710` | `0x77A` | `AT SH 710` <br> `AT CRA 77A` |
| **Подушки безпеки (Airbag)** | `15` | `0x715` | `0x77F` | `AT SH 715` <br> `AT CRA 77F` |
| **Стоянкове гальмо (EPB)** | `53` | `0x746` | `0x7B0` | `AT SH 746` <br> `AT CRA 7B0` |

---

## 4. Специфікація UDS Сервісів (ISO 14229)

Коли адаптер налаштований на блок (наприклад, `AT SH 7E0`), відправляються байти діагностичних сервісів. 

Успішна відповідь блоку завжди має байт `Service ID + 0x40`. Якщо сталася помилка, блок повертає `7F <Service ID> <Negative Response Code>`.

### 4.1 Сесії та Keep-Alive
* **0x10 DiagnosticSessionControl**:
  * `10 01` — Стандартна сесія (Default Session). Відповідь: `50 01 ...`
  * `10 03` — **Extended Diagnostic Session** (обов'язкова для кодування, скидання та сервісних функцій). Відповідь: `50 03 ...`
* **0x3E TesterPresent (Keep-Alive)**:
  * `3E 80` — відправка кожні 2–3 секунди у фоновому потоці. Байт `80` вказує блоку не відповідати, щоб не засмічувати шину (SuppressPositiveResponse).

---

### 4.2 Читання ідентифікаторів блока (Сервіс 0x22 ReadDataByIdentifier)
Відправляється `22 <DID_High> <DID_Low>`. Відповідь починається з `62 <DID_High> <DID_Low> <Data>`.

| Функція | DID | Запит | Опис та парсинг відповіді |
|---|:---:|:---:|---|
| **VIN-код авто** | `0xF190` | `22 F1 90` | Відповідь `62 F1 90 [17 байт ASCII]` — стандартний 17-значний VIN |
| **Номер запчастини (Part No)** | `0xF187` | `22 F1 87` | Номер блоку VAG (наприклад, `03G906021QJ` або `5Q0937084CF`) в ASCII |
| **Версія ПЗ (SW Version)** | `0xF189` | `22 F1 89` | Версія софту прошивки (4 байти ASCII, наприклад `9971` або `0436`) |
| **Версія Заліза (HW Version)** | `0xF191` | `22 F1 91` | Апаратна ревізія плати (ASCII) |
| **Довге кодування (Long Coding)** | `0xF1A3` | `22 F1 A3` | Рядок кодування блоку (від 10 до 30 байт у Hex) |

---

### 4.3 Робота з помилками DTC (Сервіси 0x19 та 0x14)
* **Зчитування помилок:**
  * Запит: `19 02 09`
    * `0x19` = ReadDTCInformation
    * `0x02` = ReportDTCByStatusMask
    * `0x09` = Маска (TestFailed [bit 0] + ConfirmedDTC [bit 3])
  * Формат відповіді: `59 02 09 [DTC1_H] [DTC1_M] [DTC1_L] [Status1] ...`
  * Розшифровка 3 байтів DTC у стандартний VAG / SAE код:
    ```kotlin
    fun decodeDtc(byte1: Int, byte2: Int, byte3: Int): String {
        val prefix = when ((byte1 and 0xC0) ushr 6) {
            0 -> "P" // Powertrain
            1 -> "C" // Chassis
            2 -> "B" // Body
            3 -> "U" // Network
            else -> "P"
        }
        val d1 = (byte1 and 0x30) ushr 4
        val d2 = byte1 and 0x0F
        val d3 = (byte2 and 0xF0) ushr 4
        val d4 = byte2 and 0x0F
        val faultType = byte3 // Ознака типу відмови (Fault Symptom)
        return "%s%X%X%X%X-%02X".format(prefix, d1, d2, d3, d4, faultType)
    }
    ```
* **Стирання помилок:**
  * Запит: `14 FF FF FF` (Очистити всі групи).
  * Успішна відповідь: `54` (Positive Response).

---

### 4.4 Сервісні процедури (Сервіс 0x31 RoutineControl)
Запит: `31 <SubFunction> <RoutineID_High> <RoutineID_Low> [Data]`
* `SubFunction`: `01` = StartRoutine, `02` = StopRoutine, `03` = RequestRoutineResults.

#### А. Розведення гальмівних колодок EPB (Блок 53 або 03):
1. `10 03` (Перехід в Extended Session).
2. `31 01 00 10` (Старт процедури відкриття супортів для заміни колодок).
3. Після фізичної заміни: `31 01 00 11` (Зведення супортів).
4. `31 01 00 12` (Калібрування та базове налаштування EPB).

#### Б. Скидання інтервалів ТО (Service Indicator Reset):
На свіжих VAG (MQB) здійснюється записом значень у DID адаптацій блоку приладів (`0x17`):
1. DID `0x2260` (WIV: Distance since last oil change) ➔ Запис `2E 22 60 00 00` (Скидання пробігу на 0 км).
2. DID `0x2261` (WIV: Time since last oil change) ➔ Запис `2E 22 61 00 00` (Скидання днів на 0).

---

## 5. Готовий еталонний Kotlin модуль зв'язку

Цей клас можна скопіювати та використовувати в Android-проєкті:

```kotlin
package com.custom.obd.core

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.InputStream
import java.io.OutputStream

class VagDiagnosticEngine(
    private val input: InputStream,
    private val output: OutputStream
) {
    // 1. Відправка сирої команди в сокет та очікування символу '>'
    suspend fun sendRaw(command: String): String = withContext(Dispatchers.IO) {
        output.write((command + "\r").toByteArray(Charsets.US_ASCII))
        output.flush()

        val buffer = ByteArray(1024)
        val sb = StringBuilder()
        while (true) {
            val count = input.read(buffer)
            if (count == -1) break
            val part = String(buffer, 0, count, Charsets.US_ASCII)
            sb.append(part)
            if (sb.contains(">")) break // ELM327 завершує всі відповіді символом '>'
        }
        sb.toString().replace(">", "").trim()
    }

    // 2. Ініціалізація ELM327 під CAN 500k VAG
    suspend fun connect(): Boolean {
        sendRaw("AT Z")
        sendRaw("AT E0")
        sendRaw("AT L0")
        sendRaw("AT S0")
        sendRaw("AT H1")
        val proto = sendRaw("AT SP 6")
        return proto.contains("OK")
    }

    // 3. Перемикання на конкретний блок VAG
    suspend fun selectEcu(txId: String, rxId: String) {
        sendRaw("AT SH $txId")
        sendRaw("AT CRA $rxId")
    }

    // 4. Зчитування VIN авто (DID 0xF190)
    suspend fun readVin(): String? {
        val raw = sendRaw("22 F1 90")
        val clean = raw.replace(" ", "").replace("\r", "").replace("\n", "")
        val marker = "62F190"
        val idx = clean.indexOf(marker)
        if (idx == -1) return null

        val payloadHex = clean.substring(idx + marker.length)
        return payloadHex.chunked(2)
            .mapNotNull {
                try { it.toInt(16).toChar() } catch (e: Exception) { null }
            }
            .joinToString("")
            .filter { it.isLetterOrDigit() }
    }

    // 5. Очищення пам'яті несправностей DTC
    suspend fun clearDtc(): Boolean {
        val resp = sendRaw("14 FF FF FF")
        return resp.contains("54")
    }
}
```

---

## 6. Рекомендована дорожня карта розробки (Roadmap)

1. **Фаза 1: Транспорт:** 
   Створення Android Bluetooth Scanner + підключення через SPP до адаптера, перевірка відповіді `AT Z` та `AT SP 6`.
2. **Фаза 2: Сканування блоків (AutoScan):**
   Послідовний перебір блоків з таблиці розділу 3 (`01`, `02`, `03`, `09`, `17`, `19`) ➔ зчитування наявності блоку за відповіддю на `22 F1 87`.
3. **Фаза 3: Моніторинг DTC:**
   Зчитування помилок через `19 02 09` для кожного знайденого блоку, їх парсинг у зрозумілий користувачу список і кнопка «Очистити всі помилки».
4. **Фаза 4: Сервісні інструменти:**
   Реалізація окремих екранів під EPB (розведення гальм) та скидання інтервалу заміни оливи.
