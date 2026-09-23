import json

from mpmath import mp, mpf, tan, sqrt, cot, pi

DIGITS = 40
mp.dps = DIGITS + 10

sq2 = sqrt(mpf(2))
t = tan(mpf(1) / sq2)

cMT_closed = sq2 * t / (1 + (mpf(1) / sq2) * t)

inv_MT_classical = mpf(1) / mpf(2) + mpf(2) ** (-mpf(1) / 2) * cot(mpf(2) ** (-mpf(1) / 2))
inv_cMT = mpf(1) / cMT_closed
inv_cMT_alt = sq2 / t + mpf(1) / 2

prop1 = mpf(2) - inv_cMT
prop2 = mpf(2) * cMT_closed - mpf(1)

claims = {
    "c1star": "0.7532960",
    "one_over_cMT": "1.32750",
    "two_minus_one_over_cMT": "0.67250",
    "two_cMT_minus_one": "0.50659",
}

CLAIM_TOL = mpf(5) * mpf(10) ** -mpf(6)


def lead(x, n=10):
    s = mp.nstr(x, n, strip_zeros=False)
    return s


def within(x, s):
    return abs(x - mpf(s)) <= CLAIM_TOL


results = {
    "digits": DIGITS,
    "match_tolerance": str(CLAIM_TOL),
    "cMT_closed_form": lead(cMT_closed),
    "one_over_cMT": lead(inv_cMT),
    "one_over_cMT_via_MontgomeryTaylor": lead(inv_MT_classical),
    "one_over_cMT_alt": lead(inv_cMT_alt),
    "two_minus_one_over_cMT": lead(prop1),
    "two_cMT_minus_one": lead(prop2),
    "matches_paper_c1star": within(cMT_closed, claims["c1star"]),
    "matches_paper_one_over_cMT": within(inv_cMT, claims["one_over_cMT"]),
    "matches_paper_prop1": within(prop1, claims["two_minus_one_over_cMT"]),
    "matches_paper_prop2": within(prop2, claims["two_cMT_minus_one"]),
    "lean_bounds_respected": float(cMT_closed) > 2 / 3 and float(cMT_closed) <= 4 / 5,
    "paper_defs_note": "paper: c1*=2.tan(1/sqrt2)/(sqrt2+tan(1/sqrt2))=sqrt2.tan(1/sqrt2)/(1+(1/sqrt2).tan(1/sqrt2)); 1/c1* = 1/2 + 2^-1/2 . cot(2^-1/2)",
}

diff_MT = inv_cMT - inv_MT_classical
results["abs_diff_one_over_cMT_vs_MontgomeryTaylor"] = mp.nstr(diff_MT, 15)

with open(r"C:\Users\usER\oracle-toe\FINAL_RH_PROJECT\exports\numeric_constants_check.json", "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=2, ensure_ascii=False)

for k in results:
    if k.startswith("matches") or k.startswith("lean"):
        print(f"{k}: {results[k]}")
print()
for k in (
    "cMT_closed_form",
    "one_over_cMT",
    "one_over_cMT_via_MontgomeryTaylor",
    "abs_diff_one_over_cMT_vs_MontgomeryTaylor",
    "two_minus_one_over_cMT",
    "two_cMT_minus_one",
):
    print(f"{k}: {results[k]}")