# Gemini Research Prompt — clean-room analysis for our own diagnostic app

Ти працюєш над моїм проєктом автомобільної діагностики.

ВАЖЛИВО: моя мета НЕ копіювати Carista, VCDS або будь-який інший додаток. Я хочу створити СВІЙ незалежний Android-додаток для діагностики автомобілів. Існуючі програми використовуються лише як джерело технічного дослідження сумісності, протоколів, поведінки ECU та для перевірки власної реалізації.

Я не програміст. Тому твоя задача — не пояснювати мені, що я повинен зробити вручну, а максимально виконати технічну роботу самостійно у доступному середовищі.

Репозиторій дослідження:
https://github.com/guns96x/ghidracarista

Основний принцип роботи:

НЕ ВГАДУВАТИ.
НЕ ДОМАЛЬОВУВАТИ відсутні дані.
НЕ називати припущення підтвердженим фактом.
НЕ копіювати UI, графіку, тексти, брендинг чи інші творчі елементи Carista.
НЕ намагатися відтворити платну систему Carista, ліцензії, акаунти або обходити серверну авторизацію.

Нас цікавить технічна сумісність:
- Bluetooth / USB transport;
- ELM327 / STN / vLinker;
- CAN;
- ISO-TP;
- K-Line, якщо присутня;
- KWP2000;
- UDS;
- VAG diagnostic addressing;
- ECU discovery;
- sessions;
- DTC;
- measuring values / live data;
- coding;
- adaptations;
- basic settings;
- service routines;
- security/login architecture на рівні документування;
- tester present;
- timeouts;
- retry logic;
- transport state machines;
- request/response parsing;
- ECU identification;
- gateway interaction;
- специфічні відмінності PQ35/MQB/інших платформ.

Не реалізовуй обходи захисту, SFD, серверної авторизації або отримання секретних ключів.

## 1. ГОЛОВНА МЕТА

Перетворити `ghidracarista` з набору нотаток на структуровану доказову базу, яку інший AI/розробник зможе використовувати для реалізації незалежного Android diagnostic stack.

Результатом повинна бути не просто Markdown-стаття.

Потрібні:

1. raw evidence;
2. адреси функцій;
3. назви функцій/класів;
4. XREF;
5. constants;
6. request bytes;
7. response parsing;
8. state transitions;
9. transport configuration;
10. confidence level;
11. machine-readable JSON;
12. короткий handoff для наступного AI, який буде писати Android-додаток.

## 2. СПОЧАТКУ ЗРОБИ ІНВЕНТАРИЗАЦІЮ

Перевір увесь локальний проєкт.

Знайди, якщо присутні:

- APK;
- XAPK;
- split APK;
- libCarista.so;
- інші `.so`;
- DEX;
- resources;
- assets;
- JADX output;
- Ghidra projects;
- Ghidra exports;
- decompiled `.c`;
- strings;
- protobuf;
- JSON;
- SQLite;
- config;
- logs;
- network dumps;
- Bluetooth logs.

Створи:

`research/INVENTORY.md`

Для кожного артефакту вкажи:

- path;
- size;
- SHA256;
- type;
- architecture;
- version, якщо визначається;
- чи проаналізований;
- яким інструментом;
- що з нього можна отримати.

Якщо чогось немає — прямо записати `MISSING`.

Не вигадувати вміст відсутніх файлів.

## 3. GHIDRA

Якщо доступний `libCarista.so`, провести реальний аналіз.

Використовувати Ghidra GUI або headless API/скрипти.

Потрібно знайти:

- exported functions;
- JNI;
- RTTI;
- C++ classes;
- virtual tables;
- protocol-related classes;
- constructors/destructors;
- strings;
- references;
- call graph;
- constants;
- byte arrays;
- switch tables;
- protocol dispatchers.

Особливо дослідити назви/аналоги:

Vag*
Uds*
Kwp*
Can*
IsoTp*
Elm*
Stn*
Bluetooth*
Diagnostic*
Communicator*
TroubleCode*
Coding*
Adaptation*
BasicSetting*
Service*
Epb*
Dpf*
Battery*
Gateway*
Security*
Session*
Transport*

Для кожної цікавої функції зберігати:

- binary;
- architecture;
- virtual address;
- Ghidra function name;
- demangled name;
- namespace/class;
- callers;
- callees;
- referenced strings;
- referenced constants;
- короткий decompiled fragment або псевдокод;
- interpretation;
- confidence.

НЕ достатньо написати:
"Carista використовує UDS".

Потрібно:
"функція X @ address Y викликає Z; містить constant 0x22; будує buffer таким способом; відповідь перевіряється таким способом".

## 4. JADX

Провести аналіз Java/Kotlin частини.

Знайти:

