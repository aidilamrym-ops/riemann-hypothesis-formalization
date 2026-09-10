# Milestone (b) — DiscreteOperator Retrospective

Author: Sovereign Engine / Muhammad Aidil Amry
Date: 2026-09-02
Status: ABORTED per Law of the Guillotine

---

## Attempted (b) — Self-adjointness Diskrit

The original plan: formalize a concrete Hermitian (self-adjoint) matrix as
a stepping stone toward the Hilbert-Polya operator. Specific deliverables:

1. Define `discreteLaplacian` (tridiagonal matrix, A[i,i]=2, A[i,i±1]=-1)
2. Define `berryKeatingCandidate` (rank-1 outer product A[i,j] = (i-N/2)·(j-N/2))
3. Prove `IsSymm` and `IsHermitian` for both
4. Apply Gershgorin to obtain spectrum bounds
5. Conjecture (numerical) that eigenvalues approximate zeta zeros

## Why we aborted

While implementing the `discreteLaplacian_isSymm` proof, I hit a barrier
that revealed a deeper methodological problem:

The proof required extensive case-splitting (i = j, j = i+1, j = i-1, etc.)
over a definition using `if-then-else` with Fin indices. Each case
required careful omega/arithmetic reasoning, and after multiple iterations
the proof was still failing with "Tactic `simp` made no progress" or
"Application type mismatch" errors.

This is exactly the failure mode the user warned about:
"hati-hati jangan sampai terjebak looping tak ter無限" (be careful not to get
trapped in an infinite loop).

Honest assessment: I was looping. Each fix revealed a new subproblem, and
the proof was drifting away from the conceptual contribution (the Hilbert-
Polya idea) toward pure Lean 4 syntactic wrestling.

## What I learned

1. The `Matrix.IsSymm.ext_iff` lemma requires unpacking the matrix entry
   function. For `Matrix.of fun i j => if-then-else`, this forces case
   analysis that the linear arithmetic tactics handle poorly.
2. Mathlib's `Matrix.isHermitian_iff_isSymm` works for real matrices
   (since ℝ has `TrivialStar`), so the Hermitian claim is automatic once
   IsSymm is proven — but that one step is the bottleneck.
3. For an honest exit, better to use a *structurally* symmetric matrix
   (rank-1 outer product, where symmetry is immediate from ring
   commutativity) than to fight the tridiagonal case analysis.

## What would have worked (in retrospect)

A cleaner approach:
- Use `Matrix.vecMulVec` (outer product) directly; symmetry is `ring`
  (one tactic).
- For the tridiagonal Laplacian, use `Matrix.diagonal` + a separate
  `offDiagonal` matrix and rely on the `add` / `smul` closure of
  `IsHermitian` already proven in Mathlib.

## What was actually committed

Nothing on the formal side. The "milestone (b)" produced no
verifiable theorem. The `DiscreteOperator.lean` file was deleted.

The honest record of state: Milestone (a) remains the last successfully
formalized chunk.

## Decision: do not retry

The user explicitly warned: "hati-hati jangan sampai terjebak looping
tak terhingga". Per the Law of the Guillotine, when a proof attempt
loops and the incremental value of each iteration is negative, stop.

## Recommendation for any future attempt

1. Use `Matrix.vecMulVec` (outer product) or `Matrix.diagonal` — both
   have trivial IsSymm proofs via `ring`.
2. For the tridiagonal Laplacian, first add a private lemma
   `offDiagonal_isSymm` (proven with `simp + omega`) before composing
   via `IsHermitian.add`.
3. Build incrementally, verifying after each lemma — do not attempt the
   full case-split in one tactic block.

End of retrospective.