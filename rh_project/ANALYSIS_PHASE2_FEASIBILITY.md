# ANALYSIS: Phase 2 Feasibility — Conrey Bound & Spectral Correspondence
Author: Muhammad Aidil Amry (Sang Arsitek) + Sovereign Engine
Date: 2026-09-02
Status: DIRECTIVE — Milestone (a) real theorems, Phase 2 deferred

---

## 1. Q1: Conrey-Vinogradov bound — limitation of community, not pipeline

### Honest split (two layers)

1. **Old claims = OUR problem (fixed).** `ConreyZeroFree.lean` v4 carried
   `h_bound : s.re ≤ 1 - C/log(|Im(s)|+2)` as a *hypothesis* while its header
   claimed "zero-sorry" — yet real axioms + `sorry` were present
   (recorded in `AUDIT_HONESTY.md` as "TIDAK JUJUR").
   Phase 1b removed the fake claim and replaced it with a Mathlib-proven theorem.

2. **Current gap = SHARED community frontier, not a workflow bug.**
   Mathlib v4.33.1 contains the PNT-strength nonvanishing
   (`riemannZeta_ne_zero_of_one_le_re`, Stoll-Loeffler 2024) but NOT
   the explicit Conrey-Vinogradov zero-free region.

### Why the Conrey bound is not in Mathlib yet
- It is research-grade analytic number theory:
  - quantitative control of ζ′/ζ and log ζ
  - Dirichlet polynomials + Vinogradov mean value estimates
  - Trudgian–Kadiri explicit constants
- **No human has formalized it in Lean as of v4.33.1.** Even Euler product,
  functional equation, and PNT-strength nonvanishing only landed in Mathlib
  2024–2025 (Michael Stoll, David Loeffler).
- Formalizing it ourselves = independent multi-month research project for an
  analytic-NT + Lean expert. Not an overnight fix.

### Verdict
Gap = state of the art of formal mathematics (shared with all Lean users).
Two options:
  (a) accept PNT-strength scope (DONE in Phase 1b), or
  (b) launch original research formalization of Conrey bound (separate project).

---

## 2. Q2: Phase 2 (spectral correspondence) is heavier AND riskier

### Phase 1 = reuse, low risk
All hard mathematics already done by Mathlib community. Our work = correct
imports, assembling corollaries, deleting fake axioms. One session.

### Phase 2 as written in ROADMAP = original research + dangerous pattern
1. "Trace Formula Verification: link Berry–Keating trace formula to
   Hilbert–Polya via verified SMT-generated lemmas."
   - Berry–Keating is a **conjecture**. Hilbert–Polya is **unsolved**.
     Proving the trace formula ⇒ proving RH.
   - **SMT = finite/discrete logic. It cannot prove an analytic,
     infinite-dimensional trace formula.** SMT lemmas stop at arithmetic/algebra
     — exactly the scaffolding-empty pattern AUDIT_HONESTY flagged.
2. "Dirac Operator Convergence: prove self-adjointness in the limit P → ∞."
   - Discrete part (finite Hermitian matrices) feasible; Mathlib has linear algebra.
   - Limit P → ∞ with correct spectrum + trace formula = real operator theory,
     research-grade.

### Verdict
Phase 2 as worded = heavier AND of lower epistemic value. High risk of
repeating the "machine claims what it cannot prove" mistake.

---

## 3. DIRECTIVE — Milestone (a): real theorems first

Do NOT touch the spectral trace formula yet. Execute these in order:

### Milestone 1 — Prime Number Theorem from nonvanishing
- Input we hold: `zeta_ne_zero_one_le_re` (PNT-strength zero-free region).
- Mathlib provides: `Mathlib.NumberTheory.Chebyshev` (theta/psi, pi bounds).
- Assemble: PNT (π(x) ~ x/log x) as a proven consequence chain.
- Honest scope: Mathlib's PNT machinery exists; we link our zero-free
  statement to the formal PNT, removing any remaining `sorry`/axiom at our layer.

### Milestone 2 — Zero symmetry via functional equation
- Input we hold: `riemannZeta_one_sub` (functional equation).
- Prove: ζ(s) = 0 (s nontrivial) ⇒ ζ(1−s) = 0, with correct domain conditions
  (s ≠ -n, s ≠ 1). Free the proof of the junk value at s=1.
- Consequence: nontrivial zeros symmetric about Re(s) = 0.5.
- This is a real, Mathlib-supported theorem — NOT the Hilbert–Polya trace formula.

### After Milestone (a) — evaluate (b) ONLY if honest conditions met
Candidate (b) = discrete self-adjointness only (finite Hermitian matrix facts),
explicitly WITHOUT the P → ∞ analytic claim. Verify it adds provable content,
not decoration. Gate condition: no theorem above what Mathlib linear algebra
actually gives.

## 4. Hard rule (Law of the Guillotine)
- No `sorry`, no hidden `axiom`, no `by trivial` on analytic claims.
- No claim that SMT/Neural ODE proves an analytic identity.
- Scope statement in every module: what is proven vs what is assumed.
- Numerical GUE-style evidence stays labeled as evidence, NOT proof.