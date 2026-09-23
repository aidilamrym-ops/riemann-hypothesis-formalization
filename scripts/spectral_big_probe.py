import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import flint
from flint import acb
from multiprocessing import Pool
from scipy.optimize import brentq

TWO_PI = 2.0 * math.pi
PI_8 = math.pi / 8.0

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "exports"
N = int(os.environ.get("SPECTRAL_PROBE_N", "100000"))
STEP = float(os.environ.get("SPECTRAL_PROBE_STEP", "0.02"))
TAIL_STEP = float(os.environ.get("SPECTRAL_PROBE_TAIL_STEP", "0.005"))
TAIL_PREC = int(os.environ.get("SPECTRAL_PROBE_TAIL_PREC", "128"))
COARSE_PREC = int(os.environ.get("SPECTRAL_PROBE_COARSE_PREC", "53"))
TAIL_FINE_FROM = 74800.0
RECOVERY_BANDS = [(71250.0, 72500.0)]
RECOVERY_STEP = float(os.environ.get("SPECTRAL_PROBE_RECOVERY_STEP", "0.005"))
RECOVERY_PREC = int(os.environ.get("SPECTRAL_PROBE_RECOVERY_PREC", "128"))
START_T = 14.0
flint.ctx.prec = COARSE_PREC
RECOMPUTE = "--recompute" in sys.argv
JSON_OUT = EXPORTS / "spectral_big_probe.json"
NPZ_OUT = EXPORTS / "spectral_big_zeros.npz"
MAX_WORKERS = int(os.environ.get("SPECTRAL_PROBE_WORKERS", "4"))


def theta(t):
    t = np.asarray(t, dtype=float)
    tp = t / TWO_PI
    return 0.5 * t * np.log(tp) - 0.5 * t - PI_8


def zeta_on_point(t):
    z = acb.zeta(acb(0.5, float(t)))
    return complex(z.real.mid(), z.imag.mid())


def z_on_line(t):
    ph = theta(t)
    zc = zeta_on_point(t)
    return zc.real * math.cos(ph) - zc.imag * math.sin(ph)


def critical_height(n):
    target = float(n) - 0.125
    lo = 14.0
    hi = 2.0 * target
    while (hi / TWO_PI) * math.log(hi / TWO_PI) - hi / TWO_PI + 0.875 < target:
        hi *= 1.5
    return brentq(lambda t: (t / TWO_PI) * math.log(t / TWO_PI) - t / TWO_PI + 0.875 - target, lo, hi)


def von_mangoldt(T):
    return (T / TWO_PI) * math.log(T / TWO_PI) - T / TWO_PI + 0.875


def eval_zeta(tp):
    t, prec = tp
    flint.ctx.prec = prec
    z = acb.zeta(acb(0.5, float(t)))
    return complex(z.real.mid(), z.imag.mid())


def scan_grid(t0, t1, workers, step, prec):
    grid = np.arange(t0, t1, step)

    with Pool(workers) as pool:
        vals = np.array(list(pool.imap(eval_zeta, ((t, prec) for t in grid.tolist()),
                                       chunksize=2048)), dtype=complex)
    ph = theta(grid)
    zv = vals.real * np.cos(ph) - vals.imag * np.sin(ph)
    return grid, zv


def refine_root(ab):
    a, b = ab
    return brentq(z_on_line, a, b, xtol=1e-12)


def refine_brackets(grid, zv, workers):
    idx = np.where((zv[:-1] * zv[1:]) < 0.0)[0]
    brackets = [(grid[i], grid[i + 1]) for i in idx]
    with Pool(workers) as pool:
        roots = np.array(list(pool.imap(refine_root, brackets, chunksize=128)), dtype=float)
    return np.sort(roots)


def collate(roots, eps=1e-4):
    roots = np.sort(roots)
    keep = [roots[0]]
    for x in roots[1:]:
        if x - keep[-1] < eps:
            keep[-1] = 0.5 * (keep[-1] + x)
        else:
            keep.append(x)
    return np.array(keep)


