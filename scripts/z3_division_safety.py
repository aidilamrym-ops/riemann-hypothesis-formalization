#!/usr/bin/env python3
"""
Z3 tribunal re-audit: vacuity + division-safety + NFE labels (Jalur B item 2).

WHY A REWRITE: the previous scripts/z3_vacuity_scan.py never recorded a
single verdict (calls=0 for every batch).  Its `verify` injection was
overwritten by each batch's own `def verify`, and ten of the thirteen
batches keep every solver.check() behind an `if __name__ == "__main__"`
guard that never fires under importlib exec_module.  This script instead:

  * executes each batch with __name__ == "__main__" so ALL checks run;
  * records at the Solver.check() level (style-agnostic) with a temporary
    z3.Solver subclass installed only during that batch's execution;
  * for every recorded verdict audits the three artifact modes:
      VACUITY      premises (all assertions except the last, which is the
                   negation under test) must be SAT; otherwise the UNSAT
                   proves nothing.  A witness model is stored when SAT.
      DIVISION     Z3 real division `e1/e2` is TOTAL: e2 = 0 yields an
                   arbitrary value, so an UNSAT can be an artifact.  Every
                   divisor is labelled: do the premises already force it
                   nonzero?  The verdict is re-checked with the guard
                   `denominator != 0`; if it is no longer UNSAT the claim
                   is DIVISION-SENSITIVE (suspect).
      ROOT/POWER   a^b with symbolic b is guarded by a != 0; a^(p/q) with
                   q > 1 is guarded by a >= 0 (roots of negatives are the
                   analogous partial-semantic hazard).
      UNKNOWN/NFE  results of `unknown` are captured with reason_unknown.

Output: exports/z3_division_safety.json + console summary.
CLI is backwards-compatible with scripts/z3_vacuity_scan.py (wrapper).
"""
import contextlib
import io
import json
import sys
import traceback
from fractions import Fraction
from pathlib import Path

import z3
from z3 import (
    Solver, sat, unsat, unknown, is_div, is_app, is_rational_value,
    Z3_OP_POWER,
)

ROOT = Path(__file__).resolve().parent.parent
TRIB = ROOT / "z3_tribunal"
OUT = ROOT / "exports"
TIMEOUT_MS = 15000
MAX_WITNESS_DECLS = 15

_OriginalSolver = z3.Solver
_RECORDS = []
_CAPTURE = False


class RecordingSolver(_OriginalSolver):
    def check(self, *args, **kwargs):
        r = super().check(*args, **kwargs)
        if _CAPTURE:
            snapshot = list(self.assertions())
            meta = _caller_meta()
            meta.update({
                "assertions": snapshot,
                "result": r,
            })
            if r == z3.unknown:
                try:
                    meta["reason_unknown"] = self.reason_unknown()
                except Exception:
                    meta["reason_unknown"] = "n/a"
            _RECORDS.append(meta)
        return r


def _caller_meta():
    """Recover file/line/name/stmt from the batch frame that called check()."""
    path, lineno, name, stmt = None, None, None, None
    try:
        fr = sys._getframe(1)
        while fr is not None:
            fn = fr.f_code.co_filename
            if Path(fn).parent.name == "z3_tribunal":
                path, lineno = fn, fr.f_lineno
                loc = fr.f_locals
                name = loc.get("name") or loc.get("theorem")
                stmt = loc.get("stmt") or loc.get("description")
                if name or lineno:
                    break
            fr = fr.f_back
    except Exception:
        pass
    if not name and lineno:
        name = f"line{lineno}"
    if not name:
        name = "unknown_site"
    return {"file": Path(path).name if path else "?", "line": lineno,
            "claim": str(name), "stmt": str(stmt) if stmt else None}


def _children(node):
    try:
        return list(node.children())
    except Exception:
        return [node.arg(i) for i in range(node.num_args())]


def _is_num(node):
    return is_rational_value(node) or z3.is_int_value(node)


def _num_nonzero(node):
    if is_rational_value(node):
        return node.as_fraction().numerator != 0
    if z3.is_int_value(node):
        return node.as_long() != 0
    return None  # not a numeric literal


