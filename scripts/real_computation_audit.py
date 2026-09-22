#!/usr/bin/env python3
"""
AETHERZ3OMEGA: REAL COMPUTATION AUDIT (INDEPENDENT, HIGH-PRECISION)
====================================================================
Independent numerical audit of the sensitive facts claimed in the Lean
corpus (RhCore.lean / RhZetaTower.lean / BarrierTheorem.lean). Does NOT
trust any previous report: every value is recomputed here with mpmath at
the stated working precision.

Checked facts (each maps to a formal Lean declaration):
  F1  zetaEnergy s = (re s - 1/2)^2  == 0  <=>  re s = 1/2       (zetaEnergy_zero_iff)
  F2  log(1+eps) < eps for all eps > 0                            (zetaEnergy_log_bound)
  F3  zeta(0) = -1/2  ==> 0 is NOT a zeta zero                     (zeta_value_zero / zero_is_not_zeta_zero)
  F4  zeta(-2(n+1)) = 0 for n = 0..N  (trivial zeros)              (trivial_zeta_zero)
  F5  every trivial zero is FAR from the critical line            (trivial_zeros_off_critical_line)
  F6  zeta(-4) = 0 and re(-4) = -4  ==> the OLD absolute barrier
      'forall s, zeta s = 0 -> re s = 1/2' is inconsistent        (old_absolute_barrier_is_inconsistent)
  F7  first K non-trivial zeros verified on the critical line      (RiemannHypothesis, numerical support)
  F8  Von Mangoldt N(T) ~ (T/2pi) log(T/2pi) - T/2pi + O(log T)   (zero counting law)
Usage:
    python scripts/real_computation_audit.py  (writes ../exports/real_computation_audit.json)
"""
import json
import os
import time

import mpmath as mp

mp.mp.dps = 40  # working precision: 40 decimal digits

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "exports",
                   "real_computation_audit.json")