- Bluetooth discovery;
- USB, якщо є;
- RFCOMM;
- BLE;
- UUID;
- connection lifecycle;
- reconnect;
- timeout;
- adapter detection;
- ELM clone detection;
- JNI bridges;
- ViewModel → native calls;
- service commands;
- parsing;
- ECU model objects;
- diagnostic result objects.

Для кожної важливої знахідки:

- APK;
- class;
- method;
- signature;
- source/decompiled line;
- called native method;
- interpretation;
- confidence.

## 5. ПРОТОКОЛЬНА БАЗА

Створи структуру:

`research/protocols/`

окремо:

- `transport.md`
- `elm327.md`
- `stn.md`
- `can.md`
- `isotp.md`
- `kwp2000.md`
- `uds.md`
- `vag_addressing.md`
- `ecu_discovery.md`
- `sessions.md`
- `dtc.md`
- `live_data.md`
- `coding.md`
- `adaptation.md`
- `basic_settings.md`
- `service_routines.md`
- `security_architecture.md`

Але КОЖНЕ конкретне значення повинно мати evidence.

Наприклад:

```
Request:
19 02 FF

Observed in:
libCarista.so
function:
VagUdsTroubleCode::...
address:
0x123456

Evidence:
...

Confidence:
VERIFIED
```

## 6. CONFIDENCE MODEL

Використовуй ТІЛЬКИ такі статуси:

VERIFIED
- безпосередньо знайдено в binary/source/log;
- є точна адреса/XREF/trace.

CORROBORATED
- підтверджується мінімум двома незалежними джерелами.

LIKELY
- сильна непряма ознака.

HYPOTHESIS
- припущення.

UNKNOWN
- даних недостатньо.

Ніякі `LIKELY/HYPOTHESIS` не можна подавати наступному AI як готову команду ECU.

## 7. MACHINE READABLE DATABASE

Створи:

`research/db/diagnostic_evidence.json`

Формат приблизно:

```json
{
  "entries": [
    {
      "id": "...",
      "oem": "VAG",
      "platform": "PQ35",
      "protocol": "UDS",
      "category": "DTC",
      "operation": "read_dtc",
      "request": ["19", "02", "FF"],
      "response_prefix": ["59", "02"],
      "source": {
        "file": "libCarista.so",
        "function": "...",
        "address": "0x..."
      },
      "confidence": "VERIFIED",
      "notes": "..."
    }
  ]
}
```

Не вставляй дані без evidence.

Також зроби CSV:

`research/db/diagnostic_evidence.csv`

## 8. ECU / ADDRESS DATABASE

Окремо створити:

`research/db/vag_ecus.json`

Поля:

- VAG address;
- logical name;
- platform;
- transport;
- tx CAN ID;
- rx CAN ID;
- protocol;
- session;
- evidence;
- confidence.

НЕ об'єднувати PQ35, MQB, MLB в одну універсальну таблицю, якщо binary цього не підтверджує.

## 9. SERVICE ROUTINES

Особливо ретельно перевірити все, що може щось змінити в автомобілі:

- EPB;
- DPF;
- adaptations;
- coding;
- service reset;
- battery registration;
- basic settings.

Для цих операцій недостатньо знайти один hex constant.

Потрібно встановити:

- ECU;
- protocol;
- required session;
- prerequisite checks;
- request;
- parameters;
- response;
- negative responses;
- timeout;
- tester present;
- stop/abort behavior;
- platform/model applicability.

Якщо цього немає — позначити `INCOMPLETE`.

## 10. LIVE DATA

Визначити:

- DID;
- measuring block;
- request;
- raw format;
- length;
- endian;
- signed/unsigned;
- scale;
- offset;
- unit;
- valid range.

Не вигадувати scaling.

Якщо відома лише DID — записати DID, а scaling = UNKNOWN.

## 11. STATE MACHINES

Для connection/diagnostic flows побудувати state machine.

Наприклад:

DISCONNECTED
→ CONNECTING
→ ADAPTER_INIT
→ BUS_INIT
→ ECU_SELECTED
→ SESSION_START
→ ACTIVE
→ RECOVERY / ERROR

Встановити це з коду, а не придумати.

Зберегти:

`research/state_machines/*.md`

і бажано Mermaid diagrams.

## 12. АВТОМАТИЗАЦІЯ GHIDRA

Поточні regex scripts у `tools/` — недостатні.

Створи реальні Ghidra scripts для експорту:

- functions;
- symbols;
- namespaces;
- strings;
- XREF;
- call graph;
- constants;
- byte arrays;
- decompiled code metadata.

Папка:

`ghidra_scripts/`

Результат запуску:

`research/ghidra_export/`

JSON має бути придатний для автоматичного аналізу іншим AI.

