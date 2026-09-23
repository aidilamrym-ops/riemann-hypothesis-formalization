import json
from pathlib import Path

from mpmath import mp, mpf, power

DIGITS = 40
mp.dps = DIGITS + 10

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
S_EXPONENTS = ["1.01", "1.1", "1.25", "1.5", "1.99", "2", "3", "5", "10"]

# Kernel-selection independence sweep:
# for every (prime p, exponent s > 1) the Euler-product kernel factor
#   0 < p^(-s) < 1  and  0 < 1 - p^(-s) < 1   and  (1 - p^(-s))^(-1) > 1
# Lean-proved universally (AetherZ3Omega.Riemann.KernelIndependence);
# this script independently samples the domain to cross-check numerically.
failures = []
n_checks = 0
lo_factor = None
hi_factor = None
lo_rem = None

for p in PRIMES:
    for s_str in S_EXPONENTS:
        s = mpf(s_str)
        assert s > 1
        base = mpf(p)
        term = power(base, -s)          # p^(-s)
        factor = mpf(1) - term          # 1 - p^(-s)
        rem = mpf(1) / factor           # (1 - p^(-s))^(-1)
        n_checks += 1
        if not (mpf(0) < term < mpf(1)):
            failures.append({"p": p, "s": s_str, "term_unit_bad": str(term)})
        if not (mpf(0) < factor < mpf(1)):
            failures.append({"p": p, "s": s_str, "factor_unit_bad": str(factor)})
        if not (rem > mpf(1)):
            failures.append({"p": p, "s": s_str, "renorm_bad": str(rem)})
        if lo_factor is None or factor < lo_factor:
            lo_factor = factor
        if hi_factor is None or factor > hi_factor:
            hi_factor = factor
        if lo_rem is None or rem < lo_rem:
            lo_rem = rem

results = {
    "audit": "kernel_independence_numeric",
    "digits": DIGITS,
    "domain_sampled": {
        "primes": PRIMES,
        "s_values": S_EXPONENTS,
        "points": n_checks,
        "note": "Lean universal proof covers ALL p >= 2, s > 1; this sweep samples the domain as an independent cross-check",
    },
    "check": "for each (p, s): 0 < p^(-s) < 1  and  0 < 1 - p^(-s) < 1  and  (1-p^(-s))^(-1) > 1",
    "observed": {
        "min_factor": mp.nstr(lo_factor, 10, strip_zeros=False),
        "max_factor": mp.nstr(hi_factor, 10, strip_zeros=False),
        "min_renorm": mp.nstr(lo_rem, 10, strip_zeros=False),
    },
    "passed": len(failures) == 0,
    "failures": failures[:10],
}

out = Path(__file__).resolve().parent.parent / "exports" / "kernel_independence_numeric.json"
out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"kernel-independence numeric sweep: {n_checks} points, failures={len(failures)}")
if lo_factor is not None:
    print(f"  factor 1 - p^(-s) range: [{mp.nstr(lo_factor, 10, strip_zeros=False)}, "
          f"{mp.nstr(hi_factor, 10, strip_zeros=False)}] (all in (0,1))")
    print(f"  renormalisation (1-p^(-s))^(-1) min: {mp.nstr(lo_rem, 10, strip_zeros=False)} (all > 1)")
print("PASS: numeric cross-check consistent with Lean universal proof." if not failures
      else "FAIL: discrepancies found")
print(f"report -> {out}")
if failures:
    raise SystemExit(1)