import json

with open('handoff/FEATURE_IMPLEMENTATION_INDEX.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

todos = []
for feat in data['features']:
    fid = feat['id']
    name = feat.get('user_visible_name', '')
    desc = feat.get('description', '')
    if 'todo' in fid.lower() or 'todo' in name.lower() or 'todo' in desc.lower():
        todos.append((fid, name))

print(f"Features with TODO: {len(todos)}")
for t in todos[:10]:
    print(t)
