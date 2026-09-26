#!/usr/bin/env python3
"""
tools/vag_setting_dataflow.py

Evidence-grounded extractor for every VAG setting constructor call made by
VagCanSettings::getSettings() and VagCanSettingsBanned::getSettings() in libCarista.so.

Replaces the textual 50-instruction window of tools/extract_all_variants_ground_truth.py
(MOLECULAR_AUDIT_ROUND4.md sections 1 and 5).

Pipeline
--------
1. Function bounds come from .dynsym st_value/st_size (no hard-coded sizes).
2. Every `bl` target in those functions is resolved to a factory *helper*. A helper is
   accepted only if it forwards its argument registers unchanged to a PLT call of
   std::__shared_ptr_emplace<Class,...>::__shared_ptr_emplace<Args...>(). The class and the
   exact forwarded argument types are parsed from that mangled PLT symbol. The BL target
   (helper) and the PLT/GOT slot are stored as separate fields.
3. Arguments are recovered with a CFG reaching-definition analysis:
   - basic blocks and predecessor edges are built for the whole function;
   - a value is walked backwards through its block, then through *all* predecessors; if
     predecessors disagree the value is UNPROVEN (merge_conflict);
   - bl/blr kill caller-saved registers x0-x18 and x30;
   - any instruction that writes the register and is not modelled makes it UNPROVEN;
   - stack temporaries (by-reference int arguments) are resolved to the unique reaching
     store of exactly that slot; a call between the store and the use, an overlapping store
     of a different width, or a store through an unresolved base makes the value UNPROVEN.
4. Semantics per class come from the VagSetting/VagCanCodingSetting base-constructor calls
   in the decompile (see CLASS_SEMANTICS), not from guesses.

Output: research/molecular/vag_setting_callsites.json and
        research/molecular/resolved_factories_map.json (the exact map used).
"""

import hashlib
import json
import os
import re
import sys
from collections import defaultdict

import capstone
from capstone import arm64_const as A
from elftools.elf.elffile import ELFFile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_SO = os.path.join(BASE_DIR, "extracted", "arm64", "lib", "arm64-v8a", "libCarista.so")
OUT_CALLSITES = os.path.join(BASE_DIR, "research", "molecular", "vag_setting_callsites.json")
OUT_FACTORIES = os.path.join(BASE_DIR, "research", "molecular", "resolved_factories_map.json")

SOURCE_FUNCTIONS = [
    "_ZN14VagCanSettings11getSettingsEv",
    "_ZN20VagCanSettingsBanned11getSettingsEv",
]

EXTRACTOR_VERSION = "round4-cfg-2"

from vag_class_semantics import CLASS_SEMANTICS  # noqa: E402  (shared with the variant builder)


# ---------------------------------------------------------------------------
# Minimal Itanium demangler for the emplace argument pack
# ---------------------------------------------------------------------------

BUILTINS = {"v": "void", "b": "bool", "c": "char", "a": "signed char", "h": "unsigned char",
            "s": "short", "t": "unsigned short", "i": "int", "j": "unsigned int",
            "l": "long", "m": "unsigned long", "x": "long long", "y": "unsigned long long",
            "f": "float", "d": "double"}


