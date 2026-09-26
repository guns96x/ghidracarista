#!/usr/bin/env python3
"""
tests/molecular_reproducibility.py

Proves the committed molecular artifacts can be regenerated from committed code + the pinned
binary (MOLECULAR_AUDIT_ROUND4.md section 1). Steps:

  1. the binary's SHA-256 equals the pin recorded in the committed callsite artifact;
  2. tools/vag_setting_dataflow.py is run TWICE in-memory: both runs must be identical to each
     other and byte-for-byte identical to the committed vag_setting_callsites.json and
     resolved_factories_map.json;
  3. tools/extract_all_variants_ground_truth.py logic, fed with the FRESH extraction, must equal
     the committed all_binary_variants_ground_truth.json;
  4. tools/build_variants_and_settings_index.py logic must equal each committed downstream file
     (variants index, instance index, command map, READY, BLOCKED);
  5. research/molecular/REPRODUCIBILITY_REPORT.json must match the recomputed pins and hashes.

If the binary is absent (extracted/ is git-ignored) steps 1-2 cannot run: the script says so and
exits non-zero unless --allow-missing-binary is given; steps 3-5 still run from committed inputs.

  python tests/molecular_reproducibility.py                # verify
  python tests/molecular_reproducibility.py --write-report # regenerate the report, then verify
"""

import hashlib
import json
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

REPORT_REL = os.path.join("research", "molecular", "REPRODUCIBILITY_REPORT.json")
BINARY_REL = os.path.join("extracted", "arm64", "lib", "arm64-v8a", "libCarista.so")
MOL = os.path.join("research", "molecular")

GENERATION_COMMANDS = [
    "python tools/vag_setting_dataflow.py",
    "python tools/extract_all_variants_ground_truth.py",
    "python tools/build_variants_and_settings_index.py",
    "python tools/generate_feature_dependency_graph.py",
    "python tests/molecular_reproducibility.py --write-report",
    "python tests/molecular_validation.py",
    "python tests/test_molecular_model.py",
]

GENERATED = [
    os.path.join(MOL, "vag_setting_callsites.json"),
    os.path.join(MOL, "resolved_factories_map.json"),
    os.path.join(MOL, "all_binary_variants_ground_truth.json"),
    os.path.join(MOL, "SETTING_VARIANTS_INDEX.json"),
    os.path.join(MOL, "SETTING_INSTANCE_INDEX.json"),
    os.path.join(MOL, "SETTING_TO_COMMAND_MAP.json"),
    os.path.join("handoff", "READY_FEATURES.json"),
    os.path.join("handoff", "BLOCKED_FEATURES.json"),
    os.path.join(MOL, "FEATURE_DEPENDENCY_GRAPH.json"),
    os.path.join(MOL, "FEATURE_DEPENDENCY_GRAPH.md"),
]

INPUTS = [
    os.path.join("research", "db", "diagnostic_evidence.json"),
    os.path.join("research", "features", "FEATURE_CATALOG.json"),
    os.path.join("research", "protocols", "uds.md"),
    os.path.join("research", "protocols", "coding.md"),
    os.path.join("research", "protocols", "adaptation.md"),
    os.path.join("tools", "vag_setting_dataflow.py"),
    os.path.join("tools", "vag_class_semantics.py"),
    os.path.join("tools", "extract_all_variants_ground_truth.py"),
    os.path.join("tools", "build_variants_and_settings_index.py"),
    os.path.join("tools", "molecular_model.py"),
    os.path.join("tools", "generate_feature_dependency_graph.py"),
    os.path.join("tools", "vag_ecu_addressing.py"),
]


def read_text(rel):
    with open(os.path.join(BASE_DIR, rel), encoding="utf-8", newline="") as fh:
        return fh.read().replace("\r\n", "\n")  # checkout-independent


def sha_text(rel):
    return hashlib.sha256(read_text(rel).encode("utf-8")).hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class Result:
    def __init__(self):
        self.failures = []
        self.notes = []

    def check(self, ok, msg):
        print(("  PASS " if ok else "  FAIL ") + msg)
        if not ok:
            self.failures.append(msg)
        return ok


def build_report(binary_sha, binary_rerun):
    return {
        "binary": {"path": BINARY_REL.replace("\\", "/"), "sha256": binary_sha},
        "extractor_version": json.loads(read_text(GENERATED[0]))["metadata"]["extractor_version"],
        "generation_commands": GENERATION_COMMANDS,
        "rerun_identical_to_committed": binary_rerun,
        "inputs_sha256": {p.replace("\\", "/"): sha_text(p) for p in INPUTS},
        "generated_sha256": {p.replace("\\", "/"): sha_text(p) for p in GENERATED},
        "note": "Hashes are over LF-normalised text. rerun_identical_to_committed records the outcome of "
                "the last run that had the binary available (null when it was not).",
    }


