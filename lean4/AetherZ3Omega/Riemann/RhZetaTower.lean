/-
  RhZetaTower: MENARA FAKTA-ZETA TERBUKTI (0 aksioma kustom).

  Lawan untuk narasi "spectral rigidity barrier" korpus lama: di sini tidak ada
  postulat selain `RhCore.riemann_hypothesis` (definisi resmi Mathlib).
  Semua deklarasi pada file ini adalah TEOREMA TERBUKTI berdasarkan Mathlib
  v4.33.1 (`Mathlib.NumberTheory.LSeries.RiemannZeta`, `ZetaZeros`).

  Isi menara (semuanya dibuktikan dari Mathlib, bukan dari postulat):
    * nilai zeta di 0:    ζ(0) = -1/2, jadi 0 BUKAN nol
    * nol trivial:        ζ(-2(n+1)) = 0, dan semuanya JAUH dari garis kritis
    * representasi Dirichlet: untuk Re s > 1, ζ(s) = Σ 1 / n^s
    * persamaan fungsional (bentuk selesai/Λ): Λ(1-s) = Λ(s)
    * singularitas: kutub sederhana di s = 1 dengan residu 1
    * analitisitas: ζ analitik di ℂ \ {1}
    * himpunan nol: tertutup, diskrit, hingga-di-kompak

  Kesimpulan struktural: versi "barrier absolut" korpus lama (aksioma yang
  memaksa re(s) = 1/2 untuk SEMUA nol, trivial sekalipun) terbukti inkonsisten
  dengan Mathlib -- lihat `old_absolute_barrier_is_inconsistent`.
-/

import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.LSeries.ZetaZeros

import AetherZ3Omega.Riemann.RhCore

noncomputable section

open Complex Filter
open scoped Topology

namespace AetherZ3Omega

section ZetaValues

/-- Hasil resmi Mathlib: ζ(0) = -1/2. -/
theorem zeta_value_zero : riemannZeta 0 = -1 / 2 := riemannZeta_zero

/-- Konsekuensi: 0 BUKAN nol fungsi zeta. -/
theorem zero_is_not_zeta_zero : riemannZeta 0 ≠ 0 := by
  rw [riemannZeta_zero]
  norm_num

/-- Nol trivial: untuk setiap n >= 0, ζ(-2(n+1)) = 0. (Bukti Mathlib.) -/
theorem trivial_zeta_zero (n : ℕ) : riemannZeta (-2 * (n + 1) : ℂ) = 0 := by
  simpa using (riemannZeta_neg_two_mul_nat_add_one n : riemannZeta (-2 * (n + 1)) = 0)

/-- Semua nol trivial JAUH dari garis kritis: re = -2(n+1) ≠ 1/2.
  Akibatnya setiap pernyataan "E(ρ)=0 untuk SEMUA nol" (termasuk yang
  trivial) terbukti salah -- inilah vakuum korpus lama. -/
theorem trivial_zeros_off_critical_line (n : ℕ) :
    zetaEnergy (-2 * (n + 1) : ℂ) ≠ 0 := by
  unfold zetaEnergy
  rw [show ((-2 * (n + 1) : ℂ) : ℂ).re = -2 * (n + 1 : ℝ) by simp]
  intro h
  have h0 : (-2 * (n + 1 : ℝ) - 1 / 2) = 0 := sq_eq_zero_iff.mp h
  have hnn : (0 : ℝ) < (n + 1 : ℕ) := by exact_mod_cast (Nat.succ_pos n)
  nlinarith

end ZetaValues

section DirichletSeries

/-- Representasi Dirichlet zeta untuk Re s > 1 (bukti Mathlib).
  Catatan: formula ini TIDAK berlaku untuk Re s ≤ 1 -- di sanalah
  kelanjutan analitik (bukti Mathlib) mengambil alih. -/
theorem zeta_dirichlet_series (s : ℂ) (hs : (1 : ℝ) < s.re) :
    riemannZeta s = ∑' n : ℕ, 1 / (n : ℂ) ^ s :=
  zeta_eq_tsum_one_div_nat_cpow hs

end DirichletSeries

section FunctionalEquation