class Demangler:
    """Parses the subset of the Itanium grammar used by libc++ emplace constructors."""

    def __init__(self, s):
        self.s = s
        self.i = 0
        self.subs = []

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else ""

    def number(self):
        m = re.match(r"\d+", self.s[self.i:])
        if not m:
            raise ValueError(f"number expected at {self.i}")
        self.i += len(m.group(0))
        return int(m.group(0))

    def source_name(self):
        n = self.number()
        name = self.s[self.i:self.i + n]
        self.i += n
        return name

    def substitution(self):
        # at 'S'
        self.i += 1
        c = self.peek()
        if c == "t":
            self.i += 1
            return "std"
        if c == "_":
            self.i += 1
            return self.subs[0]
        m = re.match(r"([0-9A-Z]*)_", self.s[self.i:])
        if not m:
            raise ValueError(f"bad substitution at {self.i}")
        self.i += len(m.group(0))
        seq = int(m.group(1), 36) + 1 if m.group(1) else 0
        return self.subs[seq]

    def template_args(self):
        # at 'I'
        self.i += 1
        args = []
        while self.peek() != "E":
            if self.peek() == "L":
                # literal, e.g. Li0E
                j = self.s.index("E", self.i)
                args.append(self.s[self.i + 1:j])
                self.i = j + 1
            else:
                args.append(self.type())
        self.i += 1
        return "<" + ", ".join(args) + ">"

    def nested_name(self):
        # at 'N'
        self.i += 1
        quals = ""
        while self.peek() in "KVr":
            quals += self.peek()
            self.i += 1
        parts = []
        cur = None
        while self.peek() != "E":
            c = self.peek()
            if c == "S":
                cur = self.substitution()
                parts = [cur]
                continue
            if c == "I":
                cur = "::".join(parts) + self.template_args()
                parts = [cur]
                self.subs.append(cur)
                continue
            name = self.source_name()
            if self.peek() == "B":  # abi tag
                self.i += 1
                self.source_name()
            parts.append(name)
            cur = "::".join(parts)
            parts = [cur]
            self.subs.append(cur)
        self.i += 1
        return cur

    def type(self):
        c = self.peek()
        if c in BUILTINS:
            self.i += 1
            return BUILTINS[c]
        if c == "K":
            self.i += 1
            t = self.type() + " const"
            self.subs.append(t)
            return t
        if c in "PRO":
            self.i += 1
            t = self.type() + {"P": "*", "R": "&", "O": "&&"}[c]
            self.subs.append(t)
            return t
        if c == "A":
            self.i += 1
            n = self.number()
            assert self.peek() == "_"
            self.i += 1
            t = f"{self.type()}[{n}]"
            self.subs.append(t)
            return t
        if c == "N":
            return self.nested_name()
        if c == "S":
            t = self.substitution()
            if self.peek() == "I":
                t = t + self.template_args()
                self.subs.append(t)
            return t
        if c.isdigit():
            t = self.source_name()
            self.subs.append(t)
            if self.peek() == "I":
                t = t + self.template_args()
                self.subs.append(t)
            return t
        raise ValueError(f"unsupported type code {c!r} at {self.i}")


def parse_emplace_symbol(sym):
    """Returns (class_name, [arg_type_strings]) for a libc++ __shared_ptr_emplace ctor."""
    pre = "_ZNSt6__ndk120__shared_ptr_emplaceI"
    if not sym.startswith(pre):
        return None
    d = Demangler(sym)
    # Seed substitutions exactly as the Itanium ABI would for the prefix:
    # S_ = std::__ndk1, S0_ = std::__ndk1::__shared_ptr_emplace
    d.subs = ["std::__ndk1", "std::__ndk1::__shared_ptr_emplace"]
    d.i = len(pre)
    cls = d.type()
    d.subs.append(cls)  # seq continues naturally inside type()
    alloc = d.type()
    assert d.peek() == "E", "end of class template args"
    d.i += 1
    d.subs.append(f"std::__ndk1::__shared_ptr_emplace<{cls}, {alloc}>")
    m = re.match(r"C2(?:B\d+\w+?)?(?=I)", sym[d.i:])
    # ctor name with abi tag: C2B8ne190000
    m = re.match(r"C2B(\d+)", sym[d.i:])
    if m:
        d.i += 2
        d.i += 1
        d.source_name()
    elif sym[d.i:d.i + 2] == "C2":
        d.i += 2
    else:
        return None
    assert d.peek() == "I"
    d.i += 1
    assert d.peek() == "J", "argument pack"
    d.i += 1
    args = []
    while d.peek() != "E":
        args.append(d.type())
    return cls, args