def collect_guards(exprs):
    """Walk assertions; return (divisor_guards, root_guards, all_divisors).

    divisor_guards: list of (denominator_expr, sexpr) needing `!= 0`
    root_guards:    list of (base_expr, sexpr, kind) needing `>= 0` / `!= 0`
    all_divisors:   every nonzero-skipped divisor too (for reporting),
                    deduped by sexpr.
    """
    div_guards, root_guards, all_divs = {}, {}, {}
    seen = set()
    for e in exprs:
        stack = [e]
        while stack:
            node = stack.pop()
            key = node.sexpr()
            if key in seen:
                continue
            seen.add(key)
            if is_div(node):
                num, den = node.arg(0), node.arg(1)
                all_divs[den.sexpr()] = den
                nz = _num_nonzero(den)
                if nz is False or nz is None:
                    # literal-zero denominator would be nonsense; symbolic
                    # denominators need the guard.
                    if nz is None:
                        div_guards[den.sexpr()] = den
                # numerator does not need a guard; keep walking children
                stack.extend(_children(node))
                continue
            if is_app(node) and node.decl().kind() == Z3_OP_POWER:
                base, exp = node.arg(0), node.arg(1)
                if is_rational_value(exp):
                    f = exp.as_fraction()
                    if f.numerator < 0:
                        if _num_nonzero(base) is None:
                            div_guards[base.sexpr()] = base
                            root_guards[base.sexpr()] = (base, "base_nonzero_neg_exp")
                    elif f.denominator != 1:
                        if is_rational_value(base):
                            if base.as_fraction() >= 0:
                                pass  # numeric base already safe
                            else:
                                root_guards[base.sexpr()] = (base, "negative_base_root")
                        else:
                            root_guards[base.sexpr()] = (base, "base_nonneg_root")
                else:
                    # symbolic exponent: could be negative -> base != 0
                    if _num_nonzero(base) is None:
                        div_guards[base.sexpr()] = base
                        root_guards[base.sexpr()] = (base, "base_nonzero_sym_exp")
                stack.extend(_children(node))
                continue
            stack.extend(_children(node))
    return div_guards, root_guards, all_divs


def _solve(premises, extra=None, timeout=TIMEOUT_MS):
    s = Solver()
    s.set("timeout", timeout)
    for p in premises:
        s.add(p)
    if extra:
        for g in extra:
            s.add(g)
    return s.check()


def _witness(premises):
    s = Solver()
    s.set("timeout", TIMEOUT_MS)
    for p in premises:
        s.add(p)
    if s.check() != sat:
        return None
    m = s.model()
    decls = sorted(m.decls(), key=lambda d: d.name())
    if len(decls) > MAX_WITNESS_DECLS:
        return {"_truncated": True, "_ndecls": len(decls)}
    return {d.name(): str(m[d]) for d in decls}


def _has_symbolic_power(exprs):
    """True if any Power has a non-literal exponent (transcendental NFE)."""
    seen = set()
    for e in exprs:
        stack = [e]
        while stack:
            node = stack.pop()
            key = node.sexpr()
            if key in seen:
                continue
            seen.add(key)
            if is_app(node) and node.decl().kind() == Z3_OP_POWER:
                if not _is_num(node.arg(1)):
                    return True
            stack.extend(_children(node))
    return False


def audit_check(rec):
    assertions = rec["assertions"]
    result = rec["result"]
    out = {
        "claim": rec["claim"], "file": rec["file"], "line": rec["line"],
        "stmt": rec["stmt"], "result": str(result),
        "reason_unknown": rec.get("reason_unknown"),
        "n_assertions": len(assertions),
        "premises_consistent": None,
        "vacuous": False,
        "witness_model": None,
        "divisors": [],
        "roots": [],
        "division_sensitive": False,
        "guarded_result": None,
        "note": None,
    }
    if len(assertions) == 0:
        out["note"] = "no assertions recorded"
        return out

    premises = assertions[:-1] if len(assertions) > 1 else []
    div_guards, root_guards, all_divs = collect_guards(list(assertions))

    if result == unknown:
        if _has_symbolic_power(list(assertions)):
            out["note"] = ("NFE/transcendental: Power with symbolic real "
                           "exponent (e.g. p^(-s)) is outside QF_NRA; Z3 "
                           "cannot decide it (not a counterexample)")
        elif premises:
            pr = _solve(premises)
            if pr == unknown:
                out["note"] = "premises themselves undecidable in QF_NRA (e.g. Sqrt); verdict inconclusive"
        if out["note"] is None:
            out["note"] = f"Z3 returned unknown: {rec.get('reason_unknown')}"
        return out

    if result == unsat:
        pr = _solve(premises) if premises else sat
        # Only a definite UNSAT on premises means vacuous; `unknown` on the
        # premises is INCONCLUSIVE, not vacuous (batch13/Sqrt false-positive).
        out["premises_consistent"] = True if pr == sat else (
            False if pr == unsat else None)
        out["vacuous"] = pr == unsat
        if pr == unknown:
            out["note"] = "premises undecidable (QF_NRA incomplete); vacuity inconclusive"
        if pr == sat:
            out["witness_model"] = _witness(premises)

        guards = [d != 0 for d in div_guards.values()]
        for base, kind in root_guards.values():
            if kind == "base_nonneg_root":
                guards.append(base >= 0)
            else:
                guards.append(base != 0)
        if guards:
            gr = _solve(list(assertions) + guards)
            out["guarded_result"] = str(gr)
            out["division_sensitive"] = gr != unsat

        for key, den in all_divs.items():
            forced = None
            if premises:
                forced = _solve(list(premises) + [den == 0]) == unsat
            guarded = key not in div_guards  # literal-nonzero / safe
            out["divisors"].append({
                "divisor": key,
                "premises_force_nonzero": forced,
                "guard_needed": key in div_guards,
            })
        for key, (base, kind) in root_guards.items():
            out["roots"].append({"base": key, "kind": kind})
    return out


