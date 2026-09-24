import json

with open('handoff/FEATURE_IMPLEMENTATION_INDEX.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

has_op = 0
has_operation = 0
for x in data['features']:
    if 'read_op' in x or 'write_op' in x:
        has_op += 1
    if 'read_operation' in x or 'write_operation' in x:
        has_operation += 1

print(f"has_op: {has_op}, has_operation: {has_operation}, total: {len(data['features'])}")
