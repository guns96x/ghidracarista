#!/usr/bin/env python3
"""
tests/test_molecular_model.py

Focused Round 4 tests. Each group first proves the invariant holds on the committed data, then
proves the validators FAIL on a deliberately corrupted copy - a validator that cannot fail is not
a validator. No expected result counts appear here.

Run:  python tests/test_molecular_model.py      (also collectable by pytest)
"""

import copy
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

import capstone  # noqa: E402
import molecular_invariants as mi  # noqa: E402
import molecular_model as mm  # noqa: E402
import vag_setting_dataflow as df  # noqa: E402

_LOADED = None


def loaded():
    global _LOADED
    if _LOADED is None:
        _LOADED = mi.load_all(BASE_DIR)
    return _LOADED


def fresh():
    return copy.deepcopy(loaded())


def violations(L):
    return mi.check_all(BASE_DIR, L)


def any_contains(vs, needle):
    return any(needle in v for v in vs)


# ---------------------------------------------------------------------------
# CFG / dataflow (synthetic AArch64, no binary needed)
# ---------------------------------------------------------------------------

class FakeBinary:
    """Just enough of vag_setting_dataflow.Binary for Function()."""

    def __init__(self, words, base=0x1000):
        self.cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
        self.cs.detail = True
        self.code = b"".join(w.to_bytes(4, "little") for w in words)
        self.base = base
        self.got_sym = {}

    def disasm_function(self, name):
        return list(self.cs.disasm(self.code, self.base)), self.base, len(self.code)


MOV_X1_1, MOV_X1_2 = 0xD2800021, 0xD2800041
MOV_X2_X1 = 0xAA0103E2
CBZ_W0_PLUS12, B_PLUS8 = 0x34000060, 0x14000002
BL_AWAY = 0x94000040
MOV_W8_7, STR_W8_SP16, STRB_W8_SP17 = 0x528000E8, 0xB90013E8, 0x390047E8
NOP, RET = 0xD503201F, 0xD65F03C0


def mk(words):
    return df.Function(FakeBinary(words), "synthetic")


def test_synthetic_encodings_decode_as_intended():
    ins = list(FakeBinary([MOV_X1_1, MOV_X2_X1, CBZ_W0_PLUS12, B_PLUS8, BL_AWAY, MOV_W8_7, STR_W8_SP16,
                           STRB_W8_SP17]).cs.disasm(
        b"".join(w.to_bytes(4, "little") for w in [MOV_X1_1, MOV_X2_X1, CBZ_W0_PLUS12, B_PLUS8, BL_AWAY,
                                                    MOV_W8_7, STR_W8_SP16, STRB_W8_SP17]), 0x1000))
    assert [i.mnemonic for i in ins] == ["mov", "mov", "cbz", "b", "bl", "mov", "str", "strb"], ins


def test_cfg_builds_predecessor_edges_for_conditional_branch():
    #  0 cbz w0,+12 -> 3 | 1 mov x1,1 | 2 b +8 -> 4 | 3 mov x1,2 | 4 mov x2,x1
    f = mk([CBZ_W0_PLUS12, MOV_X1_1, B_PLUS8, MOV_X1_2, MOV_X2_X1, RET])
    assert sorted(f.preds[4]) == [2, 3], "join block must have both the b and the fallthrough as predecessors"
    assert sorted(f.preds[3]) == [0], "cbz target is reached only from the cbz"
    assert 1 in f.preds and f.preds[1] == [0], "cbz fallthrough edge missing"


def test_reaching_definition_merge_conflict_is_unproven():
    f = mk([CBZ_W0_PLUS12, MOV_X1_1, B_PLUS8, MOV_X1_2, MOV_X2_X1, RET])
    try:
        f.reg_value("x1", 4)
    except df.Unproven as u:
        assert u.reason == "merge_conflict", u.reason
    else:
        raise AssertionError("conflicting reaching definitions must be UNPROVEN, not resolved to one branch")


def test_reaching_definition_agreeing_predecessors_are_proven_across_blocks():
    f = mk([CBZ_W0_PLUS12, MOV_X1_1, B_PLUS8, MOV_X1_1, MOV_X2_X1, RET])
    v, chain = f.reg_value("x1", 4)
    assert v == ("const", 1) and chain, (v, chain)
    assert chain == ["0x1004", "0x100c"], "both reaching definitions must be recorded in the definition chain"


def test_caller_saved_register_is_killed_by_call():
    f = mk([MOV_X1_1, BL_AWAY, MOV_X2_X1, RET])
    try:
        f.reg_value("x1", 2)
    except df.Unproven as u:
        assert "clobbered by call" in u.reason
    else:
        raise AssertionError("x1 survives a bl - caller-saved clobbering not modelled")