/-- Persamaan fungsional bentuk selesai `Λ(1 - s) = Λ(s)` (bukti Mathlib). -/
theorem completed_zeta_fun_eq (s : ℂ) :
    completedRiemannZeta (1 - s) = completedRiemannZeta s :=
  completedRiemannZeta_one_sub s

/-- Simetri nol `Λ`: nol dari fungsi zeta selesai simetris terhadap s ↦ 1-s,
  yang garis simetrinya justru garis kritis Re(s) = 1/2. -/
theorem completed_zeta_zero_neg_equiv (s : ℂ) :
    completedRiemannZeta (1 - s) = 0 ↔ completedRiemannZeta s = 0 := by
  rw [completed_zeta_fun_eq s]

end FunctionalEquation

section Analyticity

/-- ζ analitik pada ℂ \ {1} (bukti Mathlib). -/
theorem zeta_analytic_on_compl_one : AnalyticOnNhd ℂ riemannZeta ({1}ᶜ : Set ℂ) :=
  analyticOn_riemannZeta

/-- Singularitas di s = 1: kutub sederhana dengan residu 1 (bukti Mathlib). -/
theorem zeta_pole_residue_one :
    Tendsto (fun s : ℂ => (s - 1) * riemannZeta s) (𝓝[≠] 1) (𝓝 1) :=
  riemannZeta_residue_one

end Analyticity

section ZerosSet

/-- Himpunan nol zeta tertutup (Mathlib). -/
theorem zeta_zero_set_closed : IsClosed riemannZetaZeros :=
  isClosed_riemannZetaZeros

/-- Himpunan nol zeta diskrit (Mathlib; tidak ada titik akumulasi). -/
theorem zeta_zero_set_discrete : IsDiscrete riemannZetaZeros :=
  isDiscrete_riemannZetaZeros

/-- Hanya hingga banyak nol pada setiap himpunan kompak (Mathlib).
  Ini versi formal dari "untuk T hingga ada N(T) nol" tanpa memedarikan
  N(T) asimtotik Von Mangoldt yang tidak ada di Mathlib. -/
theorem zeta_zero_set_compact_finite {S : Set ℂ} (hS : IsCompact S) :
    (S ∩ riemannZetaZeros).Finite :=
  IsCompact.inter_riemannZetaZeros_finite hS

end ZerosSet

section BarrierVerdict

/-- INKONSISTENSI korpus lama (verdict final): aksioma absolut yang memaksa
  "∀ s, ζ(s) = 0 → re s = 1/2" (inti `log_bound_property`/`rigidity_equivalence`
  versi absolut, dan premis Z3 batch 10/14-17 yang kita temukan vakuum)
  BERTENTANGAN dengan fakta terbukti `riemannZeta (-4) = 0` dan `re (-4) = -4`.
  Dari satu aksioma itu, `False` DERIVABLE. -/
theorem old_absolute_barrier_is_inconsistent
    (h : ∀ s : ℂ, riemannZeta s = 0 → s.re = (1 / 2 : ℝ)) : False := by
  have hz : riemannZeta (-(2 * (1 + 1)) : ℂ) = 0 := by
    simpa using (riemannZeta_neg_two_mul_nat_add_one 1)
  have hre : (-(2 * (1 + 1)) : ℂ).re = (1 / 2 : ℝ) := h (-(2 * (1 + 1)) : ℂ) hz
  norm_num at hre

/-- Sebaliknya, postulat yang DIPERBAIKI (nol trivial dikecualikan, persis
  definisi Mathlib `RiemannHypothesis`) TIDAK bertabrakan dengan baris di
  atas: ketiadaan nol trivial yang dikesampingkan. Kita tidak dapat (dan tidak
  perlu) membuktikan `riemann_hypothesis`; itu masalah terbuka.
  Yang kita buktikan: struktur postulat benar secara tipe. -/
example : riemannZeta (-(2 * (1 + 1)) : ℂ) = 0 →
    (¬ ∃ n : ℕ, (-(2 * (1 + 1)) : ℂ) = -2 * (n + 1)) → False := by
  intro hz hnt
  apply hnt
  exact ⟨1, by norm_num⟩

end BarrierVerdict

end AetherZ3Omega