# Phase 2: Spectral Correspondence (The Almighty Bridge)
**Status**: PLANNING / PREPARATION
**Source**: ROADMAP.md (lines 10-13)

## Target
Formalisasi jembatan antara operator spektra diskrit (DiscreteOperator.lean) dengan nol-nol fungsi zeta Riemann, menuju konjektur Hilbert-Polya.

## Tugas Utama

### 1. Dirac Operator Convergence
**Tujuan**: Buktikan self-adjointness dari operator Dirac terdiskritisasi `D` dalam limit `P → ∞`.

**Langkah-langkah**:
1. Definisikan operator Dirac diskrit `D_P` pada ruang Hilbert berdimensi hingga `P`.
2. Buktikan `D_P` adalah Hermitian (self-adjoint) untuk setiap `P` terhingga.
3. Buktikan konvergensi `D_P → D_∞` dalam topologi resolvent / strong operator topology.
4. Buktikan `D_∞` adalah self-adjoint pada ruang Hilbert terpisah.
5. Hubungkan spektrum `D_∞` dengan nol-nol zeta (konjektur).

**Referensi**:
- Berry & Keating, "H = xp and the Riemann zeros" (1999)
- Connes, "Trace formula in noncommutative geometry..." (1999)
- Mathlib: `InnerProductSpace`, `SelfAdjoint`, `OperatorNorm`

### 2. Trace Formula Verification
**Tujuan**: Hubungkan trace formula Berry-Keating dengan konjektur Hilbert-Polya melalui lemma SMT terverifikasi.

**Langkah-langkah**:
1. Formalisasikan trace formula untuk operator diskrit `D_P`:
   `Tr(f(D_P)) = sum_{λ ∈ spec(D_P)} f(λ)`
2. Buktikan identitas trace untuk `P` terhingga menggunakan linear algebra (Mathlib).
3. Ambil limit `P → ∞` dan bandingkan dengan explicit formula Riemann-von Mangoldt:
   `∑_γ f(γ) = ...` (melibatkan Chebyshev function, nol zeta, dll.)
4. Gunakan Z3 Tribunal untuk memverifikasi identitas aljabar/aritmetika pada langkah diskrit.
5. Dokumentasikan gap analitik (limit `P → ∞`, kontinuitas spektrum) sebagai `sorry` terkontrol.

**Referensi**:
- Conrey, "The Riemann Hypothesis" (2003) - explicit formula
- Berry & Keating, "The Riemann zeros and eigenvalue asymptotics" (1999)
- Mathlib: `Matrix.trace`, `Finset.sum`, `Complex.zeta` (jika tersedia)

## Arsitektur Formalisasi (Lean 4)

### File Baru yang Dibutuhkan
```
rh_project/
├── DiracOperator.lean        # Definisi D_P, bukti Hermitian, konvergensi
├── TraceFormula.lean         # Trace formula diskrit, limit, kaitan explicit formula
├── SpectralTriple.lean       # Definisi spectral triple (A, H, D) untuk kasus diskrit
└── HilbertPolya.lean         # Konjektur Hilbert-Polya sebagai statement formal
```

### Dependensi Mathlib
- `Analysis.InnerProductSpace.Basic`
- `Analysis.OperatorNorm`
- `LinearAlgebra.Matrix.Hermitian`
- `LinearAlgebra.Matrix.Spectrum`
- `NumberTheory.ZetaFunction` (jika ada, atau formalisasi minimal sendiri)
- `Topology.MetricSpace.Basic` (untuk konvergensi resolvent)

### Integrasi Z3 Tribunal
- Setiap lemma aritmetika/aljabar dalam bukti diskrit dikirim ke Z3 untuk cross-verification.
- Gunakan `z3_tribunal_verify.py` untuk batch verification otomatis.
- Target: 100% UNSAT pada negasi lemma kunci.

## Rencana Eksekusi (Mingguan)

| Minggu | Fokus | Output |
|--------|-------|--------|
| 1 | Definisi `D_P` dan bukti `IsHermitian` untuk `P` terhingga | `DiracOperator.lean` (core lemmas, 0 sorry) |
| 2 | Konvergensi resolvent `D_P → D_∞` (statement + proof sketch) | `DiracOperator.lean` (konvergensi, dg `have`/`sorry`) |
| 3 | Trace formula diskrit untuk `D_P` | `TraceFormula.lean` (identitas trace, 0 sorry) |
| 4 | Limit trace formula & kaitan explicit formula (statement) | `TraceFormula.lean` (gap analitik terdokumentasi) |
| 5 | Z3 batch verification untuk semua lemma aritmetika | `verification_report_phase2.json` |
| 6 | Integrasi dengan `DiscreteOperator.lean` (Berry-Keating) | `SpectralTriple.lean` + `HilbertPolya.lean` |

## Gap yang Diketahui (Honest Disclosure)
1. **Analisis Fungsional Tak Hingga**: Limit `P → ∞` memerlukan teori operator tak hingga (belum sepenuhnya di Mathlib).
2. **Kontinuitas Spektrum**: Transisi dari spektrum diskrit ke kontinu (nol zeta) butuh argumen analitik kompleks.
3. **Explicit Formula**: Belum di Mathlib; perlu formalisasi minimal Chebyshev `ψ(x)` dan nol zeta.
4. **Hilbert-Polya**: Masih konjektur; formalisasi hanya sebagai statement kondisional.

## Next Immediate Action
1. Buat `DiracOperator.lean` dengan definisi `D_P` dan bukti `IsHermitian` (mirip `DiscreteOperator.lean`).
2. Buat `PHASE2_PLAN.md` ini di `rh_project/`.
3. Jalankan `lake build` untuk memastikan tidak ada regresi.

---
*Dibuat: 2026-09-07*
*Author: Sang Arsitek (Muhammad Aidil Amry)*