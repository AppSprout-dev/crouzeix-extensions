"""Reproducible non-normal matrix families for Crouzeix / cb scouting.

Every generator that uses randomness takes an explicit seed. Structured
families (nilpotent / weighted / Grcar) are deterministic.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

Array = np.ndarray

_IMPORTED_ROOT = Path(__file__).resolve().parent.parent / "data" / "imported"


def load_imported_matrix(cem: str, filename: str) -> Array:
    """Load a SCHEMA.md snapshot from data/imported/<cem>/<filename>."""
    path = _IMPORTED_ROOT / cem / filename
    payload = json.loads(path.read_text(encoding="utf-8"))
    real = np.asarray(payload["real"], dtype=float)
    imag = np.asarray(payload["imag"], dtype=float)
    if real.shape != imag.shape:
        raise ValueError(f"{path}: real/imag shape mismatch")
    return real + 1j * imag


def list_imported(cem: str) -> list[str]:
    man = _IMPORTED_ROOT / cem / "manifest.json"
    if not man.is_file():
        return []
    return list(json.loads(man.read_text(encoding="utf-8")).get("matrices", []))


def nilpotent_shift(n: int) -> Array:
    """Unweighted nilpotent Jordan block: 1's on the superdiagonal.

    W(S_n) is the disk of radius cos(π/(n+1)). Classical near-extremal
    example: for n=2, w(S)=1/2 and ||S||=1, so the scalar ratio for
    p(z)=z is exactly 2.
    """
    S = np.zeros((n, n), dtype=complex)
    if n >= 2:
        S[np.arange(n - 1), np.arange(1, n)] = 1.0
    return S


def weighted_shift(n: int, weights: Array | None = None, seed: int | None = None) -> Array:
    """Weighted forward shift (transport-like). Default weights are 1, 1/2, …."""
    S = np.zeros((n, n), dtype=complex)
    if n < 2:
        return S
    if weights is None:
        if seed is None:
            weights = 1.0 / np.arange(1, n, dtype=float)
        else:
            rng = np.random.default_rng(seed)
            weights = rng.uniform(0.25, 1.5, size=n - 1)
    w = np.asarray(weights, dtype=complex).reshape(-1)
    if w.size != n - 1:
        raise ValueError(f"expected {n - 1} weights, got {w.size}")
    S[np.arange(n - 1), np.arange(1, n)] = w
    return S


def random_triangular(n: int, seed: int) -> Array:
    """Upper-triangular factor of a complex Ginibre matrix (QR)."""
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    _, R = np.linalg.qr(A)
    return R


def random_nonnormal(n: int, seed: int | None = None) -> Array:
    """Back-compat alias used by the original harness."""
    if seed is None:
        seed = 0
    return random_triangular(n, seed)


def ginibre(n: int, seed: int) -> Array:
    """Complex Ginibre ensemble (i.i.d. complex Gaussians)."""
    rng = np.random.default_rng(seed)
    return rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))


def mild_nonnormal(n: int, seed: int, eps: float = 0.3) -> Array:
    """Normal (Hermitian) part plus a scaled strictly-upper triangular term.

    Models CEM operators that are a small departure from normality
    (asymmetric loading, tolerances).
    """
    rng = np.random.default_rng(seed)
    G = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    H = (G + G.conj().T) / 2.0
    N = np.triu(rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)), k=1)
    return H + eps * N


def perturbed_nilpotent(n: int, seed: int, eps: float = 0.1) -> Array:
    """Nilpotent shift plus a small unstructured perturbation."""
    rng = np.random.default_rng(seed)
    E = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    return nilpotent_shift(n) + eps * E / max(np.linalg.norm(E, 2), 1e-15)


def grcar(n: int, k: int = 3) -> Array:
    """Grcar Toeplitz matrix: classic non-normal test family.

    1's on the subdiagonal, 1's on the diagonal, and k superdiagonals of −1.
    """
    A = np.eye(n, dtype=complex)
    if n >= 2:
        A[np.arange(1, n), np.arange(n - 1)] = 1.0
    for d in range(1, min(k, n) + 1):
        A[np.arange(n - d), np.arange(d, n)] = -1.0
    return A


def cem_motivated_block(n: int, seed: int, kind: str = "stiffness") -> Array:
    """Small synthetic stand-in for CEM operators (not imported snapshots).

    * stiffness — SPD-ish plus a mild non-symmetric damping term
    * jacobian  — diagonally dominant, nearly triangular (zone coupling)
    """
    rng = np.random.default_rng(seed)
    if kind == "stiffness":
        G = rng.normal(size=(n, n))
        K = G.T @ G + 0.3 * np.eye(n)
        D = np.triu(rng.normal(size=(n, n), scale=0.15), k=1)
        return (K + D).astype(complex)
    if kind == "jacobian":
        diag = -np.abs(rng.normal(size=n, loc=1.0, scale=0.2))
        J = np.diag(diag).astype(complex)
        J += np.triu(rng.normal(size=(n, n), scale=0.08), k=1)
        J += np.tril(rng.normal(size=(n, n), scale=0.02), k=-1)
        return J
    raise ValueError(f"unknown CEM-motivated kind: {kind}")