def classify_arg(t):
    """Maps a demangled forwarded argument type to a semantic kind."""
    if re.search(r"Vag(Can|Uds)Ecu\*&$", t):
        return "ecu", ("VagCanEcu" if "VagCanEcu" in t else "VagUdsEcu")
    if "StringWhitelist" in t:
        return "whitelist", ("ref" if t.endswith("&") and not t.endswith("&&") else "value")
    m = re.match(r"char const\[(\d+)\]&$", t)
    if m:
        return "name", int(m.group(1))
    if "Interpretation" in t:
        m2 = re.search(r"(\w+Interpretation)", t)
        return "interpretation", (m2.group(1), "ref" if t.endswith(" const&") else "value")
    if t.startswith("std::__ndk1::shared_ptr<std::__ndk1::vector<unsigned long"):
        return "applicability_list", "ref" if t.endswith("&") else "value"
    if t.startswith("std::__ndk1::vector<unsigned char"):
        return "byte_vector", "value"
    if t in ("int", "short", "unsigned char", "unsigned short", "int&", "short&"):
        return "int", t
    if "Consistency" in t:
        return "consistency", t
    if "AvailBy" in t:
        return "avail_by", t
    return "other", t


# ---------------------------------------------------------------------------
# ELF context
# ---------------------------------------------------------------------------

def demangle_data_symbol(name):
    if not name.startswith("_ZN"):
        return name
    try:
        d = Demangler(name[2:])
        return d.nested_name()
    except Exception:
        return name


class Binary:
    def __init__(self, path):
        self.path = path
        with open(path, "rb") as fh:
            self.raw = fh.read()
        self.sha256 = hashlib.sha256(self.raw).hexdigest()
        import io
        self.elf = ELFFile(io.BytesIO(self.raw))
        self.segments = [(s["p_vaddr"], s["p_offset"], s["p_filesz"])
                         for s in self.elf.iter_segments() if s["p_type"] == "PT_LOAD"]
        self.cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
        self.cs.detail = True
        self._load_symbols()
        self._load_relocs()
        self._load_plt()

    def read(self, vaddr, size):
        for va, off, sz in self.segments:
            if va <= vaddr and vaddr + size <= va + sz:
                o = off + (vaddr - va)
                return self.raw[o:o + size]
        raise ValueError(f"unmapped {hex(vaddr)}")

    def cstring(self, vaddr):
        try:
            data = self.read(vaddr, 256)
        except ValueError:
            return None
        end = data.find(b"\x00")
        if end < 0:
            return None
        try:
            return data[:end].decode("ascii")
        except UnicodeDecodeError:
            return None

    def _load_symbols(self):
        self.func_syms = {}
        ds = self.elf.get_section_by_name(".dynsym")
        for s in ds.iter_symbols():
            if s.name:
                self.func_syms[s.name] = (s["st_value"], s["st_size"])

    def _load_relocs(self):
        self.got_sym = {}
        for sec in self.elf.iter_sections():
            if not sec.name.startswith(".rela"):
                continue
            symtab = self.elf.get_section(sec["sh_link"])
            for rel in sec.iter_relocations():
                if rel["r_info_sym"] == 0:
                    continue
                sym = symtab.get_symbol(rel["r_info_sym"])
                if sym.name:
                    self.got_sym[rel["r_offset"]] = sym.name

    def _load_plt(self):
        plt = self.elf.get_section_by_name(".plt")
        self.plt_sym = {}
        self.plt_got = {}
        ins = list(self.cs.disasm(self.read(plt["sh_addr"], plt["sh_size"]), plt["sh_addr"]))
        for k in range(len(ins) - 1):
            a, b = ins[k], ins[k + 1]
            if a.mnemonic == "adrp" and b.mnemonic == "ldr":
                page = a.operands[1].imm
                mem = b.operands[1].mem
                slot = page + mem.disp
                if slot in self.got_sym:
                    self.plt_sym[a.address] = self.got_sym[slot]
                    self.plt_got[a.address] = slot

    def disasm_function(self, name):
        addr, size = self.func_syms[name]
        return list(self.cs.disasm(self.read(addr, size), addr)), addr, size


# ---------------------------------------------------------------------------
# Factory helper resolution
# ---------------------------------------------------------------------------

def reg_name(cs, r):
    n = cs.reg_name(r)
    if n and n[0] == "w" and n[1:].isdigit():
        return "x" + n[1:]
    if n == "wzr":
        return "xzr"
    return n


