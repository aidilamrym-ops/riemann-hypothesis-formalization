import Mathlib

noncomputable section

namespace HardyZetaPositive

/-- The point `s = 1/2 + i·t` on the critical line `Re s = 1/2`. -/
abbrev criticalLine (t : ℝ) : ℂ := ((1 / 2 : ℝ) : ℂ) + Complex.I * t

/-- `criticalLine` is continuous as a function `ℝ → ℂ`. -/
lemma continuous_criticalLine : Continuous criticalLine := by
  fun_prop

/-- `criticalLine` is injective: different imaginary heights give different points. -/
lemma criticalLine_injective : Function.Injective criticalLine := by
  intro t u h
  have ht : (criticalLine t).im = t := by simp [criticalLine]
  have hu : (criticalLine u).im = u := by simp [criticalLine]
  simpa [ht, hu] using congrArg Complex.im h

/--
The zeros of ζ on the critical line with imaginary part in a bounded band
`[a, b]` form a **finite** set. This is the discreteness of `riemannZetaZeros`
(`IsCompact.inter_riemannZetaZeros_finite`) pulled back through `criticalLine`.
-/
theorem criticalLine_zero_finite_Icc (a b : ℝ) (_hab : a ≤ b) :
    {t : ℝ | t ∈ Set.Icc a b ∧ riemannZeta (criticalLine t) = 0}.Finite := by
  classical
  let f : ℝ → ℂ := fun t : ℝ => criticalLine t
  let S : Set ℂ := f '' Set.Icc a b
  have hS : IsCompact S := by
    exact (isCompact_Icc.image continuous_criticalLine)
  have hfin : (S ∩ riemannZetaZeros).Finite := hS.inter_riemannZetaZeros_finite
  have hfinPre : (f ⁻¹' (S ∩ riemannZetaZeros)).Finite :=
    hfin.preimage criticalLine_injective.injOn
  have hEq : f ⁻¹' (S ∩ riemannZetaZeros) =
      {t : ℝ | t ∈ Set.Icc a b ∧ riemannZeta (criticalLine t) = 0} := by
    ext t
    constructor
    · intro h
      rcases h with ⟨ht, hz⟩
      rcases ht with ⟨u, hu, hueq⟩
      have hut : u = t := criticalLine_injective hueq
      refine ⟨by simpa [hut] using hu, ?_⟩
      exact (mem_riemannZetaZeros.mp hz)
    · intro h
      constructor
      · exact ⟨t, h.1, rfl⟩
      · exact mem_riemannZetaZeros.mpr h.2
  simpa [hEq, f] using hfinPre

/-- Zero count on the critical line below height `T` is well defined (finite). -/
theorem criticalLine_zero_finite_below_height (T : ℝ) (hT : 0 ≤ T) :
    {t : ℝ | t ∈ Set.Icc 0 T ∧ riemannZeta (criticalLine t) = 0}.Finite :=
  criticalLine_zero_finite_Icc 0 T hT

/--
On every nonempty open real interval `(a, b)`, there is an imaginary height
`t` with `ζ(1/2 + i·t) ≠ 0`. The zero set on the critical line is "thin":
it contains no interval at all.
-/
theorem exists_zeroFree_on_criticalLine_Ioo (a b : ℝ) (hab : a < b) :
    ∃ t, t ∈ Set.Ioo a b ∧ riemannZeta (criticalLine t) ≠ 0 := by
  by_contra h
  have hZero : ∀ t, t ∈ Set.Ioo a b → riemannZeta (criticalLine t) = 0 := by
    intro t ht
    by_contra hnz
    exact h ⟨t, ht, hnz⟩
  have hFinBand : {t : ℝ | t ∈ Set.Icc a b ∧ riemannZeta (criticalLine t) = 0}.Finite :=
    criticalLine_zero_finite_Icc a b (le_of_lt hab)
  have hSub : (Set.Ioo a b : Set ℝ) ⊆
      {t : ℝ | t ∈ Set.Icc a b ∧ riemannZeta (criticalLine t) = 0} := by
    intro t ht
    exact ⟨⟨le_of_lt ht.1, le_of_lt ht.2⟩, hZero t ht⟩
  have hFin : (Set.Ioo a b : Set ℝ).Finite := hFinBand.subset hSub
  exact (Set.Ioo_infinite hab) hFin

/--
There are **infinitely many** imaginary heights `t` with `ζ(1/2 + i·t) ≠ 0`.
Together with Hardy's theorem (infinitely many zeros do lie on the critical
line), this shows the zeros on the critical line form an exceptional, thin
set: at every height band there are plenty of zero-free points, so a rising
proportion `N₀(T)/N(T)` is compatible with the line being generically
zero-free (zeros are isolated, never "covering" an interval).
-/
theorem infinite_zeroFree_heights_on_criticalLine :
    {t : ℝ | riemannZeta (criticalLine t) ≠ 0}.Infinite := by
  classical
  by_contra hInf
  have hFin : ({t : ℝ | riemannZeta (criticalLine t) ≠ 0} : Set ℝ).Finite := by
    exact Set.not_infinite.mp hInf
  rcases hFin.bddAbove with ⟨B, hB⟩
  rcases exists_zeroFree_on_criticalLine_Ioo B (B + 1) (by linarith) with ⟨t, ht, htz⟩
  have htB : t ≤ B := hB htz
  exact (not_lt_of_ge htB) ht.1

/-- Any compact subset of the plane contains only finitely many zeros of ζ. -/
theorem finite_zetaZeros_on_compact (K : Set ℂ) (hK : IsCompact K) :
    (K ∩ riemannZetaZeros).Finite :=
  hK.inter_riemannZetaZeros_finite

/-- The zero set of ζ is a discrete subset of ℂ. -/
theorem isDiscrete_riemannZetaZeros : IsDiscrete riemannZetaZeros :=
  _root_.isDiscrete_riemannZetaZeros

/-- No zero of ζ lies in the closed half-plane `Re s ≥ 1` (zero-free region). -/
theorem zeroSet_disjoint_halfPlane_geOne :
    riemannZetaZeros ∩ {s : ℂ | 1 ≤ s.re} = ∅ := by
  ext s
  constructor
  · intro h
    rcases h with ⟨hz, hre⟩
    exact False.elim (riemannZeta_ne_zero_of_one_le_re hre (mem_riemannZetaZeros.mp hz))
  · intro h
    simp at h

end HardyZetaPositive