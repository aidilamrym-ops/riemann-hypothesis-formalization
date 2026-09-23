import Mathlib

noncomputable section

open scoped BigOperators

/-!
Explicit real bounds for the Riemann zeta function on the half-line `(1, ∞)`,
proved in Lean against Mathlib 0df444a. Independent of any RH postulate.

Headline results (for `s ∈ ℝ`, `1 < s`, and `ε > 0` with `s = 1 + ε`):

  * `1 ≤ ζ(s) ≤ s / (s - 1)`        (the elementary integral-test bound)
  * equivalently `1 ≤ ζ(1+ε) ≤ (1+ε)/ε`
  * hence `0 < 1/ζ(s) ≤ 1`, i.e. `|1/ζ(1+ε)| ≤ 1`
-/

namespace ZetaBounds

/-- The real part of the zeta function, which is the real zeta value on `(1, ∞)`. -/
abbrev zetaRe (s : ℝ) : ℝ := (riemannZeta (s : ℂ)).re

lemma summable_nat_add_one_cpow {s : ℝ} (hs : 1 < s) :
    Summable (fun n : ℕ => 1 / (n + 1 : ℂ) ^ (s : ℂ)) := by
  have hsum0 : Summable (fun n : ℕ => 1 / (n : ℂ) ^ (s : ℂ)) := by
    rwa [Complex.summable_one_div_nat_cpow, Complex.ofReal_re]
  simpa using (summable_nat_add_iff 1).mpr hsum0

lemma summable_nat_add_one_rpow {s : ℝ} (hs : 1 < s) :
    Summable (fun n : ℕ => 1 / (n + 1 : ℝ) ^ s) := by
  have hsum0 : Summable (fun n : ℕ => 1 / (n : ℝ) ^ s) :=
    Real.summable_one_div_nat_rpow.mpr hs
  simpa using (summable_nat_add_iff 1).mpr hsum0

