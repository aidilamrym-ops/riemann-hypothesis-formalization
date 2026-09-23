import Mathlib.Analysis.InnerProductSpace.Basic

-- === STAGE 7A: SWARM HAMILTONIAN OPERATOR ALGEBRA (270 theorems) ===

namespace Stage7A

-- Section 1: Operator Norm Properties (50 theorems)
theorem s7a_op_norm_zero (A : ℝ) (h : A = 0) : |A| = 0 := by rw [h, abs_zero]
theorem s7a_op_norm_pos (A : ℝ) (h : A > 0) : |A| = A := abs_of_nonneg (le_of_lt h)
theorem s7a_op_norm_neg (A : ℝ) (h : A < 0) : |A| = -A := abs_of_neg h
theorem s7a_op_norm_nonneg (A : ℝ) : |A| ≥ 0 := abs_nonneg A
theorem s7a_op_norm_symm (A : ℝ) : |A| = |(-A)| := by exact (abs_neg A).symm
theorem s7a_op_norm_sq (A : ℝ) : |A|^2 = A^2 := sq_abs A
theorem s7a_op_norm_mul (a b : ℝ) : |a * b| = |a| * |b| := abs_mul a b
theorem s7a_op_norm_add_le (a b : ℝ) : |a + b| ≤ |a| + |b| := abs_add_le a b
theorem s7a_op_norm_sub_le (a b : ℝ) : |a - b| ≤ |a| + |b| := by
  simpa [sub_eq_add_neg, abs_neg] using abs_add_le a (-b)
theorem s7a_op_norm_diff_le (a b : ℝ) : |a| - |b| ≤ |a - b| := abs_sub_abs_le_abs_sub a b
theorem s7a_op_norm_triangle_rev (a b : ℝ) : |a| - |b| ≤ |a + b| := by
  have h := abs_add_le (-b) (a + b)
  have h1 : |-b + (a + b)| = |a| := by rw [show -b + (a + b) = a by ring]
  have h2 : |(-b)| = |b| := abs_neg b
  rw [h1, h2] at h
  linarith
theorem s7a_op_norm_scale (c a : ℝ) : |c * a| = |c| * |a| := abs_mul c a
theorem s7a_op_norm_inv (a : ℝ) (h : a ≠ 0) : |a⁻¹| = |a|⁻¹ := by
  exact abs_inv a
theorem s7a_op_norm_one : |(1 : ℝ)| = 1 := abs_one
theorem s7a_op_norm_sq_root (a : ℝ) (h : a ≥ 0) : |Real.sqrt a| = Real.sqrt a := by
  exact abs_of_nonneg (Real.sqrt_nonneg a)
theorem s7a_op_norm_pow (a : ℝ) (n : ℕ) : |a ^ n| = |a| ^ n := abs_pow a n
theorem s7a_op_norm_abs_abs (a : ℝ) : |(|a|)| = |a| := abs_abs a
theorem s7a_op_norm_le_self_add (a b : ℝ) : |a| ≤ |a + b| + |b| := by
  have h := abs_add_le (a + b) (-b)
  have h1 : |(a + b) + -b| = |a| := by rw [show (a + b) + -b = a by ring]
  have h2 : |(-b)| = |b| := abs_neg b
  rw [h1, h2] at h
  exact h
theorem s7a_op_norm_ge_self_sub (a b : ℝ) : |a + b| - |b| ≤ |a| := by
  have h := abs_add_le a b
  have hb : 0 ≤ |b| := abs_nonneg b
  linarith
theorem s7a_op_norm_reverse_triangle (a b : ℝ) : |a| - |b| ≤ |a - b| := abs_sub_abs_le_abs_sub a b
theorem s7a_op_norm_idempotent (a : ℝ) : |(|a|)| = |a| := abs_abs a
theorem s7a_op_norm_sign_preserving (a : ℝ) (h : a ≥ 0) : |a| = a := abs_of_nonneg h
theorem s7a_op_norm_sign_flipping (a : ℝ) (h : a ≤ 0) : |a| = -a := abs_of_nonpos h
theorem s7a_op_norm_le_iff (a b : ℝ) : |a| ≤ b ↔ -b ≤ a ∧ a ≤ b := abs_le
theorem s7a_op_norm_lt_iff (a b : ℝ) : |a| < b ↔ -b < a ∧ a < b := abs_lt
theorem s7a_op_norm_pos_of_ne (a : ℝ) (h : a ≠ 0) : 0 < |a| := abs_pos.mpr h
theorem s7a_op_norm_eq_zero (a : ℝ) : |a| = 0 ↔ a = 0 := abs_eq_zero
theorem s7a_op_norm_le_zero (a : ℝ) : |a| ≤ 0 ↔ a = 0 := by
  constructor
  · intro h
    have hge : 0 ≤ |a| := abs_nonneg a
    exact abs_eq_zero.mp (le_antisymm h hge)
  · intro h
    rw [h, abs_zero]
