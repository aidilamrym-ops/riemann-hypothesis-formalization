import Mathlib

noncomputable section

/-!
Kernel-selection independence for the Euler-product kernel factors.

The Z3 tribunal batches 7 and 8 encoded the Euler product kernel factor claims

  * `s > 1 ⊢ 1 - 2^(-s) > 0`   (batch7, `euler_factor_pos`)
  * `s > 1 ⊢ 1 - 2^(-s) < 1`   (batch7, `euler_factor_lt1`)
  * `p ≥ 2, s > 1 ⊢ 0 < 1 - p^(-s) < 1`  (batch7, `euler_factor_in_unit`)
  * `p ≥ 2, s > 1 ⊢ 1 - p^(-s) ≠ 0`  (batch8, `euler_factor_nonzero`)
  * `p ≥ 2, s > 1 ⊢ 0 < 1 - p^(-s)`   (batch8, `euler_factor_unit_interval`)

All five came back `unknown` because `p^(-s)` is a real power with a
symbolic exponent, i.e. outside QF_NRA (nonlinear transcendental NFE).
This module proves those claims **universally** — for every admissible
kernel parameter `(p, s)` with `p ≥ 2`, `s > 1` — so the Z3 results do not
depend on the bounded sample instances `(2 ≤ p < 10, 1 < s < 10)` they
were instantiated with.  The theorems close all five UNKNOWN verdicts.

Corollary of the same fact used by the kernel analysis itself: the
renormalisation factor `(1 - p^(-s))⁻¹ = Σ p^(-ns)` is `> 1`, so the Euler
product is genuinely "amplifying" (its partial log-sums are positive).
-/

namespace KernelIndependence

/-- `0 < p^(-s) < 1` for every admissible kernel parameter `(p, s)`. -/
lemma rpow_neg_unit_interval {p s : ℝ} (hp : 2 ≤ p) (hs : 1 < s) :
    0 < p ^ (-s) ∧ p ^ (-s) < 1 := by
  have hp0 : 0 < p := by linarith
  have h2s : 1 < (2 : ℝ) ^ s := Real.one_lt_rpow (by norm_num) (by linarith : 0 < s)
  have h2le : (2 : ℝ) ^ s ≤ p ^ s := by
    exact Real.rpow_le_rpow (by norm_num : 0 ≤ (2 : ℝ)) (by linarith : (2 : ℝ) ≤ p)
      (by linarith : 0 ≤ s)
  have hps_gt_one : 1 < p ^ s := lt_of_lt_of_le h2s h2le
  have hps_pos : 0 < p ^ s := by linarith
  have hpos : 0 < p ^ (-s) := by
    rw [Real.rpow_neg hp0.le]
    exact inv_pos.mpr hps_pos
  have hlt : p ^ (-s) < 1 := by
    rw [Real.rpow_neg hp0.le]
    exact inv_lt_one_of_one_lt₀ hps_gt_one
  exact ⟨hpos, hlt⟩

/-- `1 - p^(-s) > 0` for every admissible kernel parameter. (batch8 `euler_factor_unit_interval`) -/
lemma euler_factor_pos {p s : ℝ} (hp : 2 ≤ p) (hs : 1 < s) : 0 < 1 - p ^ (-s) :=
  sub_pos.mpr (rpow_neg_unit_interval hp hs).2

/-- `1 - p^(-s) < 1` for every admissible kernel parameter. (batch7 `euler_factor_lt1`) -/
lemma euler_factor_lt_one {p s : ℝ} (hp : 2 ≤ p) (hs : 1 < s) : 1 - p ^ (-s) < 1 := by
  have hpos : 0 < p ^ (-s) := (rpow_neg_unit_interval hp hs).1
  linarith

/-- `0 < 1 - p^(-s) < 1`, the unit-interval kernel factor. (batch7 `euler_factor_in_unit`) -/
lemma euler_factor_unit_interval {p s : ℝ} (hp : 2 ≤ p) (hs : 1 < s) :
    0 < 1 - p ^ (-s) ∧ 1 - p ^ (-s) < 1 :=
  ⟨euler_factor_pos hp hs, euler_factor_lt_one hp hs⟩

/-- `1 - p^(-s) ≠ 0` for every admissible kernel parameter. (batch8 `euler_factor_nonzero`) -/
lemma euler_factor_ne_zero {p s : ℝ} (hp : 2 ≤ p) (hs : 1 < s) : 1 - p ^ (-s) ≠ 0 :=
  ne_of_gt (euler_factor_pos hp hs)

/-- The renormalisation factor `(1 - p^(-s))⁻¹` exceeds 1, so each kernel
factor has a well-defined `> 1` reciprocal (geometric-series start). -/
lemma euler_renorm_factor_gt_one {p s : ℝ} (hp : 2 ≤ p) (hs : 1 < s) :
    1 < (1 - p ^ (-s))⁻¹ := by
  have hpos : 0 < 1 - p ^ (-s) := euler_factor_pos hp hs
  have hlt : 1 - p ^ (-s) < 1 := euler_factor_lt_one hp hs
  exact (one_lt_inv₀ hpos).mpr hlt

/-- Base `p = 2` specialisations of the exact batch7 statements. -/
lemma euler_factor_pos_base_two {s : ℝ} (hs : 1 < s) : 0 < 1 - (2 : ℝ) ^ (-s) :=
  euler_factor_pos (p := (2 : ℝ)) (s := s) (by norm_num) hs

/-- Base `p = 2` specialisations of the exact batch7 statements. -/
lemma euler_factor_lt_one_base_two {s : ℝ} (hs : 1 < s) : 1 - (2 : ℝ) ^ (-s) < 1 :=
  euler_factor_lt_one (p := (2 : ℝ)) (s := s) (by norm_num) hs

end KernelIndependence

end