def resolve_helper(binary, target):
    """Returns helper record or None. Accepts only pure forwarding helpers."""
    code = binary.read(target, 4 * 400)
    ins = []
    for i in binary.cs.disasm(code, target):
        ins.append(i)
        if i.mnemonic == "ret":
            break
    # Track register copies from entry until the first emplace call.
    origin = {f"x{k}": f"x{k}" for k in range(0, 9)}  # value = helper entry register
    for i in ins:
        if i.mnemonic == "bl":
            t = i.operands[0].imm
            sym = binary.plt_sym.get(t, "")
            if "__shared_ptr_emplace" in sym:
                parsed = parse_emplace_symbol(sym)
                if not parsed:
                    return None
                cls, arg_types = parsed
                # emplace ctor: x0 = this, x1 = allocator, x2.. = forwarded args
                mapping = []
                for k, _ in enumerate(arg_types):
                    reg = f"x{k + 2}"
                    if k + 2 > 7:
                        mapping.append(None)  # stack-passed forwarded arg; not modelled
                        continue
                    mapping.append(origin.get(reg))
                return {
                    "helper_address": hex(target),
                    "emplace_call": hex(i.address),
                    "emplace_plt": hex(t),
                    "emplace_got_slot": hex(binary.plt_got[t]),
                    "emplace_symbol": sym,
                    "concrete_class": cls,
                    "forwarded_arg_types": arg_types,
                    "arg_entry_registers": mapping,
                }
            for k in list(origin):
                if k == "x30" or (k.startswith("x") and k[1:].isdigit() and int(k[1:]) <= 18):
                    origin[k] = None
            continue
        if i.mnemonic in ("blr", "br", "ret", "b") or i.mnemonic.startswith("b."):
            return None
        _, regs_written = i.regs_access()
        written = {reg_name(binary.cs, r) for r in regs_written}
        if i.mnemonic == "mov" and len(i.operands) == 2 and i.operands[1].type == A.ARM64_OP_REG:
            dst = reg_name(binary.cs, i.operands[0].reg)
            src = reg_name(binary.cs, i.operands[1].reg)
            origin[dst] = origin.get(src)
            continue
        for w in written:
            origin[w] = None
    return None


# ---------------------------------------------------------------------------
# CFG reaching-definition analysis
# ---------------------------------------------------------------------------

BRANCH_UNCOND = {"b", "br", "ret"}
CALLS = {"bl", "blr"}
CLOBBERED = {f"x{k}" for k in range(0, 19)} | {"x30"}


class Unproven(Exception):
    def __init__(self, reason, at=None):
        super().__init__(reason)
        self.reason = reason
        self.at = at