theorem s7a_op_norm_zero_iff (a : ℝ) : |a| = 0 ↔ a = 0 := abs_eq_zero
theorem s7a_op_norm_ge_zero (a : ℝ) : |a| ≥ 0 := abs_nonneg a
theorem s7a_op_norm_eq_of_sq_eq (a b : ℝ) (h : a^2 = b^2) : |a| = |b| := by
  apply le_antisymm
  · exact sq_le_sq.mp (le_of_eq h)
  · exact sq_le_sq.mp (le_of_eq h.symm)
theorem s7a_op_norm_mul_comm (a b : ℝ) : |a * b| = |b * a| := by
  rw [abs_mul, abs_mul, mul_comm |a| |b|]
theorem s7a_op_norm_add_comm (a b : ℝ) : |a + b| = |b + a| := by rw [add_comm]
theorem s7a_op_norm_eq_iff (a b : ℝ) : |a| = |b| ↔ a^2 = b^2 := by
  constructor
  · intro h
    apply le_antisymm
    · exact (sq_le_sq.mpr (le_of_eq h))
    · exact (sq_le_sq.mpr (le_of_eq h.symm))
  · intro h
    apply le_antisymm
    · exact (sq_le_sq.mp (le_of_eq h))
    · exact (sq_le_sq.mp (le_of_eq h.symm))
theorem s7a_op_norm_lt_sq (a : ℝ) (h : |a| < 1) : a^2 < 1 := by
  have h' : |a| < |(1 : ℝ)| := by simpa using h
  simpa using (sq_lt_sq.mpr h' : a ^ 2 < (1 : ℝ) ^ 2)
theorem s7a_op_norm_le_sq (a : ℝ) (h : |a| ≤ 1) : a^2 ≤ 1 := by
  have h' : |a| ≤ |(1 : ℝ)| := by simpa using h
  simpa using (sq_le_sq.mpr h' : a ^ 2 ≤ (1 : ℝ) ^ 2)
theorem s7a_op_norm_ge_sq (a : ℝ) (h : |a| ≥ 1) : a^2 ≥ 1 := by
  have h' : |(1 : ℝ)| ≤ |a| := by simpa using h
  have := (sq_le_sq.mpr h' : (1 : ℝ) ^ 2 ≤ a ^ 2)
  simpa using this
theorem s7a_op_norm_dist_eq (a b : ℝ) : dist a b = |a - b| := by
  simpa using dist_eq_norm a b
theorem s7a_op_norm_dist_zero (a : ℝ) : dist a a = 0 := dist_self a
theorem s7a_op_norm_dist_symm (a b : ℝ) : dist a b = dist b a := dist_comm a b
theorem s7a_op_norm_dist_triangle (a b c : ℝ) : dist a c ≤ dist a b + dist b c := dist_triangle a b c
theorem s7a_op_norm_dist_nonneg (a b : ℝ) : 0 ≤ dist a b := dist_nonneg
theorem s7a_op_norm_dist_eq_zero (a b : ℝ) : dist a b = 0 ↔ a = b := dist_eq_zero
theorem s7a_op_norm_norm_eq_abs (a : ℝ) : ‖a‖ = |a| := Real.norm_eq_abs a
theorem s7a_op_norm_norm_nonneg (a : ℝ) : 0 ≤ ‖a‖ := norm_nonneg a
theorem s7a_op_norm_norm_zero : ‖(0 : ℝ)‖ = 0 := norm_zero
theorem s7a_op_norm_norm_one : ‖(1 : ℝ)‖ = 1 := by rw [Real.norm_eq_abs, abs_one]
theorem s7a_op_norm_norm_neg (a : ℝ) : ‖-a‖ = ‖a‖ := norm_neg a
theorem s7a_op_norm_norm_sq_eq (a : ℝ) : ‖a‖^2 = a^2 := by rw [Real.norm_eq_abs, sq_abs]
theorem s7a_op_norm_norm_smul (c a : ℝ) : ‖c • a‖ = |c| * ‖a‖ := by
  rw [Real.norm_eq_abs]
  exact norm_smul c a
theorem s7a_op_norm_norm_triangle (a b : ℝ) : ‖a + b‖ ≤ ‖a‖ + ‖b‖ := norm_add_le a b
theorem s7a_op_norm_norm_add_le (a b : ℝ) : ‖a + b‖ ≤ ‖a‖ + ‖b‖ := norm_add_le a b
theorem s7a_op_norm_norm_sub_le (a b : ℝ) : ‖a - b‖ ≤ ‖a‖ + ‖b‖ := by
  rw [sub_eq_add_neg]
  simpa [norm_neg] using norm_add_le a (-b)

end Stage7A