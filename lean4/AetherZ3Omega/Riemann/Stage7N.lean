import Mathlib.Analysis.InnerProductSpace.Basic

-- === STAGE 7N: Z3 SMT VERIFICATION LAYER (HARDENED) ===
namespace Stage7NHardened

theorem n1_sq_nonneg (x : ℝ) : 0 ≤ x^2 := sq_nonneg x
theorem n2_abs_nonneg (x : ℝ) : 0 ≤ |x| := abs_nonneg x
theorem n3_abs_le_add (a b : ℝ) : |a + b| ≤ |a| + |b| := abs_add_le a b
theorem n4_abs_sub_le (a b : ℝ) : |(|a| - |b|)| ≤ |a - b| := by
  rw [abs_le]
  constructor
  · have h := abs_sub_abs_le_abs_sub b a
    rw [abs_sub_comm] at h
    linarith
  · exact abs_sub_abs_le_abs_sub a b
theorem n5_abs_mul (a b : ℝ) : |a * b| = |a| * |b| := abs_mul a b
theorem n6_abs_neg (a : ℝ) : |-a| = |a| := abs_neg a
theorem n7_abs_pos_of_ne (a : ℝ) (h : a ≠ 0) : 0 < |a| := abs_pos.mpr h
theorem n8_abs_lt_iff (a b : ℝ) : |a| < b ↔ -b < a ∧ a < b := abs_lt
theorem n9_abs_le_iff (a b : ℝ) : |a| ≤ b ↔ -b ≤ a ∧ a ≤ b := abs_le
theorem n10_abs_sq (a : ℝ) : |a|^2 = a^2 := sq_abs a

theorem n21_sq_nonneg_sum (a b : ℝ) : 0 ≤ a^2 + b^2 := by
  have ha : 0 ≤ a^2 := sq_nonneg a
  have hb : 0 ≤ b^2 := sq_nonneg b
  linarith

theorem n23_am_gm_2 (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) : 2*a*b ≤ a^2 + b^2 := by
  have : 0 ≤ (a - b)^2 := sq_nonneg (a - b)
  nlinarith

theorem n24_cauchy_2d (a b c d : ℝ) : (a*c + b*d)^2 ≤ (a^2 + b^2)*(c^2 + d^2) := by
  have : 0 ≤ (a*d - b*c)^2 := sq_nonneg (a*d - b*c)
  nlinarith

theorem n25_young (a b : ℝ) : a*b ≤ a^2/2 + b^2/2 := by
  have h : 2 * a * b ≤ a^2 + b^2 := by nlinarith [sq_nonneg (a - b)]
  field_simp [show (2 : ℝ) ≠ 0 by norm_num]
  nlinarith

theorem n26_triangle_sq (a b : ℝ) : (a + b)^2 ≤ 2*(a^2 + b^2) := by
  have : 0 ≤ (a - b)^2 := sq_nonneg (a - b)
  nlinarith

theorem n27_diff_sq (a b : ℝ) : a^2 - b^2 = (a+b)*(a-b) := by ring
theorem n28_sum_sq (a b : ℝ) : (a+b)^2 = a^2 + 2*a*b + b^2 := by ring
theorem n29_diff_sq_2 (a b : ℝ) : (a-b)^2 = a^2 - 2*a*b + b^2 := by ring

end Stage7NHardened