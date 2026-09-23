import Mathlib

/-!
Formal bounds for the Montgomery–Taylor constant c₁* of the Anthropic zeta-23 paper
(`comparator/ChallengeDeps.lean` §3). We prove, using Mathlib alone:

  cMT = √2·tan(1/√2) / (1 + (1/√2)·tan(1/√2))   satisfies   2/3 < cMT < 4/5,

from which the three Theorem-D proportions are all strictly positive (non-vacuous):
  2 − 1/c₁* > 1/2,   2c₁* − 1 > 1/3,   c₁* > 2/3.
-/

noncomputable section

def x : ℝ := 1 / Real.sqrt 2
def f (u : ℝ) : ℝ := Real.sqrt 2 * u / (1 + x * u)
def cMT : ℝ := f (Real.tan x)

namespace CMT

lemma x_pos : 0 < x := by
  dsimp [x]
  positivity

lemma sqrt2_pos : (0 : ℝ) < Real.sqrt 2 := by positivity

lemma x_lt_one : x < 1 := by
  dsimp [x]
  have hs : (1 : ℝ) < Real.sqrt 2 :=
    (Real.lt_sqrt (by norm_num : (0 : ℝ) ≤ 1)).mpr (by norm_num)
  exact (div_lt_iff₀ sqrt2_pos).2 (by simpa using hs)

lemma x_lt_pi_div_two : x < Real.pi / 2 := by
  have hp : (2 : ℝ) < Real.pi := by nlinarith [Real.pi_gt_three]
  have h1 : (1 : ℝ) < Real.pi / 2 :=
    (lt_div_iff₀ (by norm_num : (0 : ℝ) < 2)).2 (by simpa using hp)
  exact x_lt_one.trans h1

lemma tan_gt_x : x < Real.tan x := Real.lt_tan x_pos x_lt_pi_div_two

lemma tan_pos : (0 : ℝ) < Real.tan x := lt_trans x_pos tan_gt_x

lemma x_sq : x ^ 2 = 1 / 2 := by
  dsimp [x]
  have hsq : (Real.sqrt 2 : ℝ) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  rw [div_pow, hsq]
  norm_num

lemma cos_ge_three_fourths : (3 / 4 : ℝ) ≤ Real.cos x := by
  have hle : 1 - x ^ 2 / 2 ≤ Real.cos x := Real.one_sub_sq_div_two_le_cos
  rw [x_sq] at hle
  nlinarith

lemma cos_pos : (0 : ℝ) < Real.cos x := lt_of_lt_of_le (by norm_num) cos_ge_three_fourths

lemma tan_le_four_thirds_mul_x : Real.tan x ≤ 4 / 3 * x := by
  rw [Real.tan_eq_sin_div_cos]
  have hsin : Real.sin x ≤ x := Real.sin_le x_pos.le
  have hfrac1 : Real.sin x / Real.cos x ≤ x / Real.cos x :=
    div_le_div_of_nonneg_right hsin (le_of_lt cos_pos)
  have hfrac2 : x / Real.cos x ≤ 4 / 3 * x := by
    rw [div_le_iff₀ cos_pos]
    have hmul : (3 / 4 : ℝ) * x ≤ Real.cos x * x :=
      mul_le_mul_of_nonneg_right cos_ge_three_fourths x_pos.le
    nlinarith
  exact hfrac1.trans hfrac2

lemma f_mono {u v : ℝ} (hu_pos : 0 < u) (huv : u ≤ v) : f u ≤ f v := by
  dsimp [f]
  have hdu : (0 : ℝ) < 1 + x * u := by nlinarith [x_pos, hu_pos]
  have hdv : (0 : ℝ) < 1 + x * v := by nlinarith [x_pos, hu_pos, huv]
  rw [div_le_div_iff₀ hdu hdv]
  nlinarith [sqrt2_pos, huv]

lemma f_lt {u v : ℝ} (hu_pos : 0 < u) (huv : u < v) : f u < f v := by
  dsimp [f]
  have hdu : (0 : ℝ) < 1 + x * u := by nlinarith [x_pos, hu_pos]
  have hdv : (0 : ℝ) < 1 + x * v := by nlinarith [x_pos, hu_pos, huv]
  rw [div_lt_div_iff₀ hdu hdv]
  nlinarith [sqrt2_pos, huv]

lemma f_x_eq : f x = 2 / 3 := by
  dsimp [f, x]
  have hsq : (Real.sqrt 2 : ℝ) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  field_simp [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ Real.sqrt 2)]
  nlinarith [hsq]

lemma f_43x_eq : f (4 / 3 * x) = 4 / 5 := by
  dsimp [f, x]
  have hsq : (Real.sqrt 2 : ℝ) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  field_simp [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ Real.sqrt 2)]
  nlinarith [hsq]

lemma cMT_gt_two_thirds : (2 / 3 : ℝ) < cMT := by
  rw [cMT, ← f_x_eq]
  exact f_lt (u := x) (v := Real.tan x) x_pos tan_gt_x

lemma cMT_le_four_fifths : cMT ≤ 4 / 5 := by
  rw [cMT, ← f_43x_eq]
  exact f_mono (u := Real.tan x) (v := 4 / 3 * x) tan_pos tan_le_four_thirds_mul_x

lemma cMT_pos : (0 : ℝ) < cMT := lt_trans (by norm_num) cMT_gt_two_thirds

lemma cMT_lt_one : cMT < 1 := cMT_le_four_fifths.trans_lt (by norm_num)

lemma cMT_ne_zero : cMT ≠ 0 := ne_of_gt cMT_pos

lemma inv_cMT_lt_three_halves : cMT⁻¹ < 3 / 2 := by
  have h : (1 / cMT : ℝ) < 3 / 2 := by
    rw [div_lt_iff₀ cMT_pos]
    nlinarith [cMT_gt_two_thirds]
  simpa using h

lemma prop_two_minus_inv_cMT_gt : 2 - 1 / cMT > (1 / 2 : ℝ) := by
  have h : cMT⁻¹ < 3 / 2 := inv_cMT_lt_three_halves
  rw [one_div]
  nlinarith [h]

lemma prop_two_mul_cMT_minus_one_gt : 2 * cMT - 1 > (1 / 3 : ℝ) := by
  nlinarith [cMT_gt_two_thirds]

lemma cMT_prop_gt : cMT > (2 / 3 : ℝ) := cMT_gt_two_thirds

end CMT

end

#check CMT.cMT_gt_two_thirds
#check CMT.cMT_le_four_fifths
#check CMT.cMT_pos
#check CMT.cMT_lt_one
#check CMT.prop_two_minus_inv_cMT_gt
#check CMT.prop_two_mul_cMT_minus_one_gt