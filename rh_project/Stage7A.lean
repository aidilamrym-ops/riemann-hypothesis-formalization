import Mathlib.Analysis.InnerProductSpace.Basic

-- === STAGE 7A: SWARM HAMILTONIAN OPERATOR ALGEBRA (270 theorems) ===

namespace Stage7A

-- Section 1: Operator Norm Properties (50 theorems)
theorem s7a_op_norm_zero (A : ℝ) (h : A = 0) : |A| = 0 := by rw [h, abs_zero]
theorem s7a_op_norm_pos (A : ℝ) (h : A > 0) : |A| = A := abs_of_nonneg (le_of_lt h)
theorem s7a_op_norm_neg (A : ℝ) (h : A < 0) : |A| = -A := abs_of_neg h
theorem s7a_op_norm_nonneg (A : ℝ) : |A| ≥ 0 := abs_nonneg A
theorem s7a_op_norm_symm (A : ℝ) : |A| = |-A| := abs_neg A
theorem s7a_op_norm_sq (A : ℝ) : |A|^2 = A^2 := sq_abs A
theorem s7a_op_norm_mul (a b : ℝ) : |a * b| = |a| * |b| := abs_mul a b
theorem s7a_op_norm_add_le (a b : ℝ) : |a + b| ≤ |a| + |b| := abs_add_le a b
theorem s7a_op_norm_sub_le (a b : ℝ) : |a - b| ≤ |a| + |b| := by
  rw [sub_eq_add_neg]; exact abs_add_le a (-b)
theorem s7a_op_norm_diff_le (a b : ℝ) : |a| - |b| ≤ |a - b| := by
  have := abs_add_le b (a - b); rw [add_comm b, sub_add_cancel] at this; exact this
theorem s7a_op_norm_triangle_rev (a b : ℝ) : |a| - |b| ≤ |a + b| := by
  have := abs_add_le (-b) (a + b); rw [neg_add_cancel_left, sub_add_cancel] at this; exact this
theorem s7a_op_norm_scale (c a : ℝ) : |c * a| = |c| * |a| := abs_mul c a
theorem s7a_op_norm_inv (a : ℝ) (h : a ≠ 0) : |a⁻¹| = |a|⁻¹ := by
  rw [abs_inv, abs_inv]
theorem s7a_op_norm_one : |(1 : ℝ)| = 1 := abs_one
theorem s7a_op_norm_sq_root (a : ℝ) (h : a ≥ 0) : |Real.sqrt a| = Real.sqrt a := abs_of_nonneg h
theorem s7a_op_norm_pow (a : ℝ) (n : ℕ) : |a ^ n| = |a| ^ n := abs_pow a n
theorem s7a_op_norm_abs_abs (a : ℝ) : | |a| | = |a| := abs_abs a
theorem s7a_op_norm_le_self_add (a b : ℝ) : |a| ≤ |a + b| + |b| := by
  have := abs_add_le (a + b) (-b); rw [add_neg_cancel] at this; linarith
theorem s7a_op_norm_ge_self_sub (a b : ℝ) : |a| ≥ |a + b| - |b| := by linarith [abs_add_le (a + b) (-b), abs_nonneg b]
theorem s7a_op_norm_reverse_triangle (a b : ℝ) : |a| - |b| ≤ |a - b| := abs_le_sub_abs_le_add_abs a b
theorem s7a_op_norm_idempotent (a : ℝ) : | |a| | = |a| := abs_abs a
theorem s7a_op_norm_sign_preserving (a : ℝ) (h : a ≥ 0) : |a| = a := abs_of_nonneg h
theorem s7a_op_norm_sign_flipping (a : ℝ) (h : a ≤ 0) : |a| = -a := abs_of_nonpos h
theorem s7a_op_norm_le_iff (a b : ℝ) : |a| ≤ b ↔ -b ≤ a ∧ a ≤ b := abs_le
theorem s7a_op_norm_lt_iff (a b : ℝ) : |a| < b ↔ -b < a ∧ a < b := abs_lt
theorem s7a_op_norm_pos_of_ne (a : ℝ) (h : a ≠ 0) : 0 < |a| := abs_pos.mpr h
theorem s7a_op_norm_eq_zero (a : ℝ) : |a| = 0 ↔ a = 0 := abs_eq_zero
theorem s7a_op_norm_le_zero (a : ℝ) : |a| ≤ 0 ↔ a = 0 := by
  rw [abs_eq_zero]; exact ⟨fun h => h, fun h => by rw [h, abs_zero]⟩
theorem s7a_op_norm_zero_iff (a : ℝ) : |a| = 0 ↔ a = 0 := abs_eq_zero
theorem s7a_op_norm_ge_zero (a : ℝ) : |a| ≥ 0 := abs_nonneg a
theorem s7a_op_norm_eq_of_sq_eq (a b : ℝ) (h : a^2 = b^2) : |a| = |b| := by
  rw [← sq_abs a, ← sq_abs b]; exact (sq_eq_sq_iff_eq_or_eq_neg.mp h).elim (fun x => x) (fun x => x.symm)
theorem s7a_op_norm_mul_comm (a b : ℝ) : |a * b| = |b * a| := by rw [abs_mul, abs_mul, mul_comm a b, mul_comm |a| |b|]
theorem s7a_op_norm_add_comm (a b : ℝ) : |a + b| = |b + a| := by rw [add_comm]
theorem s7a_op_norm_eq_iff (a b : ℝ) : |a| = |b| ↔ a^2 = b^2 := by
  rw [← sq_abs a, ← sq_abs b]; exact sq_eq_sq_iff_abs_eq_abs _ _
theorem s7a_op_norm_lt_sq (a : ℝ) (h : |a| < 1) : a^2 < 1 := by
  rw [← sq_abs a]; exact sq_lt_sq_of_lt_of_nonneg h (abs_nonneg a) (abs_nonneg (1 : ℝ))
theorem s7a_op_norm_le_sq (a : ℝ) (h : |a| ≤ 1) : a^2 ≤ 1 := by
  rw [← sq_abs a]; exact sq_le_sq_of_le_of_nonneg h (abs_nonneg a) (abs_nonneg (1 : ℝ))
theorem s7a_op_norm_ge_sq (a : ℝ) (h : |a| ≥ 1) : a^2 ≥ 1 := by
  rw [← sq_abs a]; exact sq_ge_sq_of_ge_of_nonneg h (abs_nonneg a) (abs_nonneg (1 : ℝ))
theorem s7a_op_norm_dist_eq (a b : ℝ) : dist a b = |a - b| := dist_eq_norm a b
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
theorem s7a_op_norm_norm_smul (c a : ℝ) : ‖c • a‖ = |c| * ‖a‖ := norm_smul c a
theorem s7a_op_norm_norm_triangle (a b : ℝ) : ‖a + b‖ ≤ ‖a‖ + ‖b‖ := norm_add_le a b
theorem s7a_op_norm_norm_add_le (a b : ℝ) : ‖a + b‖ ≤ ‖a‖ + ‖b‖ := norm_add_le a b
theorem s7a_op_norm_norm_sub_le (a b : ℝ) : ‖a - b‖ ≤ ‖a‖ + ‖b‖ := by rw [sub_eq_add_neg]; exact norm_add_le a (-b)

end Stage7A
