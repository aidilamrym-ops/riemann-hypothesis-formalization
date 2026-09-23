| **`PrimeDistribution.lean`** | 8 teorema: Chebyshev/prime-counting bounds | **Verified, Mathlib-proven (Milestone a)** |
| **`ZeroSymmetry.lean`** | 4 teorema: zero reflection via functional equation | **Verified, Mathlib-proven (Milestone a)** |
| **`DiscreteOperator.lean`** | 6 teorema: rank-1 Berry-Keating + diagonal Hermitian | **Verified, zero sorry (Milestone b)** |

**`DiscreteOperator.lean` Discrete Hermitian Operator (Milestone b - zero sorry):**
- `berryKeatingCandidate_isSymm` / `_isHermitian`: rank-1 outer product v⊗ᵥv, symmetry via `ring`
- `diagonal_isHermitian`: diagonal matrix Hermitian via `IsSymm` + `TrivialStar`
- `zero_isHermitian`: trivial base case

**`verify_discrete_eigenvalues.py` Numerical Verification:**
- Berry-Keating: rank-1, one nonzero eigenvalue (v·v), N-1 zeros
- Laplacian: spectrum bounded by [0, 4] per Gershgorin
- Numerical output: Berry-Keating eigenvalue scales as O(N²), Laplacian spectrum bounded

### Tingkat 2 - Verified tapi Trivial
`RhProject.lean`, `AdditionalTheorems.lean` - Aritmetika `nlinarith`/`linarith`, **bukan** struktur Millennium.

### Tingkat 3 - Placeholder Kosong (⚠️ KLAM DITARIK)
`NavierStokesRegularity.lean`, `BirchSwinnertonDyer.lean`, `HodgeConjecture.lean`, `PoincareConjecture.lean`, `PvsNP.lean`, `PillarSynergy.lean`, `Stage7D.lean`, `Stage7E.lean`, `Stage7F.lean`, `Stage7H.lean` - **BUKAN** verified struktur Millennium. Hanya scaffolding aksioma.

## Update Phase 1a (Euler Product + Functional Equation)
- **Step 1**: `ZetaBasic.lean` - replaced placeholder Euler product skeleton with 5 proven theorems via Mathlib `riemannZeta_eulerProduct_tprod` (and 4 variants)
- **Step 2**: `ZetaFunctional.lean` - functional equation strengthened via Mathlib `riemannZeta_one_sub` (real + complex)
- **Step 3**: Z3 batch 7 (10 verification): 7/10 VERIFIED (3 OTHER - QF_NRA limit transcendental)
- **Step 4**: mpmath ground truth (4 test points, 20 primes): all PASS
- **Cumulative Z3 verified**: 135 theorems (was 128)

## Update Phase 1b (Zero-Free Region — axioms removed)
- **Step 1**: `ConreyZeroFree.lean` rewritten — 3 axioms (A, B, F) REMOVED, replaced with Mathlib-proven nonvanishing (Stoll-Loeffler)
- **Step 2**: `Stage7J.lean` rewritten — no axioms, builds on ConreyZeroFree
- **Step 3**: Full build 1943 jobs, 0 sorry, 0 error
- **Step 4**: Z3 batch 8 (12 verification): 10/12 VERIFIED, 0 FAILED (2 OTHER - transcendental power)
- **Cumulative Z3 verified**: 145 theorems (was 135)

## Update Milestone (a) — Real theorems (2026-09-02)
- **`PrimeDistribution.lean`**: 8 Chebyshev/prime-counting theorems, ALL Mathlib-proven
  - Upper/lower bounds on θ(x) and π(x)
  - Structural identity π = θ/log + O(x/log²x)
  - Honest PNT gap documented (chain nonvanishing → θ/x → 1 requires explicit formula, absent from Mathlib v4.33.1)
- **`ZeroSymmetry.lean`**: 4 zero-symmetry theorems, ALL Mathlib-proven
  - `zero_of_one_sub_zero`: ζ(s)=0 ⇒ ζ(1-s)=0 (via functional equation)
  - `zero_symmetry_nontrivial`: version with domain conditions (0 < Re(s) ≤ 1)
  - `reflection_preserves_zero_strip`: zeros map into the critical strip
  - `domain_condition_for_nontrivial_zeros`: zeros with Re>0 avoid negative integers

## Update Milestone (b) — Discrete Hermitian Operator (2026-09-02)
- **`DiscreteOperator.lean`**: 6 theorems (rank-1 Berry-Keating + diagonal Hermitian)
  - `berryKeatingCandidate_isSymm` / `_isHermitian`: rank-1 outer product v⊗ᵥv, symmetry via `ring`
  - `diagonal_isHermitian`: diagonal matrix Hermitian via `IsSymm` + `TrivialStar`
  - `zero_isHermitian`: trivial base case
- **`verify_discrete_eigenvalues.py`**: numerical verification of eigenvalues
  - Berry-Keating: rank-1, one nonzero eigenvalue (v·v), N-1 zeros
  - Laplacian: spectrum bounded by [0, 4] per Gershgorin

## Changelog Tahap F
- 2026-09-01: Zero-Free Region proven via Mathlib nonvanishing (Stoll-Loeffler 2024)
- 2026-09-01: ConreyZeroFree.lean 3 axioms REMOVED → Tingkat 1 substantif
- 2026-09-01: Stage7J.lean rewritten (v2 axioms → v3 Mathlib proven)
- 2026-09-01: Z3 batch 8 added (12 theorems, 83% verified)
- 2026-09-01: ConreyZeroFree + Stage7J upgraded → Tingkat 1
- 2026-09-02: PrimeDistribution + ZeroSymmetry added → Milestone (a) complete
- 2026-09-02: DiscreteOperator.lean added → rank-1 Berry-Keating candidate + diagonal Hermitian
- 2026-09-02: DiscreteOperator promoted to Tingkat 1 substantif
- 2026-09-02: numerical verification script added
- 2026-09-02: Milestone (b) complete — no sorry, no axiom in DiscreteOperator
- Honest scope: Conrey-Vinogradov explicit bound `1 - C/log(|Im(s)|+2)` NOT in Mathlib v4.33.1 — deferred
- Honest scope: DiscreteOperator is structural stepping stone only, NOT a proof of RH
- Honest scope: Full PNT (θ(x)/x → 1) requires explicit formula — gap documented in PrimeDistribution.lean

## Update Final (2026-09-23) — Full Rewrite Honesty Pass
- **62/62 modules** in `lean4/AetherZ3Omega/Riemann/` rebuilt from source via `lean.exe` (kernel 4.33.1): 0 error, 0 sorry.
- **One open postulate only**: `AetherZ3Omega.riemann_hypothesis` (RhCore.lean). RH never claimed as proved.
- **Kernel `#print axioms` audit** post-rebuild: flagship theorems depend only on
  `[propext, Classical.choice, Quot.sound]` (+ `riemann_hypothesis` for the RH chain). See `exports/_axioms.txt`.
- All straw-man axioms removed or proved; all impossible "master theorems" re-framed honestly as
  conditional/consistency statements (e.g. `rigidity_at_infinity` conditional on RH postulate;
  `bounded_goldbach_consistency`, `hodge_conjecture_conditional`, `mass_gap_conditional`, etc.).
