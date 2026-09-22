; Z3 Cross-Verification: ZetaBasic.lean theorems
; Translated from Lean 4 kernel-verified theorems to SMT-LIB2
; Logic: QF_NRA (Quantifier-Free Nonlinear Real Arithmetic)

(set-logic QF_NRA)
(set-option :produce-models true)

; --- Theorem 1: th_critical_line_half ---
; Original: theorem th_critical_line_half (s : ℝ) (h : s = 0.5) : s ≤ 1 ∧ s ≥ 0
(declare-fun s () Real)
(assert (= s 0.5))
(assert (not (and (<= s 1) (>= s 0))))
(check-sat)
(get-model)
; Expected: unsat (negation is unsatisfiable, so original holds)

; --- Theorem 2: th_deviation_bound ---
; Original: theorem th_deviation_bound (delta : ℝ) (h_pos : delta > 0) : 0.5 + delta ≠ 0.5
(declare-fun delta () Real)
(assert (> delta 0))
(assert (= (+ 0.5 delta) 0.5))
(check-sat)
; Expected: unsat

; --- Theorem 3: th_potential_wall_barrier ---
; Original: theorem th_potential_wall_barrier (V : ℝ) (h_barrier : V ≥ 1000000) : V > 0
(declare-fun V () Real)
(assert (>= V 1000000))
(assert (not (> V 0)))
(check-sat)
; Expected: unsat

; --- Theorem 4: th_swarm_energy_nonneg ---
; Original: theorem th_swarm_energy_nonneg (E : ℝ) (h : E ≥ 0) : E^2 ≥ 0
(declare-fun E () Real)
(assert (>= E 0))
(assert (not (>= (* E E) 0)))
(check-sat)
; Expected: unsat

; --- Theorem 5: th_hamiltonian_bound ---
; Original: theorem th_hamiltonian_bound (p q : ℝ) : p * q ≤ (p^2 + q^2) / 2
(declare-fun p () Real)
(declare-fun q () Real)
(assert (not (<= (* p q) (/ (+ (* p p) (* q q)) 2))))
(check-sat)
; Expected: unsat

(exit)