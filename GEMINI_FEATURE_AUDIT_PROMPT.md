# Gemini Task — Hard Audit of 478-Feature Catalog

Мета: НЕ писати Android-додаток. Довести існуючий 478-feature catalog до стану, коли кожен запис реально придатний для реалізації.

Поточний стан:
- research/features/FEATURE_CATALOG.json містить 478 feature;
- handoff/FEATURE_IMPLEMENTATION_INDEX.json містить ті ж записи;
- FULL_FEATURE_MATRIX.md заявляє, що всі 478 verified;
- але research/features/flows/ наразі має лише один детальний flow (EPB);
- частина vehicle/platform metadata виглядає узагальненою і може бути inferred, а не extracted.

## 1. Перевір КОЖЕН із 478 записів

Для кожної feature обов'язково встановити:

- чи це реально окрема функція Carista, а не дубль/alias/category;
- точний source artifact;
- exact asset/config record, якщо є;
- exact DEX class/method, якщо є;
- exact native function/address/XREF, якщо є;
- ECU;
- applicability;
- read path;
- write path;
- value mapping;
- validation;
- prerequisites;
- post-check;
- error handling;
- confidence.

Якщо немає достатнього evidence — ЗНИЗИТИ статус до LIKELY/HYPOTHESIS/UNKNOWN.

Заборонено масово ставити VERIFIED лише тому, що назву знайдено у strings/assets.

## 2. Прибери фальшиву "100% verified" картину

Перегенеруй:
- handoff/FULL_FEATURE_MATRIX.md
- handoff/FEATURE_IMPLEMENTATION_INDEX.json
- research/features/FEATURE_CATALOG.json

Додай summary:
- total_features
- verified
- corroborated
- likely
- hypothesis
- unknown
- duplicates
- aliases
- incomplete_write_flows

## 3. Source provenance для кожної feature

Кожен запис повинен мати:

```json
"evidence": [
  {
    "type": "ASSET|DEX|NATIVE|LOG|STANDARD",
    "source": "...",
    "location": "...",
    "claim_supported": "...",
    "strength": "DIRECT|INDIRECT"
  }
]
```

Якщо evidence=[] — feature не може бути VERIFIED.

## 4. Детальні flows

Створи окремий flow JSON для:
- усіх write/customization feature;
- усіх service routines;
- coding/adaptation/basic-settings;
- battery registration;
- service reset;
- TPMS operations;
- DPF operations;
- EPB;
- будь-яких actuator/test operations.

Для чисто read-only однотипних features дозволяється shared flow template + per-feature parameters.

Кожен write flow:
detect_support
-> select ECU
-> identify ECU
-> enter required session
-> security if needed
-> read current value
-> validate bounds
-> backup
-> write/routine
-> verify response
-> read-back
-> success/rollback/error.

## 5. Реально розбери *.iap / Realm

Не задовольняйся описом "34 Realm bundles".

Потрібно:
- визначити schema;
- витягнути класи/таблиці/records;
- встановити, які записи відповідають settings/features;
- зберегти parser/extractor у tools/;
- створити machine-readable export у research/assets_export/;
- прив'язати feature IDs до конкретних asset records.

Якщо контейнер encrypted/custom:
- знайти локальний код читання/декодування;
- документувати формат;
- реалізувати локальний parser якщо можливо;
- не обходити серверну авторизацію/платну систему.

## 6. Vehicle / ECU applicability

Не використовуй загальні списки моделей/років із загальних знань як VERIFIED.

Для кожного:
- model;
- year;
- engine;
- ECU;
- part number;
- SW/HW;
- ASAM;

вказати source.

Якщо модель/рік не витягнуті з Carista assets/code — позначити INFERRED або UNKNOWN.

Перегенеруй:
- research/db/vehicles.json
- research/db/ecu_variants.json
- research/features/applicability_rules.json

з provenance на кожному record.

## 7. Automatic validators

Створи tests/catalog_validation.py, який перевіряє:

- VERIFIED => evidence.length > 0;
- write feature => write/routine path present;
- service routine => prerequisites + success condition present;
- feature ID unique;
- no duplicate aliases counted as separate feature без alias_of;
- CAN/TP2 arithmetic consistent;
- every referenced source path exists;
- every flow references existing feature;
- every feature marked implementable has enough fields.

Запусти validator.

## 8. Дублі та aliases

Визнач:
- duplicate features;
- same operation with different labels;
- same feature on different ECU/platform variants;
- category headers accidentally counted as features.

Додай:
- canonical_feature_id
- alias_of
- variant_of

Не завищуй total feature count.

## 9. Implementation readiness

Для кожної feature додай:

```json
"implementation_readiness": {
  "read_ready": true/false,
  "write_ready": true/false,
  "applicability_ready": true/false,
  "parser_ready": true/false,
  "safe_to_implement_without_more_re": true/false
}
```

## 10. Результат

Створи:
- research/FEATURE_AUDIT.md
- research/feature_audit_errors.json
- research/assets_export/
- tests/catalog_validation.py
- handoff/READY_FEATURES.json
- handoff/BLOCKED_FEATURES.json

READY_FEATURES.json — тільки ті функції, які реально можна реалізувати без нового реверсу.

BLOCKED_FEATURES.json — що саме бракує для кожної іншої.

Після завершення:
1. validate JSON;
2. run catalog_validation.py;
3. покажи кількість READY/BLOCKED;
4. git diff;
5. commit;
6. push.

Не пиши план замість роботи. Виконуй.
