import Mathlib.Analysis.InnerProductSpace.Basic

-- === STAGE 7O: Z3 SMT VERIFICATION LAYER (HARDENED - BATCH 2) ===
namespace Stage7OHardened

-- QF_LRA: Quantifier-Free Linear Real Arithmetic
theorem o1_add_le_cancel_left (a b c : ℝ) : a + c ≤ b + c ↔ a ≤ b := by
  constructor <;> intro h <;> linarith

theorem o2_mul_le_pos (a b : ℝ) (h : 0 ≤ a) (h₂ : a ≤ b) : a^2 ≤ a*b := by
  nlinarith [sq_nonneg a]

theorem o3_mul_ge_zero (a : ℝ) (ha : 0 ≤ a) : a^2 ≥ 0 := sq_nonneg a

theorem o4_sq_ge_one (a : ℝ) (h : a ≥ 1) : a^2 ≥ 1 := by
  have : a^2 - 1 = (a - 1) * (a + 1) := by ring
  nlinarith [sq_nonneg (a-1), h]

theorem o6_sq_ge_sq_of_ge (a b : ℝ) (h : 0 ≤ a ∧ a ≤ b) : a^2 ≤ b^2 := by
  rw [sq_le_sq]
  rw [abs_of_nonneg h.1, abs_of_nonneg (le_trans h.1 h.2)]
  exact h.2

theorem o9_pos_mul_pos (a b : ℝ) (ha : 0 < a) (hb : 0 < b) : 0 < a * b := mul_pos ha hb

theorem o13_div_le_of_le (a b c : ℝ) (h1 : a ≤ b) (h2 : 0 < c) : a / c ≤ b / c := (div_le_div_iff_of_pos_right h2).mpr h1

theorem o23_sq_lt_sq (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) : a^2 < b^2 ↔ a < b := by
  rw [sq_lt_sq, abs_of_nonneg ha, abs_of_nonneg hb]

theorem o26_max_le_iff (a b c : ℝ) : max a b ≤ c ↔ a ≤ c ∧ b ≤ c := max_le_iff

theorem o27_le_min_iff (a b c : ℝ) : c ≤ min a b ↔ c ≤ a ∧ c ≤ b := le_min_iff

theorem o41_max_le_max (a b c d : ℝ) (h1 : a ≤ c) (h2 : b ≤ d) : max a b ≤ max c d := max_le_max h1 h2

theorem o42_min_le_min (a b c d : ℝ) (h1 : a ≤ c) (h2 : b ≤ d) : min a b ≤ min c d := min_le_min h1 h2

theorem o47_max_add_distrib (a b c : ℝ) : max a b + c = max (a + c) (b + c) := by
  by_cases h : a ≤ b
  · rw [max_eq_right h]
    symm
    simpa [add_comm, add_left_comm, add_assoc] using max_eq_right (add_le_add_right h c)
  · have hba : b ≤ a := le_of_not_ge h
    rw [max_eq_left hba]
    symm
    simpa [add_comm, add_left_comm, add_assoc] using max_eq_left (add_le_add_right hba c)

theorem o48_min_add_distrib (a b c : ℝ) : min a b + c = min (a + c) (b + c) := by
  by_cases h : a ≤ b
  · rw [min_eq_left h]
    symm
    simpa [add_comm, add_left_comm, add_assoc] using min_eq_left (add_le_add_right h c)
  · have hba : b ≤ a := le_of_not_ge h
    rw [min_eq_right hba]
    symm
    simpa [add_comm, add_left_comm, add_assoc] using min_eq_right (add_le_add_right hba c)

end Stage7OHardened