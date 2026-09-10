import Almighty.Core
import Mathlib.NumberTheory.Prime
import Mathlib.NumberTheory.ArithmeticFunction

namespace Almighty.Goldbach

/-- Bounded Goldbach verification: every even n ≤ bound is sum of two primes -/
theorem goldbach_bounded (n : ℕ) (hn : n ≥ 4 ∧ n % 2 = 0) (hbound : n ≤ 200000) :
    ∃ p q : ℕ, Nat.Prime p ∧ Nat.Prime q ∧ p + q = n := by
  have h_main : ∃ p q : ℕ, Nat.Prime p ∧ Nat.Prime q ∧ p + q = n := by
    have h : n ≤ 200000 := hbound
    interval_cases n <;> norm_num [Nat.Prime] <;>
      (try decide) <;>
      (try {
        use 2, n - 2
        <;> norm_num [Nat.Prime] <;>
        (try decide)
      })
  exact h_main

end Almighty.Goldbach