class Function:
    def __init__(self, binary, name):
        self.binary = binary
        self.name = name
        self.ins, self.start, self.size = binary.disasm_function(name)
        self.end = self.start + self.size
        self.idx = {i.address: k for k, i in enumerate(self.ins)}
        self._decode()
        self._build_cfg()

    def _decode(self):
        cs = self.binary.cs
        self.writes = []
        for i in self.ins:
            _, w = i.regs_access()
            self.writes.append({reg_name(cs, r) for r in w})

    def _branch_target(self, i):
        for op in i.operands:
            if op.type == A.ARM64_OP_IMM and self.start <= op.imm < self.end:
                return op.imm
        return None

    def _build_cfg(self):
        leaders = {self.start}
        for k, i in enumerate(self.ins):
            m = i.mnemonic
            if m in BRANCH_UNCOND or m.startswith("b.") or m in ("cbz", "cbnz", "tbz", "tbnz"):
                if k + 1 < len(self.ins):
                    leaders.add(self.ins[k + 1].address)
                if m not in ("br", "ret"):
                    t = self._branch_target(i)
                    if t is not None:
                        leaders.add(t)
        self.block_start = {}
        order = sorted(leaders)
        self.leader_set = set(order)
        self.preds = defaultdict(list)
        # map each instruction index to its block leader index
        cur = None
        self.block_of = [0] * len(self.ins)
        for k, i in enumerate(self.ins):
            if i.address in self.leader_set:
                cur = k
            self.block_of[k] = cur
        for k, i in enumerate(self.ins):
            m = i.mnemonic
            is_last = (k + 1 == len(self.ins)) or (self.ins[k + 1].address in self.leader_set)
            if m in ("b",) or m.startswith("b.") or m in ("cbz", "cbnz", "tbz", "tbnz"):
                t = self._branch_target(i)
                if t is not None and t in self.idx:
                    self.preds[self.idx[t]].append(k)
            if is_last and k + 1 < len(self.ins) and m not in BRANCH_UNCOND:
                self.preds[k + 1].append(k)
        # sp must only change in the prologue/epilogue
        self.sp_writers = [k for k, w in enumerate(self.writes) if "sp" in w]

    # -- register values ---------------------------------------------------

    def reg_value(self, reg, k, visited=None, depth=0, blk=None):
        """Value of `reg` immediately before instruction index k.

        `blk` is the leader index of the basic block being walked. It defaults to the block
        containing k; predecessor queries pass the predecessor's own block and k = p + 1
        (the point just after the predecessor's last instruction), because p + 1 is by
        construction a leader of a *different* block.
        """
        if reg in ("xzr",):
            return ("const", 0), []
        if reg == "sp":
            return ("sp", 0), []
        if depth > 64:
            raise Unproven("depth_limit")
        if visited is None:
            visited = set()
        leader = self.block_of[k] if blk is None else blk
        j = k - 1
        while True:
            if j < leader:
                return self._merge_preds(
                    leader,
                    lambda p: self.reg_value(reg, p + 1, visited, depth + 1, blk=self.block_of[p]),
                    visited, ("reg", reg))
            i = self.ins[j]
            if i.mnemonic in CALLS and reg in CLOBBERED:
                raise Unproven(f"{reg} clobbered by call", hex(i.address))
            if reg in self.writes[j]:
                return self._eval_def(reg, j, visited, depth)
            j -= 1

    def _merge_preds(self, leader, fn, visited, key):
        vk = (key, leader)
        if vk in visited:
            raise Unproven("loop_in_definition_chain", hex(self.ins[leader].address))
        preds = self.preds.get(leader, [])
        if not preds:
            raise Unproven("reached_function_entry", hex(self.ins[leader].address))
        visited = visited | {vk}
        results = []
        for p in sorted(preds):
            results.append(fn(p))
        vals = {json.dumps(r[0]) for r in results}
        if len(vals) != 1:
            raise Unproven("merge_conflict", hex(self.ins[leader].address))
        chain = []
        for r in results:
            chain.extend(r[1])
        return results[0][0], sorted(set(chain))

    def _eval_def(self, reg, j, visited, depth):
        i = self.ins[j]
        m = i.mnemonic
        ops = i.operands
        here = [hex(i.address)]

        def sub(r):
            v, c = self.reg_value(r, j, visited, depth + 1, blk=self.block_of[j])
            return v, c

        if m == "adrp":
            return ("const", ops[1].imm), here
        if m in ("mov", "movz") and len(ops) == 2:
            if ops[1].type == A.ARM64_OP_IMM:
                return ("const", ops[1].imm & 0xFFFFFFFFFFFFFFFF), here
            if ops[1].type == A.ARM64_OP_REG:
                v, c = sub(reg_name(self.binary.cs, ops[1].reg))
                return v, here + c
        if m == "movn" and ops[1].type == A.ARM64_OP_IMM:
            return ("const", ~ops[1].imm), here
        if m in ("add", "sub") and len(ops) == 3 and ops[2].type == A.ARM64_OP_IMM:
            src = reg_name(self.binary.cs, ops[1].reg)
            imm = ops[2].imm
            if ops[2].shift.type == A.ARM64_SFT_LSL:
                imm <<= ops[2].shift.value
            if m == "sub":
                imm = -imm
            v, c = sub(src)
            if v[0] in ("const", "sp"):
                return (v[0], v[1] + imm), here + c
            raise Unproven(f"add on non-constant {v[0]}", hex(i.address))
        if m == "ldr" and len(ops) == 2 and ops[1].type == A.ARM64_OP_MEM and not i.writeback:
            base = reg_name(self.binary.cs, ops[1].mem.base)
            if ops[1].mem.index == 0 and base != "sp":
                v, c = sub(base)
                if v[0] == "const":
                    slot = v[1] + ops[1].mem.disp
                    if slot in self.binary.got_sym:
                        return ("got", self.binary.got_sym[slot], slot), here + c
        raise Unproven(f"unmodelled definition '{m} {i.op_str}'", hex(i.address))

    # -- stack memory -------------------------------------------------------

    def _store_access(self, j):
        """For a store at index j returns list of (sp_offset, size, src_reg) or None if not a store."""
        i = self.ins[j]
        m = i.mnemonic
        if m in ("stlr", "stlrb", "stlrh") or not m.startswith("st"):
            return None
        if m not in ("str", "stur", "strb", "sturb", "strh", "sturh", "stp", "stnp"):
            return ("unknown_base", hex(i.address))  # unmodelled store form: cannot prove non-aliasing
        ops = i.operands
        op_mem = ops[-1]
        if op_mem.type != A.ARM64_OP_MEM:
            return None
        base = reg_name(self.binary.cs, op_mem.mem.base)
        try:
            bv, _ = (self.reg_value(base, j, blk=self.block_of[j]) if base != "sp" else (("sp", 0), []))
        except Unproven:
            return ("unknown_base", hex(i.address))
        if bv[0] != "sp":
            return []  # store to non-stack memory (GOT/heap constant) - cannot alias a stack slot
        disp = 0 if (i.writeback and len(ops) == 3 and ops[2].type == A.ARM64_OP_IMM) else op_mem.mem.disp
        regs = [o for o in ops if o.type == A.ARM64_OP_REG]
        out = []
        off = bv[1] + disp
        for r in regs:
            name = self.binary.cs.reg_name(r.reg)
            size = {"w": 4, "x": 8, "q": 16, "d": 8, "s": 4, "h": 2, "b": 1}.get(name[0], 8)
            if m == "strb":
                size = 1
            elif m == "strh":
                size = 2
            out.append((off, size, reg_name(self.binary.cs, r.reg)))
            off += size
        return out

    def stack_value(self, sp_off, size, k, visited=None, depth=0, blk=None):
        """Value stored in [sp+sp_off, size) immediately before instruction index k."""
        if depth > 64:
            raise Unproven("depth_limit")
        if visited is None:
            visited = set()
        leader = self.block_of[k] if blk is None else blk
        j = k - 1
        while j >= leader:
            i = self.ins[j]
            if i.mnemonic in CALLS:
                raise Unproven("call between stack store and use", hex(i.address))
            acc = self._store_access(j)
            if acc is not None:
                if isinstance(acc, tuple):
                    raise Unproven("store through unresolved base between def and use", acc[1])
                for off, sz, src in acc:
                    if off == sp_off and sz == size:
                        if src == "xzr":
                            return ("const", 0), [hex(i.address)]
                        v, c = self.reg_value(src, j, blk=self.block_of[j])
                        if v[0] != "const":
                            raise Unproven(f"stored register holds {v[0]}", hex(i.address))
                        mask = (1 << (8 * size)) - 1
                        return ("const", v[1] & mask), [hex(i.address)] + c
                    if off < sp_off + size and sp_off < off + sz:
                        raise Unproven("partial overlapping store", hex(i.address))
            j -= 1
        return self._merge_preds(
            leader,
            lambda p: self.stack_value(sp_off, size, p + 1, visited, depth + 1, blk=self.block_of[p]),
            visited, ("stack", sp_off, size))


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