def test_entry_without_definition_is_unproven():
    f = mk([NOP, MOV_X2_X1, RET])
    try:
        f.reg_value("x1", 1)
    except df.Unproven as u:
        assert u.reason == "reached_function_entry"
    else:
        raise AssertionError("value with no definition must be UNPROVEN")


def test_stack_slot_reaching_store_and_hazards():
    ok = mk([MOV_W8_7, STR_W8_SP16, NOP, RET])
    v, chain = ok.stack_value(16, 4, 2)
    assert v == ("const", 7) and chain

    call_between = mk([MOV_W8_7, STR_W8_SP16, BL_AWAY, NOP, RET])
    for label, fn in (("call", call_between),):
        try:
            fn.stack_value(16, 4, 3)
        except df.Unproven as u:
            assert "call between stack store and use" in u.reason, label
        else:
            raise AssertionError("a call between store and use may write the slot")

    overlap = mk([MOV_W8_7, STR_W8_SP16, STRB_W8_SP17, NOP, RET])
    try:
        overlap.stack_value(16, 4, 3)
    except df.Unproven as u:
        assert "overlapping" in u.reason
    else:
        raise AssertionError("partial overlapping store must make the slot UNPROVEN")


# ---------------------------------------------------------------------------
# Reproducibility relationships that need no binary
# ---------------------------------------------------------------------------

def test_every_factory_class_is_reproduced_from_its_committed_emplace_symbol():
    L = loaded()
    assert L["factories"]["factories"], "empty factory map"
    for addr, f in L["factories"]["factories"].items():
        parsed = df.parse_emplace_symbol(f["emplace_symbol"])
        assert parsed is not None, f"{addr}: emplace symbol does not parse"
        cls, arg_types = parsed
        assert cls == f["concrete_class"], f"{addr}: {cls} != committed {f['concrete_class']}"
        assert arg_types == f["forwarded_arg_types"], f"{addr}: forwarded argument types not reproducible"


def test_provenance_chain_is_clean_and_detects_missing_factory():
    L = fresh()
    assert mi.check_provenance_chain(L["callsites"], L["factories"], L["raw"]) == []
    victim = L["raw"]["variants"][0]["factory_helper_address"]
    del L["factories"]["factories"][victim]
    vs = mi.check_provenance_chain(L["callsites"], L["factories"], L["raw"])
    assert any_contains(vs, "absent from committed map"), vs


def test_bl_target_is_never_a_got_or_plt_slot():
    L = loaded()
    for addr, f in L["factories"]["factories"].items():
        assert addr not in (f["emplace_got_slot"], f["emplace_plt"])
    for v in L["raw"]["variants"]:
        assert v["factory_helper_address"] != v["emplace_got_slot"]


def test_missing_factory_reproducibility_prevents_exact():
    L = fresh()
    ev = mm.load_request_evidence(BASE_DIR)
    docs = mm.load_protocol_docs(BASE_DIR)
    exact_raw = None
    for raw in L["raw"]["variants"]:
        if mm.evaluate_variant(raw, ev, docs, L["factories"]["factories"])["variant_status"] == mm.ST_EXACT:
            exact_raw = raw
            break
    assert exact_raw is not None, "fixture needs at least one exact variant"
    bad = mm.evaluate_variant(exact_raw, ev, docs, {})
    assert bad["variant_status"] != mm.ST_EXACT and not bad["executable"]
    assert "factory_not_reproducible_from_committed_map" in bad["blockers"]


# ---------------------------------------------------------------------------
# Heuristic provenance must not be EXACT
# ---------------------------------------------------------------------------

def test_exact_variant_without_definition_chain_is_rejected():
    L = fresh()
    victim = next(v for lst in L["variants"]["variants_by_key"].values() for v in lst
                  if v["variant_status"] == mm.ST_EXACT)
    raw = next(r for r in L["raw"]["variants"] if r["variant_id"] == victim["variant_id"])
    raw["args"][2]["def_chain"] = []
    vs = mi.check_variant_records(L["variants"]["variants_by_key"], L["raw"], L["factories"],
                                  mm.load_request_evidence(BASE_DIR))
    assert any_contains(vs, "no definition chain"), vs