def main():
    write_report = "--write-report" in sys.argv
    allow_missing = "--allow-missing-binary" in sys.argv
    r = Result()

    import extract_all_variants_ground_truth as raw_mod
    import build_variants_and_settings_index as idx_mod

    committed = {rel: read_text(rel) for rel in GENERATED}
    pinned = json.loads(committed[GENERATED[0]])["metadata"]["binary_sha256"]
    binary_path = os.path.join(BASE_DIR, BINARY_REL)
    binary_sha = None
    rerun_ok = None
    fresh_callsites = fresh_factories = None

    print("[*] Step 1-2: binary pin and dataflow re-extraction")
    if os.path.exists(binary_path):
        import vag_setting_dataflow as df
        binary_sha = sha_file(binary_path)
        r.check(binary_sha == pinned, f"binary sha256 {binary_sha} equals committed pin")
        runs = []
        for n in (1, 2):
            data, fmap = df.extract(binary_path)
            runs.append((df.render_json(data), df.render_json(fmap)))
        r.check(runs[0] == runs[1], "two consecutive extractions are byte-identical")
        r.check(runs[0][0] == committed[GENERATED[0]], "fresh extraction == committed vag_setting_callsites.json")
        r.check(runs[0][1] == committed[GENERATED[1]], "fresh extraction == committed resolved_factories_map.json")
        rerun_ok = runs[0][0] == committed[GENERATED[0]] and runs[0][1] == committed[GENERATED[1]] \
            and runs[0] == runs[1]
        fresh_callsites, fresh_factories = json.loads(runs[0][0]), json.loads(runs[0][1])
    else:
        msg = f"binary not found at {BINARY_REL}: extraction cannot be re-run (git-ignored input)"
        print("  SKIP " + msg)
        if not allow_missing:
            r.failures.append(msg + " (use --allow-missing-binary to verify downstream steps only)")
        binary_sha = pinned

    print("[*] Step 3: raw variants regenerate from the (fresh, else committed) extraction")
    callsites = fresh_callsites or json.loads(committed[GENERATED[0]])
    factories = fresh_factories or json.loads(committed[GENERATED[1]])
    regenerated_raw = raw_mod.render_json(raw_mod.build(callsites, factories))
    r.check(regenerated_raw == committed[GENERATED[2]], "all_binary_variants_ground_truth.json regenerates exactly")

    print("[*] Step 4: downstream artifacts regenerate exactly")
    outputs = idx_mod.build(BASE_DIR)
    for rel, obj in outputs.items():
        r.check(idx_mod.render_json(obj) == committed[rel], f"{rel.replace(os.sep, '/')} regenerates exactly")

    import generate_feature_dependency_graph as gfd
    graph = gfd.build_graph(os.path.join(BASE_DIR, MOL))
    r.check(gfd.render_json(graph) == committed[GENERATED[8]],
            "research/molecular/FEATURE_DEPENDENCY_GRAPH.json regenerates exactly")
    r.check(gfd.render_markdown(graph) == committed[GENERATED[9]],
            "research/molecular/FEATURE_DEPENDENCY_GRAPH.md regenerates exactly")

    print("[*] Step 5: reproducibility report")
    report_path = os.path.join(BASE_DIR, REPORT_REL)
    if write_report:
        if rerun_ok is None and os.path.exists(report_path):
            rerun_ok = json.loads(read_text(REPORT_REL)).get("rerun_identical_to_committed")
        with open(report_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(build_report(binary_sha, rerun_ok), indent=1, sort_keys=True) + "\n")
        print(f"  wrote {REPORT_REL.replace(os.sep, '/')}")
    if os.path.exists(report_path):
        stored = json.loads(read_text(REPORT_REL))
        fresh = build_report(binary_sha, stored.get("rerun_identical_to_committed"))
        r.check(stored == fresh, "REPRODUCIBILITY_REPORT.json matches recomputed pins and hashes")
        if rerun_ok is not None:
            r.check(stored.get("rerun_identical_to_committed") == rerun_ok,
                    "report's recorded rerun result matches this run")
    else:
        r.check(False, "REPRODUCIBILITY_REPORT.json is missing (run with --write-report)")

    print("=" * 70)
    if r.failures:
        print("REPRODUCIBILITY: FAILED")
        for f in r.failures:
            print("  - " + f)
        return 1
    print("REPRODUCIBILITY: OK" + ("" if rerun_ok is not None else " (binary re-extraction SKIPPED)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