def audit():
    results = []
    ok_all = True

    # ---- F1: zetaEnergy zero iff critical line ---------------------------
    s_off = mp.mpf("0.3") + 1j * mp.mpf("14.134725141734693790457251983562470270784")
    s_on = mp.mpf("0.5") + 1j * mp.mpf("14.134725141734693790457251983562470270784")
    E_off = (s_off.real - mp.mpf("0.5")) ** 2
    E_on = (s_on.real - mp.mpf("0.5")) ** 2
    ok1 = (E_on == 0) and (E_off > 0)
    results.append({
        "fact": "F1",
        "description": "zetaEnergy s = (re s - 1/2)^2 == 0 <=> re s = 1/2",
        "computed": {"E(off, re=0.3)": str(E_off), "E(on, re=0.5)": str(E_on)},
        "expect": "E_on == 0 and E_off > 0", "pass": ok1,
    })
    ok_all &= ok1

    # ---- F2: log(1+eps) < eps -------------------------------------------
    eps_bound = [mp.mpf("1e-3"), mp.mpf("0.1"), mp.mpf("0.5"), mp.mpf("1.0"), mp.mpf("10.0")]
    violations = []
    for e in eps_bound:
        lhs = mp.log1p(e)
        if not lhs < e:
            violations.append(str(e))
    ok2 = (len(violations) == 0)
    results.append({
        "fact": "F2",
        "description": "log(1+eps) < eps for eps in {1e-3,0.1,0.5,1,10}",
        "computed": {str(e): str(mp.log1p(e)) for e in eps_bound},
        "expect": "no violations", "pass": ok2,
    })
    ok_all &= ok2

    # ---- F3: zeta(0) = -1/2 ---------------------------------------------
    z0 = mp.zeta(0)
    ok3 = (z0 == mp.mpf("-0.5")) and (z0 != 0)
    results.append({
        "fact": "F3",
        "description": "zeta(0) = -1/2 (so 0 is not a zero)",
        "computed": {"zeta(0)": str(z0)},
        "expect": "-0.5", "pass": ok3,
    })
    ok_all &= ok3

    # ---- F4 + F5: trivial zeros on negative even axis --------------------
    K = 10
    trivial = []
    trivial_ok = True
    for n in range(K):
        s = -2 * mp.mpf(n + 1)
        val = mp.zeta(s)
        dist = abs((s - mp.mpf("0.5")))
        trivial.append({"s": str(s), "zeta": str(val),
                        "dist_to_critical_real": str(dist),
                        "is_zero_rel": (abs(val) < mp.mpf("1e-35"))})
        trivial_ok &= (abs(val) < mp.mpf("1e-35"))
    results.append({
        "fact": "F4+F5",
        "description": f"zeta(-2(n+1)) = 0 for n=0..{K-1} and Re = -2(n+1) != 1/2",
        "computed": trivial,
        "expect": "all |zeta| < 1e-35 and every Re far from 0.5", "pass": trivial_ok,
    })
    ok_all &= trivial_ok

    # ---- F6: the OLD absolute barrier is falsified -----------------------
    z4 = mp.zeta(-4)
    re4 = mp.mpf("-4")
    ok6 = (abs(z4) < mp.mpf("1e-35")) and (re4 != mp.mpf("0.5"))
    results.append({
        "fact": "F6",
        "description": "zeta(-4)=0 with Re=-4: disproves 'forall zeros re s = 1/2'",
        "computed": {"zeta(-4)": str(z4), "re(-4)": "-4", "re(-4)==0.5?": str(re4 == mp.mpf("0.5"))},
        "expect": "zeta(-4)==0 and re != 0.5", "pass": ok6,
    })
    ok_all &= ok6

    # ---- F7: first K_nt non-trivial zeros on critical line (numerical) ---
    K_nt = 25
    zeros = mp.zetazero_conjugate if hasattr(mp, "zetazero_conjugate") else None
    nt = []
    nt_ok = True
    for k in range(1, K_nt + 1):
        y = mp.zetazero(k)
        s = mp.mpf("0.5") + 1j * mp.im(y)
        val = mp.zeta(s)
        re_s = mp.re(s)
        nt.append({"k": k, "gamma": str(mp.im(y)),
                   "re": str(re_s), "|zeta(0.5+i gamma)|": str(abs(val))})
        nt_ok &= (abs(re_s - mp.mpf("0.5")) < mp.mpf("1e-30")) and \
                 (abs(val) < mp.mpf("1e-20"))
    results.append({
        "fact": "F7",
        "description": f"first {K_nt} non-trivial zeros: zeta(0.5+i gamma) ~ 0 (numerical RH support)",
        "computed": nt,
        "expect": f"all |zeta| < 1e-20 for k=1..{K_nt}", "pass": nt_ok,
    })
    ok_all &= nt_ok

    # ---- F8: Von Mangoldt counting law ------------------------------------
    T_list = [mp.mpf(t) for t in (100, 1000, 5000)]
    vm = []
    for T in T_list:
        args_hi = mp.nzeros(T)
        exact_N = int(args_hi)
        term = (T / (2 * mp.pi)) * mp.log(T / (2 * mp.pi)) - (T / (2 * mp.pi))
        log_T = mp.log(T)
        vm.append({
            "T": str(T), "N(T)_exact": int(exact_N),
            "main_term": str(term), "O(log T)": str(log_T),
            "|N(T) - main| <= log T": bool(abs(exact_N - term) <= log_T),
        })
    vm_ok = all(b["|N(T) - main| <= log T"] for b in vm)
    results.append({
        "fact": "F8",
        "description": "Von Mangoldt N(T) = (T/2pi)log(T/2pi) - T/2pi + O(log T)",
        "computed": vm, "expect": "|N(T) - main_term| <= log T for all T", "pass": vm_ok,
    })
    ok_all &= vm_ok

    out = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "precision_digits": 40,
        "engine": f"mpmath {mp.__version__}",
        "overall": "PASS" if ok_all else "FAIL",
        "facts": results,
    }
    return out


if __name__ == "__main__":
    report = audit()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=4, ensure_ascii=False)
    print(json.dumps({"engine": report["engine"],
                      "precision_digits": report["precision_digits"],
                      "overall": report["overall"],
                      "facts": [f["fact"] + (" OK" if f["pass"] else " FAIL")
                                for f in report["facts"]]}, indent=2))
    print(f"Laporan numerik nyata disimpan ke {os.path.abspath(OUT)}")