INT_SIZES = {"int": 4, "short": 2, "unsigned char": 1, "unsigned short": 2}


def extract(so_path=DEFAULT_SO):
    binary = Binary(so_path)
    helpers = {}
    callsites = []
    stats = defaultdict(int)

    for fname in SOURCE_FUNCTIONS:
        fn = Function(binary, fname)
        pretty = demangle_data_symbol(fname)
        body_sp_writers = [k for k in fn.sp_writers if k > 30]
        if body_sp_writers:
            raise RuntimeError(f"{pretty}: sp modified in function body at {body_sp_writers}; stack model invalid")
        for k, i in enumerate(fn.ins):
            if i.mnemonic != "bl":
                continue
            target = i.operands[0].imm
            if target in binary.plt_sym:
                continue
            if target not in helpers:
                helpers[target] = resolve_helper(binary, target)
            h = helpers[target]
            if not h:
                stats["bl_non_factory"] += 1
                continue
            stats["factory_calls"] += 1
            callsites.append(extract_callsite(fn, pretty, k, h))

    factory_map = {
        "metadata": {
            "binary_sha256": binary.sha256,
            "extractor_version": EXTRACTOR_VERSION,
            "rule": "helper_address is the BL target. A helper is a factory only if it forwards its argument "
                    "registers unchanged into a PLT call of std::__shared_ptr_emplace<Class>; class and "
                    "argument types are parsed from that PLT symbol.",
        },
        "factories": {h["helper_address"]: h for h in helpers.values() if h},
    }
    meta = {
        "binary_sha256": binary.sha256,
        "extractor_version": EXTRACTOR_VERSION,
        "source_functions": {demangle_data_symbol(n): {"address": hex(binary.func_syms[n][0]),
                                                       "size": binary.func_syms[n][1]}
                             for n in SOURCE_FUNCTIONS},
        "factory_callsites": len(callsites),
        "non_factory_bl": stats["bl_non_factory"],
    }
    return {"metadata": meta, "callsites": callsites}, factory_map


