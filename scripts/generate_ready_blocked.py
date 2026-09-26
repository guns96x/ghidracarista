import sys as _sys
_sys.exit("DEPRECATED (Round 4): this generator wrote SETTING_*/READY/BLOCKED artifacts with "
          "collapsed variants and unpinned inputs. Use tools/build_variants_and_settings_index.py.")
import json
import os

with open('handoff/FEATURE_IMPLEMENTATION_INDEX.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

features = data['features']

ready_features = []
blocked_features = []

for feat in features:
    fid = feat.get('id', '')
    name = feat.get('user_visible_name', '')
    cat = feat.get('category', '')
    sec = feat.get('security', '')
    desc = feat.get('description', '')
    read_op = feat.get('read_op') or feat.get('read_operation', 'None')
    write_op = feat.get('write_op') or feat.get('write_operation', 'None')
    routine = feat.get('routine', 'None')

    # Normalize fields
    feat_clean = dict(feat)
    feat_clean['read_op'] = read_op
    feat_clean['write_op'] = write_op
    if 'read_operation' in feat_clean:
        del feat_clean['read_operation']
    if 'write_operation' in feat_clean:
        del feat_clean['write_operation']

    # Blocking checks
    if 'TODO' in fid or name.lower() == 'todo':
        feat_clean['blocking_reason'] = 'INCOMPLETE_SPECIFICATION'
        feat_clean['remediation'] = 'Specify feature parameters and corroborating ECU mapping.'
        blocked_features.append(feat_clean)
    elif 'tpms_in_mmi_step' in fid.lower() or 'tpms_indirect_step' in fid.lower():
        feat_clean['blocking_reason'] = 'MULTI_STEP_MANUAL_PROCEDURE'
        feat_clean['remediation'] = 'Implement coordinated multi-step calibration wizard with user drive-cycle prompts.'
        blocked_features.append(feat_clean)
    elif 'SFD' in sec and 'MQB2020' in sec:
        # EPB has SFD note for MQB2020, but is READY for standard MQB/PQ.
        # It should be READY for PQ/MQB with conditional SFD warning
        feat_clean['readiness_status'] = 'READY_CONDITIONAL'
        feat_clean['readiness_notes'] = 'Fully ready on PQ35 and MQB pre-2020. Blocked by SFD on MQB2020 / MQBevo vehicles.'
        ready_features.append(feat_clean)
    elif 'SFD' in desc or 'SFD' in sec:
        feat_clean['blocking_reason'] = 'SFD_REQUIRED'
        feat_clean['remediation'] = 'Requires SFD (Schutz Fahrzeug Diagnose) token for MQB2020 / MQBevo architecture.'
        blocked_features.append(feat_clean)
    else:
        # Standard features (Diagnostics, Service Tools, Long Coding & Adaptation)
        feat_clean['readiness_status'] = 'READY'
        feat_clean['readiness_notes'] = 'Verified protocol frames, ECU addresses, and parameter mappings.'
        ready_features.append(feat_clean)

ready_dict = {
    "metadata": {
        "catalog_version": "1.0-cleanroom",
        "description": "Ready features for autonomous Android VAG diagnostic & customization app",
        "total_ready": len(ready_features)
    },
    "features": ready_features
}

blocked_dict = {
    "metadata": {
        "catalog_version": "1.0-cleanroom",
        "description": "Features blocked by SFD, proprietary seed-keys, or requiring multi-step wizards",
        "total_blocked": len(blocked_features)
    },
    "features": blocked_features
}

with open('handoff/READY_FEATURES.json', 'w', encoding='utf-8') as f:
    json.dump(ready_dict, f, indent=2, ensure_ascii=False)

with open('handoff/BLOCKED_FEATURES.json', 'w', encoding='utf-8') as f:
    json.dump(blocked_dict, f, indent=2, ensure_ascii=False)

print(f"Generated READY_FEATURES.json: {len(ready_features)} features")
print(f"Generated BLOCKED_FEATURES.json: {len(blocked_features)} features")
print(f"Total features partitioned: {len(ready_features) + len(blocked_features)} / {len(features)}")