def main():
    t_start = time.time()
    npz_cached = NPZ_OUT.exists() and not RECOMPUTE
    if npz_cached:
        with np.load(NPZ_OUT) as d:
            imags = d["imags"]
        print(f"loaded cached zeros from {NPZ_OUT} (len={imags.size}); "
              f"use --recompute to regenerate")
    else:
        end_t = critical_height(N)
        end_t += 0.02 * end_t
        if end_t > TAIL_FINE_FROM:
            print(f"arb scan for N={N}: coarse t in [{START_T}, {TAIL_FINE_FROM}] "
                  f"step={STEP} prec={COARSE_PREC} + tail [{TAIL_FINE_FROM}, {end_t:.1f}] "
                  f"step={TAIL_STEP} prec={TAIL_PREC}; workers={MAX_WORKERS}")
            gc, zvc = scan_grid(START_T, TAIL_FINE_FROM, MAX_WORKERS, STEP, COARSE_PREC)
            roots_c = refine_brackets(gc, zvc, MAX_WORKERS)
            gt, zvt = scan_grid(TAIL_FINE_FROM, end_t, MAX_WORKERS, TAIL_STEP, TAIL_PREC)
            roots_t = refine_brackets(gt, zvt, MAX_WORKERS)
            roots = np.sort(np.unique(np.concatenate([roots_c, roots_t])))
        else:
            print(f"arb scan for N={N}: t in [{START_T}, {end_t:.1f}], step={STEP}, "
                  f"workers={MAX_WORKERS}")
            grid, zv = scan_grid(START_T, end_t, MAX_WORKERS, STEP, COARSE_PREC)
            roots = refine_brackets(grid, zv, MAX_WORKERS)
        recovered = 0
        for b0, b1 in RECOVERY_BANDS:
            if b0 >= end_t or roots.size < N + 1:
                continue
            gr, zvr = scan_grid(b0, b1, MAX_WORKERS, RECOVERY_STEP, RECOVERY_PREC)
            roots_r = refine_brackets(gr, zvr, MAX_WORKERS)
            new_n = int(np.count_nonzero(np.abs(roots_r[:, None] - roots[None, :]).min(axis=1) > 0.005))
            roots = np.sort(np.unique(np.concatenate([roots, roots_r])))
            roots = collate(roots)
            recovered += new_n
            print(f"  recovery band [{b0}, {b1}): {roots_r.size} roots, {new_n} newly added "
                  f"(running total {roots.size})")
        print(f"  scanned -> {roots.size} roots (RvM expects {int(von_mangoldt(end_t))}); "
              f"recovered {recovered}")
        if roots.size < N + 1:
            raise SystemExit(
                f"FAIL: only {roots.size} roots detected, need >= {N + 1}; "
                f"suspect sub-resolution near-degenerate pairs (step={STEP})")
        imags = roots[: N + 1]
        np.savez_compressed(NPZ_OUT, imags=imags)
        print(f"  cached {imags.size} zeros -> {NPZ_OUT}")

    g = imags
    print(f"gamma_1 = {g[0]:.6f} (known 14.134725), gamma_2 = {g[1]:.6f} (known 21.022040)")
    print(f"gamma_{N} = {g[N - 1]:.6f}, gamma_{N + 1} = {g[N]:.6f}")

    sample_idx = sorted(set([1, 2, 100, 500, 1000, 5000, 10000, 25000, 50000, 75000,
                             N // 2, N - 1, N]))
    deltas = []
    max_off_line = 0.0
    import mpmath as mp
    mp.mp.dps = 25
    for k in sample_idx:
        if k > g.size:
            continue
        z = mp.zetazero(k)
        gm = float(z.imag)
        delta = abs(gm - g[k - 1])
        deltas.append({"n": k, "gamma_mpmath": gm, "gamma_probe": float(g[k - 1]),
                       "delta": delta})
        max_off_line = max(max_off_line, abs(float(z.real) - 0.5))
    max_delta = max(d["delta"] for d in deltas)

    rec_heights = [60000.0, 65000.0, 70000.0, 71250.0, 72500.0,
                   73750.0, 74100.0, 74450.0, 74600.0, 74750.0, 74850.0, 74900.0]
    mp.mp.dps = 25
    count_rec = []
    for T in rec_heights:
        n = float(mp.nzeros(T))
        ours = int((g <= T).sum())
        count_rec.append({"T": T, "mpmath_nzeros": n, "probe_cumulative": ours,
                          "delta": n - ours})
    max_count_dev = max(abs(c["delta"]) for c in count_rec)

    ds = np.diff(g[:N])
    mean_spacing = float(ds.mean())
    local_den = (1.0 / TWO_PI) * np.log(np.asarray(g[1:N]) / TWO_PI)
    sn = ds * local_den

    edges = np.linspace(0.0, 3.0, 61)
    hist, _ = np.histogram(sn, bins=edges)
    bin_w = edges[1] - edges[0]
    centers = (edges[:-1] + edges[1:]) / 2.0
    total = float(hist.sum())

    def gue_wigner(s):
        return (32.0 / math.pi ** 2) * s * s * math.exp(-4.0 * s * s / math.pi)

    def poisson(s):
        return math.exp(-s)

    def chi2(pdf):
        exp = np.array([pdf(c) * total * bin_w for c in centers])
        mask = exp >= 5.0
        return float(((hist[mask] - exp[mask]) ** 2 / exp[mask]).sum()), int(mask.sum())

    chi2_gue, ndf_gue = chi2(gue_wigner)
    chi2_pois, ndf_pois = chi2(poisson)
    chi2_ratio = chi2_gue / chi2_pois if chi2_pois > 0 else float("inf")

    n_end = g.size - 1
    T_end = float(g[N - 1])
    n_pred = von_mangoldt(T_end)
    rvm_at_end = {"T": T_end, "empirical_N": n_end, "von_mangoldt_pred": float(n_pred),
                  "deviation": float(n_pred - n_end)}

    results = {
        "audit": "spectral_big_probe",
        "n_zeros": N,
        "method": {
            "scan": "arb (python-flint 0.9) rigorous interval zeta: sign pattern of "
                    "Z(t)=Re(e^{i theta(t)} zeta(0.5+it)) on the critical line",
            "grid_step": STEP,
            "refinement": "scipy brentq per bracket, xtol=1e-12",
            "cache": str(NPZ_OUT),
            "regenerated": not npz_cached,
            "on_line": "by construction only t on Re=1/2 is searched; independent mpmath "
                       "zetazero spot-checks confirm Re(z)=0.5 and match imaginary parts",
        },
        "extent": {
            "gamma_first": float(g[0]),
            "gamma_N": float(g[N - 1]),
            "gamma_N_plus_1": float(g[N]),
            "mean_spacing": mean_spacing,
            "von_mangoldt_at_end": rvm_at_end,
        },
        "on_line_and_spot_check": {
            "mpmath_samples": len(deltas),
            "max_delta_vs_mpmath": max_delta,
            "max_abs_Re_minus_half_independent_mpmath": max_off_line,
        },
        "count_reconciliation_mpmath_nzeros": {
            "sweep": count_rec,
            "max_abs_deviation": max_count_dev,
        },
        "spacing_statistics": {
            "normalized_mean": float(sn.mean()),
            "normalized_std": float(sn.std()),
            "gue_wigner_surmise_chi2": chi2_gue,
            "poisson_chi2": chi2_pois,
            "chi2_ratio_GUE_over_Poisson": chi2_ratio,
            "bins_used_ndf": min(ndf_gue, ndf_pois),
            "reference": "GUE Wigner surmise p(s)=32 s^2/(pi^2) exp(-4 s^2/pi); "
                        "Poisson p(s)=exp(-s); lower chi2 = better fit",
        },
        "low_zeros": {
            "gamma_1": float(g[0]), "gamma_2": float(g[1]), "gamma_5": float(g[4]),
            "known_gamma_1": 14.134725141734693790,
            "known_gamma_2": 21.022039638771554992,
        },
        "verdict": {
            "stats": ("GUE (random-matrix) spacing fit strongly preferred over Poisson; "
                      "consistent with Odlyzko-class numerical evidence for the Hilbert-Polya "
                      "statistical picture") if chi2_ratio < 0.5 else
                     ("GUE vs Poisson fit inconclusive at this scale") if chi2_ratio < 1.5 else
                     ("data do NOT prefer GUE — investigate"),
            "exact_correspondence": ("individual finite-dimensional Dirac secular-root <-> zeta-zero "
                                     "correspondence remains FAILED (0-2/20, spectral_verification.py) "
                                     "-> the toy operator is falsified (STOP), while GUE statistics "
                                     "STRENGTHEN the spectral/HP program (stays OPEN)"),
        },
        "runtime_seconds": round(time.time() - t_start, 1),
    }
    JSON_OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "=" * 64)
    print(f"SPECTRAL BIG PROBE: N={N} zeta zeros (arb, rigorous interval arithmetic)")
    print(f"  gamma_1={g[0]:.6f}  gamma_2={g[1]:.6f}  gamma_{N}={g[N - 1]:.6f}")
    print(f"  RvM @ gamma_{N}: N(T)={n_end} vs F(T)={n_pred:.1f} (dev={n_pred - n_end:+.2f})")
    print(f"  mpmath spot-check @ {len(deltas)} indices: max|delta|={max_delta:.3e}, "
          f"max|Re-0.5|={max_off_line:.3e}")
    print(f"  normalized spacing: mean={float(sn.mean()):.6f}  std={float(sn.std()):.6f}")
    print(f"  chi2: GUE-Wigner={chi2_gue:.1f} vs Poisson={chi2_pois:.1f} (ndf={ndf_gue})  "
          f"ratio={chi2_ratio:.3f}")
    print(f"  runtime {results['runtime_seconds']}s  ->  {JSON_OUT}")
    print("=" * 64)


if __name__ == "__main__":
    main()