def run_batch(path: Path):
    src = path.read_text(encoding="utf-8-sig", errors="replace")  # strip BOM
    code = compile(src, str(path), "exec")
    ns = {"__name__": "__main__", "__file__": str(path),
          "__builtins__": __builtins__}
    buf = io.StringIO()
    err = None
    old_cwd = Path.cwd()
    global _CAPTURE
    _CAPTURE = True
    z3.Solver = RecordingSolver
    try:
        import os
        os.chdir(path.parent)  # batch JSON writes use ../exports/
        with contextlib.redirect_stdout(buf):
            exec(code, ns)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
    finally:
        z3.Solver = _OriginalSolver
        _CAPTURE = False
        try:
            os.chdir(old_cwd)
        except Exception:
            pass
    return buf.getvalue(), err


def main():
    global _RECORDS
    files = sorted(TRIB.glob("z3_*.py"))
    report = {
        "audit": "z3_division_safety_and_vacuity",
        "engine": {
            "method": "Solver.check-level recording; batch executed with "
                      "__name__=='__main__' so main-guarded checks run",
            "timeout_ms": TIMEOUT_MS,
            "note": "premises := all assertions except the last (the "
                    "negation under test); guards: denominator != 0, "
                    "symbolic/negative power base != 0, root base >= 0",
        },
        "batches": {},
        "summary": {},
    }
    S = {"checks": 0, "unsat": 0, "sat": 0, "unknown": 0,
         "vacuous": 0, "division_sensitive": 0,
         "divisors_seen": 0, "divisors_forced_nonzero": 0,
         "divisors_needing_guard": 0, "witnesses": 0, "exec_errors": 0}

    for f in files:
        _RECORDS = []
        stdout_text, err = run_batch(f)
        entries = [audit_check(r) for r in _RECORDS]
        report["batches"][f.stem] = {
            "exec_error": err,
            "stdout_tail": stdout_text.splitlines()[-8:],
            "checks": entries,
        }
        if err:
            S["exec_errors"] += 1
        for e in entries:
            S["checks"] += 1
            if e["result"] == "unsat":
                S["unsat"] += 1
            elif e["result"] == "sat":
                S["sat"] += 1
            elif e["result"] == "unknown":
                S["unknown"] += 1
            if e["vacuous"]:
                S["vacuous"] += 1
            if e["division_sensitive"]:
                S["division_sensitive"] += 1
            if e["witness_model"]:
                S["witnesses"] += 1
            for d in e["divisors"]:
                S["divisors_seen"] += 1
                if d["premises_force_nonzero"]:
                    S["divisors_forced_nonzero"] += 1
                if d["guard_needed"]:
                    S["divisors_needing_guard"] += 1

    report["summary"] = S
    out = OUT / "z3_division_safety.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False),
                   encoding="utf-8")

    print(f"checks={S['checks']} unsat={S['unsat']} sat={S['sat']} "
          f"unknown={S['unknown']} vacuous={S['vacuous']} "
          f"division_sensitive={S['division_sensitive']} "
          f"divisors={S['divisors_seen']} "
          f"(forced_nonzero={S['divisors_forced_nonzero']}, "
          f"needed_guard={S['divisors_needing_guard']}) "
          f"witnesses={S['witnesses']} exec_errors={S['exec_errors']}")
    for stem, b in report["batches"].items():
        flags = []
        if b["exec_error"]:
            flags.append(f"EXEC_ERROR={b['exec_error']}")
        for e in b["checks"]:
            if e["result"] == "unknown":
                flags.append(f"UNKNOWN:{e['claim']}({e['reason_unknown']})")
            if e["result"] == "sat":
                flags.append(f"COUNTERMODEL:{e['claim']}")
            if e["vacuous"]:
                flags.append(f"VACUOUS:{e['claim']}")
            if e["division_sensitive"]:
                flags.append(f"DIV_SENSITIVE:{e['claim']}")
        if flags:
            print(f"  [{stem}] " + "; ".join(flags))
    print(f"report -> {out}")


if __name__ == "__main__":
    main()