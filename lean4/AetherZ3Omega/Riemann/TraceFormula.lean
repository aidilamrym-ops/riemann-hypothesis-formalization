import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import AetherZ3Omega.Riemann.DiracOperator

namespace TraceFormula

open Matrix
open Finset

theorem kinetic_trace (N : ℕ) :
    (DiracOperator.diracKinetic N).trace = (N : ℝ) := by
  dsimp [DiracOperator.diracKinetic, Matrix.trace]
  simp [Matrix.vecMulVec_apply]

theorem fullDirac_trace_linear (N : ℕ) :
    (DiracOperator.fullDirac N).trace =
      (DiracOperator.diracDiagonal N).trace + (DiracOperator.diracKinetic N).trace := by
  dsimp [DiracOperator.fullDirac]
  exact Matrix.trace_add (DiracOperator.diracDiagonal N) (DiracOperator.diracKinetic N)

theorem diagonal_trace (N : ℕ) :
    (DiracOperator.diracDiagonal N).trace = (-(N : ℝ) / 2 : ℝ) := by
  rw [DiracOperator.diracDiagonal]
  rw [Matrix.trace_diagonal]
  have h2 : (Finset.sum (Finset.univ : Finset (Fin N)) (fun k : Fin N => (k : ℝ))) =
      (N : ℝ) * ((N : ℝ) - 1) / 2 := by
    rw [Fin.sum_univ_eq_sum_range (fun (k : ℕ) => (k : ℝ))]
    induction N with
    | zero => simp
    | succ N ih =>
      rw [Finset.sum_range_succ, ih]
      push_cast
      ring_nf
  have h3 : (Finset.sum (Finset.univ : Finset (Fin N)) (fun _ : Fin N => ((N : ℝ) / 2 : ℝ))) =
      (N : ℝ) * ((N : ℝ) / 2) := by
    simp [Finset.sum_const]
  calc
    (∑ i ∈ (Finset.univ : Finset (Fin N)), ((i : ℝ) - (N : ℝ) / 2 : ℝ)) =
        (∑ i ∈ (Finset.univ : Finset (Fin N)), (i : ℝ)) -
          (∑ i ∈ (Finset.univ : Finset (Fin N)), ((N : ℝ) / 2 : ℝ)) := by
      rw [Finset.sum_sub_distrib]
    _ = (N : ℝ) * ((N : ℝ) - 1) / 2 - (N : ℝ) * ((N : ℝ) / 2) := by
      rw [h2, h3]
    _ = -(N : ℝ) / 2 := by
      ring

theorem trace_scaled_dirac (N : ℕ) (c : ℝ) :
    (c • DiracOperator.fullDirac N).trace = c * (DiracOperator.fullDirac N).trace := by
  exact Matrix.trace_smul c (DiracOperator.fullDirac N)

end TraceFormula