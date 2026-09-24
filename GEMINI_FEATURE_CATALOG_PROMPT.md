# Gemini Task — Full Carista Feature Catalog & Applicability Map

Мета: НЕ писати Android-додаток. Спочатку витягнути з наявних артефактів Carista максимально повний каталог функцій і точну прив'язку до авто/ECU/протоколів/умов.

Працюй автономно. Не питай мене, що робити далі, якщо можеш перевірити сам.

## Основна ціль

Створити доказову базу, яка дозволить іншому AI реалізувати функціональність Carista максимально близько 1:1 за можливостями, без повторного дослідження кожної функції.

Використовуй:
- APK / split APK;
- classes.dex / classes2.dex;
- libCarista.so;
- libCarista.so.c;
- Ghidra project/export;
- assets/*.iap;
- Realm bundles;
- resources/strings;
- JNI bridges;
- existing research/*;
- existing handoff/*.

НЕ зупиняйся на UDS-командах. Потрібен ПОВНИЙ feature catalog.

## 1. Розбери assets / IAP / Realm

Це пріоритет №1.

Встанови:
- формат кожного *.iap;
- чи це Realm / encrypted Realm / custom container;
- schema;
- tables/classes;
- vehicle definitions;
- ECU definitions;
- feature definitions;
- labels;
- ranges;
- values/enums;
- applicability rules;
- model/year/engine/platform matching;
- SW/HW/ASAM matching;
- dependencies/prerequisites;
- command templates;
- read/write parameters;
- categories.

Якщо потрібна декомпресія/дешифрування локальних конфігів, досліди код, який їх читає, і задокументуй формат. Не обходь серверну авторизацію, платні акаунти чи SFD.

## 2. Побудуй повний каталог функцій

Створи:
research/features/FEATURE_CATALOG.json
research/features/FEATURE_CATALOG.csv
research/features/FEATURE_CATALOG.md

Для КОЖНОЇ знайденої функції поля:

- id
- internal_name
- category
- user_visible_name
- description
- OEM
- platform
- vehicle_models
- years
- engine/transmission constraints
- ECU logical address
- ECU name
- ECU matching rules
- protocol
- session
- security requirement
- read operation
- write operation
- routine
- request bytes/template
- response parser
- value type
- allowed values
- scaling
- unit
- prerequisites
- postconditions
- polling
- timeout
- error/NRC handling
- applicability source
- implementation source
- binary function/address
- asset/config source
- confidence
- status

Не вигадувати невідомі поля. Став UNKNOWN.

## 3. Категорії мають покрити ВСЕ

Знайди весь фактичний функціонал, включно з:
- diagnostics / AutoScan;
- DTC read/clear;
- ECU info;
- live data;
- service reset;
- EPB;
- battery registration;
- DPF;
- coding;
- long coding;
- adaptations;
- basic settings;
- lighting;
- DRL;
- locking;
- windows;
- mirrors;
- comfort;
- cluster;
- needle sweep;
- seat-belt settings;
- start/stop;
- steering;
- ABS;
- HVAC;
- infotainment;
- TPMS;
- gateway;
- parking;
- wipers/rain sensor;
- seats;
- trailer;
- camera/radar/ADAS settings if present;
- any BMW/Toyota/etc functionality present in this Carista build.

Не обмежуйся VAG, якщо в артефактах є інші OEM. Але VAG пропрацюй найглибше.

## 4. Feature applicability engine

Знайди, ЯК Carista вирішує:
- чи показувати функцію;
- чи підтримується вона на конкретному авто;
- по VIN?
- ECU part number?
- software version?
- hardware version?
- ASAM/ODX?
- logical address?
- platform?
- model/year/engine?
- capability probe?
- server response?
- local asset rule?

Створи:
research/features/APPLICABILITY_ENGINE.md
research/features/applicability_rules.json

Для кожного правила потрібне evidence.

## 5. Vehicle/ECU database

Створи:
research/db/vehicles.json
research/db/ecu_variants.json

Потрібно максимально витягнути:
- OEM
- model/platform
- year range
- engine/transmission if present
- ECU address
- ECU part number patterns
- HW/SW patterns
- ASAM/ODX identifiers
- supported features
- source asset
- confidence

## 6. Поведінка функцій

Для кожної feature визначити повний flow:

detect support
-> connect ECU
-> session
-> prerequisite read/check
-> read current value
-> user value mapping
-> write/routine
-> response validation
-> polling
-> post-check
-> rollback/abort/error

Створи:
research/features/flows/<feature-id>.json

Для складних сервісних процедур також Mermaid у Markdown.

## 7. UI потрібен лише як функціональна карта

Не копіюй UI/графіку/брендинг.

Але встанови:
- які екрани/категорії існують;
- які feature групуються разом;
- які параметри користувач може вибирати;
- які попередження/confirmation потрібні;
- які результати показуються.

Створи:
research/features/PRODUCT_MAP.md

Це карта функціоналу, не копія дизайну.

## 8. Cross-check

Кожну конкретну команду/ID/feature зістав:
1. asset/config;
2. Java/Kotlin/DEX;
3. native/Ghidra;
4. existing evidence DB;
5. logs, якщо є.

Статуси:
VERIFIED
CORROBORATED
LIKELY
HYPOTHESIS
UNKNOWN

VERIFIED/CORROBORATED тільки коли є реальні докази.

## 9. Знайди суперечності в уже створеній базі

Перевір:
handoff/VERIFIED_COMMANDS.json
research/db/diagnostic_evidence.json
research/db/vag_ecus.json

Зокрема автоматично перевір арифметичні/логічні правила адресації.

Наприклад, якщо правило каже TP2.0 setup = 0x200 + logical address, кожне значення повинно відповідати правилу.

Створи:
research/CONSISTENCY_AUDIT.md
research/consistency_errors.json

Не виправляй мовчки — покажи old/new/evidence.

## 10. Handoff для реалізації

Онови/створи:
handoff/FEATURE_IMPLEMENTATION_INDEX.json
handoff/FULL_FEATURE_MATRIX.md
handoff/IMPLEMENTATION_ORDER.md

FEATURE_IMPLEMENTATION_INDEX.json має бути машинозчитуваним і для кожної feature містити все, що потрібно для реалізації без нового реверсу.

## 11. Критерій завершення

Робота НЕ завершена, якщо знайдено лише кілька десятків команд.

Вона завершена, коли:
- пройдені всі assets/config bundles;
- побудований повний список feature;
- кожна feature прив'язана до applicability;
- є source/evidence;
- є список UNKNOWN;
- є consistency audit;
- можна по FEATURE_IMPLEMENTATION_INDEX.json послідовно реалізувати весь продукт.

Починай з assets/*.iap / Realm, бо там найімовірніше лежить значна частина готової матриці функцій.

Після завершення:
1. git diff;
2. перевір JSON;
3. запусти consistency checks;
4. commit;
5. push.

Не пиши мені план замість виконання. Виконуй.
