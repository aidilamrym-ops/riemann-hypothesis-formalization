# Zenodo Deposit Package

## Metadata
- **Title**: Sovereign Deterministic Verification of Foundational Lemmas for the Millennium Problems
- **Upload type**: preprint
- **Publication date**: 2026-08-28
- **License**: MIT
- **Access**: Open
- **Keywords**: Riemann Hypothesis, Lean 4, Z3 SMT, Formal Verification, Millennium Problems, Chebyshev bounds, Functional equation
- **Creator**: Amry, Muhammad Aidil (Omega Cyber Guard / AETHER-Z3-OMEGA)

## Files to Upload (in `D:\WORKSPACE\VAULT\rh_project_backup_20260827\`)

### Core Manuscript
- `PaperA_Millennium_Verification.tex` — Main preprint source
- `PaperA_Millennium_Verification.pdf` — Compiled PDF

### Lean 4 Source (proofs)
- `ZetaFunctional.lean` — Zeta functional equation symmetry (5 theorems)
- `ChebyshevFormal.lean` — Chebyshev prime bounds (3 theorems)
- `PrimeDistributionBounds.lean` — Von Mangoldt proxy (2 theorems)
- `CriticalZeroSpacing.lean` — Critical line zero spacing (5 theorems)
- `ConreyZeroFree.lean` — Conrey zero-free region (5 axioms + 2 theorems)

### Lean 4 Build Infrastructure
- `lakefile.toml` — Lean 4 build configuration
- `lean-toolchain` — Lean 4 version pin

### Z3 SMT Tribunal
- `z3_tribunal_verify.py` — Cross-verification script (74 assertions)
- `zeta_basic_smt.smt2` — SMT-LIB2 constraint file
- `Z3_CROSS_VERIFICATION_REPORT.md` — Verification report

### Project Documentation
- `README.md` — Project README
- `CITATION.cff` — Citation file
- `LICENSE.md` — MIT License

## Submission Checklist

- [ ] Login ke https://zenodo.org menggunakan akun yang memiliki token
- [ ] Klik **Upload** → **New Upload**
- [ ] Copy-paste isi `zenodo_metadata.json` ke form
- [ ] Drag-and-drop 14 file di atas ke zona upload
- [ ] Review metadata → klik **Save** (jangan Publish dulu)
- [ ] Verifikasi DOI Draft sudah tergenerate
- [ ] (Optional) klik **Publish** untuk mengunci DOI permanen
- [ ] Catat DOI di `STATE.md` dan `brain.db`
