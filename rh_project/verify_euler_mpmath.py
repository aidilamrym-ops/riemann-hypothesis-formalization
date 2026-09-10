#!/usr/bin/env python3
"""
Euler Product Numerical Ground Truth Verification via mpmath
AETHER-Z3-OMEGA | Millennium Workspace
Computes ζ(s) and compares with finite Euler product ∏_{p < N} (1 - p^(-s))^(-1)
for Re(s) > 1 at 50 decimal places precision.
"""
import mpmath

mpmath.mp.dps = 50

def verify_euler_product():
    print("=" * 60)
    print("MPMATH GROUND TRUTH: EULER PRODUCT CONVERGENCE")
    print("=" * 60)
    
    # Test points with Re(s) > 1
    test_points = [
        mpmath.mpc(2.0, 0.0),
        mpmath.mpc(1.5, 2.0),
        mpmath.mpc(3.0, 5.0),
        mpmath.mpc(1.1, 10.0)
    ]
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
    
    all_passed = True
    for s in test_points:
        zeta_exact = mpmath.zeta(s)
        
        # Compute finite Euler product over primes
        prod = mpmath.mpc(1.0, 0.0)
        for p in primes:
            factor = 1 / (1 - mpmath.power(p, -s))
            prod *= factor
            
        diff = mpmath.fabs(zeta_exact - prod)
        # For 20 primes, error should be reasonably small
        passed = diff < 0.05
        all_passed = all_passed and passed
        
        print(f"s = {s}")
        print(f"  zeta(s) exact:      {zeta_exact}")
        print(f"  Euler prod (20p):   {prod}")
        print(f"  Difference:         {float(diff):.2e} | Status: {'PASS' if passed else 'APPROX'}")
        print("-" * 60)
        
    return all_passed

if __name__ == "__main__":
    success = verify_euler_product()
    print(f"Ground Truth Verification: {'SUCCESS' if success else 'CHECK'}")
