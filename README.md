# AetherZ3Omega — Riemann Hypothesis Formalization Workspace

[![GitHub Repo Size](https://img.shields.io/github/repo-size/aidilamrym-ops/riemann-hypothesis-formalization)](https://github.com/aidilamrym-ops/riemann-hypothesis-formalization)
[![GitHub](https://img.shields.io/github/license/aidilamrym-ops/riemann-hypothesis-formalization)](LICENSE)
[![Lean 4](https://img.shields.io/badge/Lean%204-blue.svg)](https://leanprover.github.io/)
[![Z3 SMT](https://img.shields.io/badge/SMT%20Z3-orange)](https://ericponvil.fr/z3-smt-solver/)

## Status (Honest, 2026-09-23)

- **Lean 4 corpus**: `lean4/AetherZ3Omega/Riemann/` — **66/66 modules** rebuilt individually from source
  via the Lean 4.33.1 kernel: **0 errors, 0 sorrys**, 1880 declarations scanned by the transpilation
  nexus from the live AST.
- **One open postulate**: `AetherZ3Omega.riemann_hypothesis` (in `RhCore.lean`). The Riemann
  Hypothesis is carried as a genuinely-open postulate — **no module claims a proof of RH**.
- **Kernel axiom audit** (`#print axioms` on flagship theorems): every declaration depends only on
  `[propext, Classical.choice, Quot.sound]` plus `riemann_hypothesis` for the RH-carrying chain.
  Full listing: `exports/_axioms.txt`; CI axiom sweep 857 "depends on axioms" lines.
- The spectral (Hilbert–Pólya) correspondence and RH itself remain **OPEN**.

## Grand Transpilation Nexus + Z3 Spectral Tribunal (2026-09-23)

- **`scripts/transpilation_nexus.py`** — reads the LIVE corpus AST (66 modules / 1880 decls), picks the
  flagship theorem by its **actually-present name** (`log_one_plus_lt` in `BarrierTheorem.lean`) and
  **refuses** to emit artifacts when the flagship is missing (exit 3, anti-cocoklogi gate). Generates
  4 backbone artifacts: **Dedukti** (λΠ-modulo), **Coq** (CIC), **Isabelle/HOL**, **CompCert Clight**,
  plus `flagship.txt` and `_transpilation_manifest.json`.
- **`scripts/z3_spectral_tribunal.py`** — real pyz3 5.0.0 spectral tribunal: F1/F2/F4 **UNSAT (NRA
  PROVEN)**, F3 honest **UNKNOWN** (transcendental `ln` deferred to the Lean kernel, never polished
  into SAT/UNSAT). Verdict JSON: `exports/z3_spectral_tribunal.json`.
- **CI**: job `transpile-nexus` in `.github/workflows/external-audit.yml` runs nexus `--assert` +
  tribunal `--assert` and uploads `exports/transpilation/**`. Last run (HEAD `8182808`): **success**.

## Repository Structure

```
FINAL_RH_PROJECT/
├── lean4/AetherZ3Omega/Riemann/     # Lean 4 formal proofs (62 modules, 0 sorry, 1 postulate)
│   ├── RhCore.lean                  # riemann_hypothesis postulate + derived lemmas
│   ├── BarrierTheorem.lean          # barrier rigidity (conditional on RH postulate)
│   ├── StressTest.lean              # epsilon rigidity stress test (conditional)
│   ├── Rigidity.lean / Obstruction.lean / CriticalLine.lean ...
│   └── ...
├── z3_tribunal/                     # Z3 SMT-LIB2 verification batches (1–17)
├── exports/                         # Verified status + publication artifacts
│   ├── FINAL_STATUS.md              # Final honest status report
│   ├── STATE.md                     # Build/module state
│   ├── VERIFICATION_STATUS.md       # Machine verification status
│   ├── AUDIT_HONESTY.md             # Honest audit of the proof chain
│   ├── HONESTY_LABELING.md          # Honest labeling of every module tier
│   ├── _axioms.txt                  # Kernel axiom audit listing
│   ├── research_paper.tex           # LaTeX manuscript
│   └── referensi.bib                # Bibliography
├── papers/                          # Dissertation + PaperA manuscript
├── scripts/                         # check_sorry.py, spectral_verification.py
└── lean_kernel_validator.sh         # Linux/Git-Bash kernel audit pipeline
```

## Verification Pipeline

### Lean 4 Kernel (Honest Scope)
1. Every module in `lean4/AetherZ3Omega/Riemann/` is kernel-compiled against real Mathlib oleans
   (Lean 4.33.1) — repeatable via `lean_kernel_validator.sh` (bash) or direct `lean -o`.
2. Axiom/sorry pollution audit with comments stripped (only real `sorry` tokens count → 0).
3. `#print axioms` kernel audit: exact axiom dependencies per flagship theorem
   (see `exports/_axioms.txt`).
4. Re-framed honestly: "master theorems" for BSD / Goldbach / Hodge / Poincaré / PvsNP /
   Yang-Mills are **conditional/consistency statements**, never proved resolutions.

### Z3 SMT Tribunal
- `z3_tribunal/*.py` runs SMT-LIB2 batches (1–17) checking algebraic/sat assertions.
- UNSAT results verify consistency of the asserted identities with the underlying SMT theory;
  they are auxiliary checks, not a replacement for the Lean kernel.

### Numerical Evidence
- `scripts/spectral_verification.py` and `scripts/real_computation_audit.py` reproduce the
  numerical claims (e.g. Berry-Keating heuristic ratio ≈ 0.979). Reported honestly:
  the Dirac finite-dim operator does **not** reproduce individual zeta zeros.

## Building & Verification

### Lean 4 verification
```bash
cd lean4/AetherZ3Omega/Riemann
# Requires Lean 4.33.1 + Mathlib v4.33.1
```
Fresh rebuild + axiom audit: see `lean_kernel_validator.sh` (Linux/Git-Bash) or the detailed
procedure documented in `exports/FINAL_STATUS.md`.

### Z3 Tribunal
```bash
cd z3_tribunal
python z3_verify_batch17_barrier.py
```

## Publication Artifacts

- **Status**: `exports/FINAL_STATUS.md`
- **Kernel audit**: `exports/_axioms.txt`
- **Manuscript**: `exports/research_paper.tex`
- **Dissertation**: `papers/riemann-hypothesis-skeleton_dissertation.{typ,pdf}`

## Citation

```bibtex
@misc{amry2026rh,
  title={AetherZ3Omega: Honest Formalization Workspace for the Riemann Hypothesis Skeleton},
  author={Muhammad Aidil Amry},
  year={2026},
  note={Lean 4 v4.33.1 kernel corpus: 62 modules, 0 sorry, 1 open postulate (RH). RH open.}
}
```

## License

MIT License — See LICENSE file.

## Contact

**Author**: Muhammad Aidil Amry (Sang Arsitek)
**ORCID**: 0009-0002-9718-9710
**Repository**: https://github.com/aidilamrym-ops/riemann-hypothesis-formalization