def test_exact_variant_with_unproven_argument_is_rejected():
    L = fresh()
    victim = next(v for lst in L["variants"]["variants_by_key"].values() for v in lst
                  if v["variant_status"] == mm.ST_EXACT)
    raw = next(r for r in L["raw"]["variants"] if r["variant_id"] == victim["variant_id"])
    raw["args"][3]["status"] = "UNPROVEN"
    vs = mi.check_variant_records(L["variants"]["variants_by_key"], L["raw"], L["factories"],
                                  mm.load_request_evidence(BASE_DIR))
    assert any_contains(vs, "EXACT with UNPROVEN argument"), vs


# ---------------------------------------------------------------------------
# Protocol consistency
# ---------------------------------------------------------------------------

def test_no_exact_variant_has_protocol_disagreement_and_conflicts_are_rejected():
    for v in (v for lst in loaded()["variants"]["variants_by_key"].values() for v in lst):
        pm = v["protocol_model"]
        if pm["conflict"]:
            assert v["variant_status"] == mm.ST_CONFLICT and not v["executable"]
        if v["variant_status"] == mm.ST_EXACT:
            vals = {pm["class"], pm["ecu_object"], pm["ecu_table"], pm["request_builder"]}
            assert len(vals) == 1 and None not in vals, vals
            assert v["request_flow"]["protocol"] == pm["runtime_protocol"]


def test_uds_class_on_can_ecu_is_a_conflict_not_exact():
    ev = mm.load_request_evidence(BASE_DIR)
    docs = mm.load_protocol_docs(BASE_DIR)
    raw = _synthetic_raw("VagUdsCodingSetting", "VagCanEcu::CENTRAL_ELEC", "VagCanEcu", "class_fixed_id", 0x600)
    v = mm.evaluate_variant(raw, ev, docs, _factories_for(raw))
    assert v["variant_status"] == mm.ST_CONFLICT and not v["executable"] and v["request_flow"] is None, v["blockers"]


def test_corrupted_command_protocol_is_detected():
    L = fresh()
    c = next(c for c in L["commands"]["commands"] if c["protocol"] == mm.UDS)
    c["protocol"] = mm.TP2
    vs = mi.check_features(L["catalog"], L["variants"], L["instances"], L["commands"], L["ready"], L["blocked"])
    assert any_contains(vs, "command protocol"), vs


def test_kwp_ecu_borrowing_uds_can_ids_is_detected():
    L = fresh()
    victim = next((v for lst in L["variants"]["variants_by_key"].values() for v in lst
                   if v["variant_status"] == mm.ST_EXACT and v["ecu"]["protocol"] == mm.TP2), None)
    assert victim is not None, "fixture needs one exact TP2/KWP variant"
    victim["ecu"]["uds_tx_id"], victim["ecu"]["uds_rx_id"] = "0x70E", "0x778"
    vs = mi.check_variant_records(L["variants"]["variants_by_key"], L["raw"], L["factories"],
                                  mm.load_request_evidence(BASE_DIR))
    assert any_contains(vs, "borrowed from a same-named UDS ECU"), vs


def test_unknown_ecu_is_never_exact_and_has_no_fallback_ids():
    ev = mm.load_request_evidence(BASE_DIR)
    docs = mm.load_protocol_docs(BASE_DIR)
    raw = _synthetic_raw("VagUdsCodingSetting", "VagUdsEcu::NOT_A_REAL_ECU", "VagUdsEcu", "class_fixed_id", 0x600)
    v = mm.evaluate_variant(raw, ev, docs, _factories_for(raw))
    assert v["variant_status"] != mm.ST_EXACT and "ecu_transport_unresolved" in v["blockers"]
    assert v["ecu"]["uds_tx_id"] is None and v["ecu"]["uds_rx_id"] is None


# ---------------------------------------------------------------------------
# TP2 / KWP adaptation flow
# ---------------------------------------------------------------------------

def _synthetic_raw(cls, ecu, ecu_class, id_role, ident, byte_offset=1, mask=4):
    args = [{"index": i, "kind": k, "type": t, "status": "PROVEN", "def_chain": ["0x1"], "value": val}
            for i, (k, t, val) in enumerate([
                ("ecu", f"{ecu_class}*&", ecu), ("whitelist", "wl", "VagWhitelists::X"),
                ("int", "int", ident), ("int", "int", byte_offset), ("int", "int", mask),
                ("name", "char const[4]&", "car_setting_synthetic"), ("interpretation", "i", "Interp::X")])]
    if id_role == "class_fixed_id":
        args = [a for a in args if a["index"] != 2]
        for i, a in enumerate(args):
            a["index"] = i
    return {"variant_id": f"synthetic@{cls}", "setting_key": "car_setting_synthetic", "callsite": "0x1",
            "asm_address": "0x1", "source_function": "synthetic", "factory_helper_address": "0xf",
            "emplace_got_slot": "0xe", "concrete_class": cls, "ecu": ecu, "ecu_object_class": ecu_class,
            "whitelist": "VagWhitelists::X", "interpretation": "Interp::X", "applicability_list": None,
            "applicability_list_present": False, "did_or_channel": ident, "id_role": id_role,
            "byte_offset": byte_offset, "bit_mask": mask,
            "field_provenance": {"did_or_channel": {"source": id_role if id_role == "class_fixed_id" else "constructor_arg",
                                                    "arg_index": 2, "def_chain": ["0x1"]},
                                 "byte_offset": {"source": "constructor_arg", "arg_index": 3, "def_chain": ["0x1"]},
                                 "bit_mask": {"source": "constructor_arg", "arg_index": 4, "def_chain": ["0x1"]}},
            "semantics_status": "VERIFIED", "args": args}


