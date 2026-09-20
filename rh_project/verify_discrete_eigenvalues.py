#!/usr/bin/env python3
"""
Numerical verification: eigenvalues of DiscreteOperator matrices vs zeta zeros
AETHER-Z3-OMEGA | Millennium Workspace | rh_project
"""
import numpy as np
import mpmath as mp
import json
import os

mp.mp.dps = 80

def berry_keating_matrix(N):
    """Construct the Berry-Keating candidate matrix: A[i,j] = (i - M) * (j - M)
    where M = N/2. This is a rank-1 outer product v⊗ᵥv."""
    M = N / 2.0
    v = np.array([i - M for i in range(N)], dtype=float)
    A = np.outer(v, v)
    return A

def laplacian_matrix(N):
    """Discrete 1D Laplacian: tridiagonal with 2 on diagonal, -1 on off-diagonals."""
    A = np.zeros((N, N))
    for i in range(N):
        A[i, i] = 2.0
        if i + 1 < N:
            A[i, i+1] = -1.0
            A[i+1, i] = -1.0
    return A

def eigenvalue_comparison(N_values=[10, 20, 50, 100]):
    """Compare eigenvalues with zeta zeros."""
    # First few zeta zeros (from mpmath)
    zeta_zeros = []
    for n in range(1, 21):
        zero = mp.zetazero(n)
        zeta_zeros.append(float(zero.imag))
    
    print("=" * 70)
    print("NUMERICAL EIGENVALUE vs ZETA ZEROS COMPARISON")
    print("=" * 70)
    
    results = {}
    
    for N in N_values:
        print(f"\nN = {N}")
        print("-" * 40)
        
        # Berry-Keating matrix
        B = berry_keating_matrix(N)
        evals_B = np.linalg.eigvals(B)
        evals_B = np.sort(evals_B.real)[::-1]  # descending
        
        # Laplacian matrix
        L = laplacian_matrix(N)
        evals_L = np.linalg.eigvals(L)
        evals_L = np.sort(evals_L.real)  # ascending
        
        # Berry-Keating: only one non-zero eigenvalue (rank-1)
        nonzero_B = evals_B[evals_B > 1e-10]
        print(f"  Berry-Keating nonzero eigenvalues: {nonzero_B[:5]}")
        print(f"  Berry-Keating zero eigenvalues (count): {N - len(nonzero_B)}")
        
        # Laplacian eigenvalues
        print(f"  Laplacian eigenvalues: {evals_L[:5]} ... {evals_L[-5:]}")
        
        # Compare with zeta zeros (only meaningful if we map appropriately)
        # Note: Berry-Keating eigenvalues are NOT zeta zeros - this is empirical exploration
        print(f"  First 5 zeta zeros (imag): {zeta_zeros[:5]}")
        
        results[N] = {
            "berry_keating_nonzero": nonzero_B.tolist(),
            "laplacian_evals": evals_L.tolist(),
        }
    
    return results

if __name__ == "__main__":
    results = eigenvalue_comparison([10, 20, 50, 100])
    
    # Save results
    os.makedirs("C:/Users/usER/oracle-toe/millennium_workspace/exports", exist_ok=True)
    with open("C:/Users/usER/oracle-toe/millennium_workspace/exports/eigenvalue_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 70)
    print("Results saved to exports/eigenvalue_results.json")
    print("=" * 70)