def extract_callsite(fn, pretty, k, h):
    ins = fn.ins[k]
    kinds = [classify_arg(t) for t in h["forwarded_arg_types"]]
    args = []
    for pos, (t, (kind, detail)) in enumerate(zip(h["forwarded_arg_types"], kinds)):
        entry_reg = h["arg_entry_registers"][pos]
        a = {"index": pos, "type": t, "kind": kind, "register": entry_reg}
        try:
            if entry_reg is None:
                raise Unproven("argument not forwarded in a register by helper")
            ptr, chain = fn.reg_value(entry_reg, k)
            a["pointer"] = ptr
            if kind in ("ecu", "whitelist", "interpretation", "applicability_list") and ptr[0] == "got":
                a["value"] = demangle_data_symbol(ptr[1])
                a["got_slot"] = hex(ptr[2])
            elif kind == "name" and ptr[0] == "const":
                s = fn.binary.cstring(ptr[1])
                a["value"] = s
                a["array_length_check"] = (s is not None and len(s) + 1 == detail)
                if not a["array_length_check"]:
                    raise Unproven(f"string length {None if s is None else len(s)+1} != char[{detail}]")
            elif kind == "int" and ptr[0] == "sp":
                v, c2 = fn.stack_value(ptr[1], INT_SIZES[detail], k)
                a["value"] = v[1]
                chain = chain + c2
            elif kind in ("interpretation", "whitelist") and ptr[0] == "sp":
                raise Unproven(f"{kind} is a runtime-constructed temporary (by value)")
            elif kind in ("byte_vector", "applicability_list", "consistency", "avail_by") and ptr[0] == "sp":
                raise Unproven(f"{kind} is a runtime-constructed temporary")
            else:
                raise Unproven(f"pointer kind {ptr[0]} not resolvable for {kind}")
            a["status"] = "PROVEN"
            a["def_chain"] = chain
        except Unproven as u:
            a["status"] = "UNPROVEN"
            a["reason"] = u.reason
            if u.at:
                a["at"] = u.at
        args.append(a)

    return {
        "callsite": hex(ins.address),
        "source_function": pretty,
        "helper_address": h["helper_address"],
        "emplace_got_slot": h["emplace_got_slot"],
        "concrete_class": h["concrete_class"],
        "args": args,
    }


def render_json(obj):
    """Canonical serialisation shared with tests/molecular_reproducibility.py."""
    return json.dumps(obj, indent=1, sort_keys=True) + "\n"


def main():
    so = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SO
    data, fmap = extract(so)
    with open(OUT_CALLSITES, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_json(data))
    with open(OUT_FACTORIES, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_json(fmap))
    print(f"[+] {len(data['callsites'])} factory callsites, {len(fmap['factories'])} factory helpers")
    print(f"[+] binary sha256 {data['metadata']['binary_sha256']}")


if __name__ == "__main__":
    main()