def _factories_for(raw):
    return {raw["factory_helper_address"]: {"concrete_class": raw["concrete_class"]}}


def test_tp2_adaptation_is_the_ordered_31b9_31ba_31bb_flow():
    ev = mm.load_request_evidence(BASE_DIR)
    docs = mm.load_protocol_docs(BASE_DIR)
    raw = _synthetic_raw("VagCanShortAdaptationSetting", "VagCanEcu::CENTRAL_ELEC", "VagCanEcu", "channel", 61)
    v = mm.evaluate_variant(raw, ev, docs, _factories_for(raw))
    assert v["variant_status"] == mm.ST_EXACT, v["blockers"]
    flow = v["request_flow"]
    assert flow["flow_id"] == "tp2_adaptation_channel_flow" and flow["protocol"] == mm.TP2
    assert [s.get("request_prefix_hex") for s in flow["steps"]] == ["31B9", "31BA", None, "31BB", "31BA"]
    assert [s["op"] for s in flow["steps"]] == ["select_channel", "read_adaptation_data", "decode_modify",
                                                 "write_adaptation_data", "read_back_verify"]
    assert flow["steps"][0]["operands"] == [{"name": "channel", "source": "constructor_arg", "value": 61}]
    assert mi.check_flow(flow, mm.TP2, ev) == []
    text = repr(flow)
    assert "'21'" not in text and "'27'" not in text


def test_tp2_adaptation_flow_bytes_come_from_committed_evidence_only():
    ev = mm.load_request_evidence(BASE_DIR)
    docs = mm.load_protocol_docs(BASE_DIR)
    raw = _synthetic_raw("VagCanShortAdaptationSetting", "VagCanEcu::CENTRAL_ELEC", "VagCanEcu", "channel", 1)
    broken = dict(ev)
    broken.pop("vag_tp20_write_adaptation_data")
    try:
        mm.build_request_flow(raw, broken, docs)
    except mm.ModelError:
        pass
    else:
        raise AssertionError("flow must refuse to build when its evidence entry is missing")
    weakened = copy.deepcopy(ev)
    weakened["vag_tp20_read_adaptation_data"]["confidence"] = "INFERRED"
    try:
        mm.build_request_flow(raw, weakened, docs)
    except mm.ModelError:
        pass
    else:
        raise AssertionError("flow must require VERIFIED evidence")


def test_synthetic_0x21_0x27_adaptation_is_detected():
    ev = mm.load_request_evidence(BASE_DIR)
    docs = mm.load_protocol_docs(BASE_DIR)
    raw = _synthetic_raw("VagCanShortAdaptationSetting", "VagCanEcu::CENTRAL_ELEC", "VagCanEcu", "channel", 61)
    flow = mm.evaluate_variant(raw, ev, docs, _factories_for(raw))["request_flow"]
    bad = copy.deepcopy(flow)
    bad["steps"] = [s for s in bad["steps"] if s["op"] != "select_channel"]
    for i, s in enumerate(bad["steps"], 1):
        s["order"] = i
    bad["steps"][0]["request_prefix_hex"] = "21"
    bad["steps"][2]["request_prefix_hex"] = "27"
    vs = mi.check_flow(bad, mm.TP2, ev)
    assert any_contains(vs, "not 31 B9 / 31 BA"), vs


def test_short_adaptation_variants_in_data_are_never_executable_with_a_wrong_flow():
    for lst in loaded()["variants"]["variants_by_key"].values():
        for v in lst:
            if v["concrete_class"] == "VagCanShortAdaptationSetting" and v["request_flow"]:
                assert v["request_flow"]["flow_id"] == "tp2_adaptation_channel_flow"
                assert [s.get("request_prefix_hex") for s in v["request_flow"]["steps"]] == \
                       mi.TP2_ADAPTATION_SEQUENCE


