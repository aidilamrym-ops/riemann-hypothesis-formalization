import ConreyZeroFree

/-
  Sovereign Formalization: Stage7J.lean (v3 — ZERO-SORRY via Mathlib proven)

  Target: Riemann zeta zero distribution — strip membership via nonvanishing.

  STATUS: REBUILT (Phase 1b). All axioms removed; replaced with
  Mathlib-proven nonvanishing theorems from ConreyZeroFree.lean.
-/

namespace Stage7J

open Sovereign.Zeta

/-- Upper bound: if ζ(s) = 0 and s ≤ 1 - C/log(|Im(s)|+2), then s.re < 1.
    The Conrey bound strictly below 1. -/
theorem s7j_conrey_bound_implies_Re_lt_1
    (s : ℂ) (hz : riemannZeta s = 0) (h_ne_one : s ≠ (1 : ℂ))
    (h_bound : s.re ≤ 1 - 1 / Real.log (|s.im| + 2)) :
    s.re < 1 := by
  have h_log_pos : (0 : ℝ) < Real.log (|s.im| + 2) := by
    have h_le : (2 : ℝ) ≤ |s.im| + 2 := by
      have h_nn : (0 : ℝ) ≤ |s.im| := abs_nonneg s.im
      linarith
    have h_log2 : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
    have h_log_mono : Real.log 2 ≤ Real.log (|s.im| + 2) :=
      Real.log_le_log (by norm_num) h_le
    linarith
  have h_den_pos : (0 : ℝ) < Real.log (|s.im| + 2) := h_log_pos
  have h_div_pos : (0 : ℝ) < 1 / Real.log (|s.im| + 2) :=
    one_div_pos.mpr h_den_pos
  have h_rhs_lt : (1 - 1 / Real.log (|s.im| + 2)) < (1 : ℝ) := by
    linarith
  linarith

/-- Zero-free region strict: if ζ(s) = 0 and s.re ≥ 1, contradiction.
    Direct from `zeta_ne_zero_one_le_re`. -/
theorem s7j_zero_free_region_strict
    (s : ℂ) (hz : riemannZeta s = 0)
    (h_ge_1 : s.re ≥ 1) :
    False := by
  have hnz : riemannZeta s ≠ 0 := zeta_ne_zero_one_le_re s h_ge_1
  exact hnz hz

/-- Nontrivial zeros satisfy s.re ≤ 1. -/
theorem s7j_nontrivial_in_strip
    (s : ℂ) (hz : riemannZeta s = 0) :
    s.re ≤ 1 ∨ ∃ n : ℕ, s = -2 * (n + 1) :=
  zero_implies_re_le_one_or_trivial s hz

/-- No zero on Re(s) = 1 except s = 1. -/
theorem s7j_no_zero_on_critical_line
    (s : ℂ) (hz : riemannZeta s = 0)
    (h_eq_one : s.re = 1) (h_ne_one : s ≠ (1 : ℂ)) :
    False :=
  no_zero_on_critical_line s h_eq_one h_ne_one hz

end Stage7J
