#!/usr/bin/env python3
"""Minimal harness for empirical Crouzeix / cb-ratio scouting.

Scalar Crouzeix is settled at constant 2.
This script computes observed ratios for random non-normal matrices
and can be extended to matrix-valued polynomials (cb probe).
"""

import numpy as np
from numpy.linalg import norm, eigvals

def numerical_radius(A, n_samples=2000):
    """Simple Monte-Carlo estimate of numerical radius."""
    n = A.shape[0]
    xs = np.random.randn(n_samples, n) + 1j * np.random.randn(n_samples, n)
    xs /= np.linalg.norm(xs, axis=1, keepdims=True)
    vals = np.einsum("ij,jk,ik->i", xs.conj(), A, xs)
    return np.max(np.abs(vals))

def random_nonnormal(n, seed=None):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    # mild non-normality via triangular factor
    Q, R = np.linalg.qr(A)
    return R

def scalar_crouzeix_ratio(A, poly_coeffs, n_samples=2000):
    """||p(A)|| / max_{W(A)} |p|  (Monte-Carlo max on numerical range)."""
    pA = np.zeros_like(A, dtype=complex)
    Ap = np.eye(A.shape[0], dtype=complex)
    for c in poly_coeffs:
        pA = pA + c * Ap
        Ap = Ap @ A
    num = norm(pA, 2)
    # crude max |p| on numerical range via samples
    n = A.shape[0]
    xs = np.random.randn(n_samples, n) + 1j * np.random.randn(n_samples, n)
    xs /= np.linalg.norm(xs, axis=1, keepdims=True)
    zs = np.einsum("ij,jk,ik->i", xs.conj(), A, xs)
    pzs = np.polyval(poly_coeffs[::-1], zs)  # numpy polyval highest degree first
    den = np.max(np.abs(pzs))
    return num / den if den > 0 else np.nan

if __name__ == "__main__":
    np.random.seed(42)
    print("Empirical scalar Crouzeix ratios (should stay <= ~2)")
    for n in (2, 3, 4, 8):
        A = random_nonnormal(n, seed=n)
        # monomial z^{n-1} often near-extremal for shifts
        coeffs = [0] * (n - 1) + [1.0]
        r = scalar_crouzeix_ratio(A, coeffs)
        print(f"  n={n:2d}  ratio ≈ {r:.4f}")
    print("\nExtend this harness with matrix-valued polynomials to probe the cb ratio.")