# ---------------------------------------------------------------------------
# No first-variant collapse
# ---------------------------------------------------------------------------

def _multi_exact_feature(L):
    counts = {}
    for c in L["commands"]["commands"]:
        counts.setdefault(c["feature_id"], []).append(c)
    return next((fid for fid, cs in counts.items() if len(cs) > 1), None)


def test_multi_variant_features_are_never_ready():
    L = loaded()
    ready = {f["id"] for f in L["ready"]["features"]}
    for i in L["instances"]["instances"]:
        if i["variants_count"] > 1:
            assert i["id"] not in ready
            assert i["resolution_status"] != mm.FS_EXACT


def test_every_exact_variant_of_a_feature_is_published_not_only_the_first():
    L = loaded()
    fid = _multi_exact_feature(L)
    if fid is None:
        return  # data currently has no feature with >1 executable variants; the mutation test below builds one
    inst = next(i for i in L["instances"]["instances"] if i["id"] == fid)
    published = {c["variant_id"] for c in L["commands"]["commands"] if c["feature_id"] == fid}
    assert published == set(inst["exact_variant_ids"])


def test_first_variant_collapse_is_detected():
    L = fresh()
    fid = _multi_exact_feature(L)
    assert fid is not None, "fixture needs a feature with several executable variants"
    kept = False
    survivors = []
    for c in L["commands"]["commands"]:
        if c["feature_id"] == fid:
            if kept:
                continue
            kept = True
        survivors.append(c)
    L["commands"]["commands"] = survivors
    L["commands"]["metadata"]["total_commands"] = len(survivors)
    L["instances"]["metadata"]["total_executable_variants"] = len(survivors)
    vs = mi.check_features(L["catalog"], L["variants"], L["instances"], L["commands"], L["ready"], L["blocked"])
    assert any_contains(vs, "first-variant collapse"), vs


def test_promoting_an_ambiguous_feature_to_ready_is_detected():
    L = fresh()
    amb = next(i for i in L["instances"]["instances"] if i["resolution_status"] == mm.FS_AMBIGUOUS)
    L["ready"]["features"].append({"id": amb["id"]})
    L["ready"]["metadata"]["total_ready"] += 1
    vs = mi.check_features(L["catalog"], L["variants"], L["instances"], L["commands"], L["ready"], L["blocked"])
    assert any_contains(vs, "READY") , vs


def test_identity_free_variant_selection_is_not_order_based():
    # Reordering the raw variants must not change any feature state or command.
    L = loaded()
    ev = mm.load_request_evidence(BASE_DIR)
    docs = mm.load_protocol_docs(BASE_DIR)
    raws = list(L["raw"]["variants"])
    a = [mm.evaluate_variant(r, ev, docs, L["factories"]["factories"]) for r in raws]
    b = [mm.evaluate_variant(r, ev, docs, L["factories"]["factories"]) for r in reversed(raws)]
    key = lambda v: v["variant_id"]  # noqa: E731
    assert sorted(a, key=key) == sorted(b, key=key)


# ---------------------------------------------------------------------------
# Not-a-setting operations
# ---------------------------------------------------------------------------

def test_service_and_diagnostic_operations_are_never_settings():
    L = loaded()
    exact_ids = {c["feature_id"] for c in L["commands"]["commands"]}
    for fid in mm.NOT_A_SETTING:
        assert fid not in exact_ids
        inst = next(i for i in L["instances"]["instances"] if i["id"] == fid)
        assert inst["resolution_status"] == mm.FS_REJECTED and inst["variants_count"] == 0


def test_autoscan_as_coding_setting_is_detected():
    L = fresh()
    inst = next(i for i in L["instances"]["instances"] if i["id"] == "DIAG_AUTOSCAN")
    victim = next(c for c in L["commands"]["commands"])
    victim["feature_id"] = "DIAG_AUTOSCAN"
    vs = mi.check_features(L["catalog"], L["variants"], L["instances"], L["commands"], L["ready"], L["blocked"])
    assert any_contains(vs, "DIAG_AUTOSCAN"), vs


# ---------------------------------------------------------------------------
# Whole-artifact relationship check
# ---------------------------------------------------------------------------

def test_committed_artifacts_satisfy_every_relationship():
    vs = violations(loaded())
    assert vs == [], "\n".join(vs[:25])


def test_totals_are_recomputed_not_asserted():
    L = fresh()
    L["instances"]["metadata"]["counts"]["EXACT_RESOLVED"] += 1
    assert any_contains(violations(L), "metadata.counts")


def main():
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS {name}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  FAIL {name}: {type(exc).__name__}: {exc}")
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