## 13. НЕ ЗАМІНЮЙ ДОКАЗИ ЗАГАЛЬНИМИ ЗНАННЯМИ

Стандарт ISO 14229 може казати, що `0x22` = ReadDataByIdentifier.

Це не означає, що конкретна Carista-функція використовує конкретний DID.

Чітко розділяй:

STANDARD
OBSERVED_IN_CARISTA
OBSERVED_IN_LOG
INFERRED

## 14. ПЕРЕВІР ІСНУЮЧУ СПЕЦИФІКАЦІЮ

Перевір:

`VAG_OBD_Diagnostic_Specification.md`

Кожен конкретний:

- CAN ID;
- DID;
- Routine ID;
- service sequence;
- timeout;
- command;
- formula

порівняти з реальною evidence base.

Створи:

`research/SPEC_AUDIT.md`

Таблиця:

Claim
Evidence
Status
Correction
Confidence

Помилкові або непідтверджені твердження не видаляти безслідно.

Перенести їх у:

`research/unverified_claims.md`

## 15. HANDOFF ДЛЯ CHATGPT

Це КРИТИЧНО.

Метою дослідження є те, що інший AI — ChatGPT — буде реалізовувати Android-додаток.

Створи:

`handoff/IMPLEMENTATION_BRIEF.md`

У ньому не повинно бути довгої води.

Структура:

1. What is VERIFIED
2. What is CORROBORATED
3. What remains UNKNOWN
4. Transport API required
5. Protocol API required
6. ECU discovery algorithm
7. Session management
8. DTC API
9. LiveData API
10. Coding API
11. Adaptation API
12. BasicSettings API
13. Safety requirements
14. Suggested Kotlin interfaces
15. Test vectors
16. Exact paths to evidence files

Також:

`handoff/VERIFIED_COMMANDS.json`

ТІЛЬКИ VERIFIED/CORROBORATED.

І:

`handoff/OPEN_QUESTIONS.md`

## 16. TEST VECTORS

Створи тестові vectors з реальних знайдених прикладів:

request
raw response
expected parsed response

Наприклад:

```json
{
  "request": "22F190",
  "rawFrames": [],
  "expected": {
    "vin": "..."
  }
}
```

Але не вигадувати реальний VIN чи response.

Якщо немає response — тест не створювати.

## 17. GIT

Всю роботу вести у Git.

Перед змінами:

`git status`

Після логічного етапу:

- перевірити diff;
- commit;
- push.

Коміти робити маленькими і зрозумілими.

Наприклад:

`research: add binary inventory and hashes`
`research: add Ghidra evidence exporter`
`research: map VAG UDS dispatcher`
`docs: audit diagnostic specification`
`handoff: add verified implementation brief`

Не робити destructive rewrite history.

## 18. НЕ ПИТАЙ МЕНЕ ТЕХНІЧНИХ ПИТАНЬ, ЯКІ МОЖЕШ ВИРІШИТИ САМ

Я не програміст.

Не зупиняй роботу словами:

"можете запустити..."
"тепер вам потрібно..."
"відкрийте Ghidra..."
"перевірте..."

Якщо інструмент доступний — запускай сам.

Якщо задача велика — виконуй послідовно.

Якщо один метод не працює — використовуй інший.

Зупинитися дозволено лише якщо реально бракує артефакту, якого немає на диску та який неможливо отримати з поточного середовища.

Тоді записати:

BLOCKED:
- що саме відсутнє;
- де очікувалось;
- навіщо потрібне;
- що вже перевірено;
- чи можна продовжити інші частини без нього.

І ПРОДОВЖИТИ все інше, що можливо.

## 19. НЕ ЗАЙМАЙСЯ UI ДОДАТКА

Зараз твоя головна роль — дослідження і підготовка доказової технічної бази.

Не витрачай час на красивий Android UI.

ChatGPT буде окремо будувати наш власний Android-додаток.

Тобі потрібно максимально зменшити ймовірність того, що при реалізації ChatGPT доведеться щось вгадувати.

## 20. КІНЦЕВИЙ КРИТЕРІЙ

Робота НЕ завершена, якщо просто створено README або кілька Markdown-файлів.

Робота вважається виконаною, коли інший розробник/AI може відкрити:

`handoff/IMPLEMENTATION_BRIEF.md`

та

`handoff/VERIFIED_COMMANDS.json`

і реалізувати незалежний diagnostic stack без необхідності здогадуватись, звідки взялися конкретні protocol constants.

Кожна небезпечна write-operation повинна мати evidence та applicability.

Починай з інвентаризації поточного репозиторію та локальних артефактів.

НЕ проси підтвердження.
НЕ пиши план замість виконання.
Після короткої інвентаризації одразу виконуй роботу.