lemma zeta_tsum_re_id {s : ℝ} (hsum : Summable (fun n : ℕ => 1 / (n + 1 : ℂ) ^ (s : ℂ))) :
    (∑' n : ℕ, 1 / (n + 1 : ℂ) ^ (s : ℂ)).re = ∑' n : ℕ, 1 / (n + 1 : ℝ) ^ s := by
  calc
    (∑' n : ℕ, 1 / (n + 1 : ℂ) ^ (s : ℂ)).re
        = ∑' n : ℕ, (1 / (n + 1 : ℂ) ^ (s : ℂ)).re := by
          rw [Complex.re_tsum hsum]
    _ = ∑' n : ℕ, 1 / (n + 1 : ℝ) ^ s := by
          apply tsum_congr
          intro n
          have hn0 : 0 ≤ (n + 1 : ℝ) := by positivity
          have hcast' : (↑n : ℂ) + 1 = (((n + 1 : ℝ) : ℂ)) := by norm_num
          rw [hcast', ← Complex.ofReal_cpow hn0 s]
          simp

/-- The real zeta value equals the real Dirichlet series `∑ 1/(n+1)^s`. -/
lemma zeta_re_eq_tsum_add_one_rpow {s : ℝ} (hs : 1 < s) :
    zetaRe s = ∑' n : ℕ, 1 / (n + 1 : ℝ) ^ s := by
  have hs' : 1 < (s : ℂ).re := by simpa using hs
  unfold zetaRe
  rw [zeta_eq_tsum_one_div_nat_add_one_cpow (s := (s : ℂ)) hs']
  exact zeta_tsum_re_id (summable_nat_add_one_cpow hs)

/-- `ζ(s) ≥ 1` for `1 < s`. -/
lemma one_le_zeta_re {s : ℝ} (hs : 1 < s) : 1 ≤ zetaRe s := by
  rw [zeta_re_eq_tsum_add_one_rpow hs]
  have hsum1 : Summable (fun n : ℕ => 1 / (n + 1 : ℝ) ^ s) := summable_nat_add_one_rpow hs
  have hdecomp : (∑' n : ℕ, 1 / (n + 1 : ℝ) ^ s) = 1 + ∑' n : ℕ, 1 / (n + 2 : ℝ) ^ s := by
    rw [Summable.tsum_eq_zero_add hsum1]
    norm_num
    congr 1
    funext n
    apply congrArg (fun x : ℝ => (x ^ s)⁻¹)
    ring
  rw [hdecomp]
  have hrest : 0 ≤ ∑' n : ℕ, 1 / (n + 2 : ℝ) ^ s := tsum_nonneg (fun n => by positivity)
  linarith

/-- `ζ(s) ≤ s/(s-1)` for `1 < s` (elementary integral-test bound). -/
lemma zeta_le_s_div_sub_one {s : ℝ} (hs : 1 < s) : zetaRe s ≤ s / (s - 1) := by
  rw [zeta_re_eq_tsum_add_one_rpow hs]
  have hts : 0 ≤ ZetaAsymptotics.termTSum s :=
    tsum_nonneg (fun n => ZetaAsymptotics.term_nonneg (n + 1) s)
  have hline : 1 - s * ZetaAsymptotics.termTSum s ≤ 1 := by
    linarith [mul_nonneg (by linarith : 0 ≤ s) hts]
  have hsub :
      (∑' n : ℕ, 1 / (n + 1 : ℝ) ^ s) - 1 / (s - 1) ≤ 1 := by
    rw [ZetaAsymptotics.zeta_limit_aux1 hs]
    exact hline
  have h : (∑' n : ℕ, 1 / (n + 1 : ℝ) ^ s) ≤ 1 + 1 / (s - 1) := by
    linarith
  have hid : 1 + 1 / (s - 1) = s / (s - 1) := by
    field_simp [show (s - 1 : ℝ) ≠ 0 by linarith]
    ring
  simpa using h.trans_eq hid

/-- `ζ(s) > 0` for `1 < s`. -/
lemma zeta_re_pos {s : ℝ} (hs : 1 < s) : 0 < zetaRe s := riemannZeta_re_pos_of_one_lt hs

/-- `1/ζ(s) ≤ 1` for `1 < s`. -/
lemma inv_zeta_re_le_one {s : ℝ} (hs : 1 < s) : (zetaRe s)⁻¹ ≤ 1 := by
  have h1 : 1 ≤ zetaRe s := one_le_zeta_re hs
  exact inv_le_one_of_one_le₀ h1

/-- Epsilon form of the upper bound: `ζ(1+ε) ≤ (1+ε)/ε`. -/
lemma zeta_eps_le {ε : ℝ} (hε : 0 < ε) : zetaRe (1 + ε) ≤ (1 + ε) / ε := by
  have hs : 1 < 1 + ε := by linarith
  calc
    zetaRe (1 + ε) ≤ (1 + ε) / ((1 + ε) - 1) := zeta_le_s_div_sub_one hs
    _ = (1 + ε) / ε := by ring_nf

/-- Epsilon form of the lower bound: `1 ≤ ζ(1+ε)`. -/
lemma one_le_zeta_eps {ε : ℝ} (hε : 0 < ε) : 1 ≤ zetaRe (1 + ε) :=
  one_le_zeta_re (by linarith : 1 < 1 + ε)

/-- `|1/ζ(1+ε)| ≤ 1`. -/
lemma abs_inv_zeta_eps_le_one {ε : ℝ} (hε : 0 < ε) : |(1 / zetaRe (1 + ε))| ≤ 1 := by
  have hs : 1 < 1 + ε := by linarith
  have hpos : 0 < (1 / zetaRe (1 + ε)) := by
    exact one_div_pos.mpr (zeta_re_pos hs)
  rw [abs_of_pos hpos]
  simpa using (inv_zeta_re_le_one hs)

end ZetaBounds

end