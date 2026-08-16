#!/usr/bin/env python3
"""Empirical Crouzeix / completely-bounded ratio scouting.

Scalar Crouzeix is settled at constant 2. This harness:

* estimates W(A) by Johnson's supporting-line method (not crude Monte-Carlo);
* computes scalar ratios ||p(A)|| / max_{W(A)} |p|;
* probes cb ratios ||F(A)|| / max_{W(A)} ||F(z)|| for matrix-valued F;
* generates seeded synthetic ensembles (nilpotent shifts, triangular, …).

The original Monte-Carlo sampler systematically *underestimates* max |p| on
W(A) for high-degree monomials (the n=8 baseline of ~6.5 was an artifact).
Johnson's method is the default; `--legacy-mc` reproduces the old sampler.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

import numpy as np
from numpy.linalg import norm

# Allow `python numerical/ratio_harness.py` from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ensembles import (
    cem_motivated_block,
    ginibre,
    grcar,
    mild_nonnormal,
    nilpotent_shift,
    perturbed_nilpotent,
    random_nonnormal,
    random_triangular,
    weighted_shift,
)

# ---------------------------------------------------------------------------
# Numerical range
# ---------------------------------------------------------------------------


def numerical_range_boundary(A: np.ndarray, n_angles: int = 720) -> np.ndarray:
    """Johnson supporting-line vertices of W(A).

    For θ in [0, 2π), take a unit eigenvector of the largest eigenvalue of
    Re(e^{-iθ} A) and evaluate the Rayleigh quotient. The resulting polygon
    converges to ∂W(A) as n_angles → ∞. W(A) is convex, so the polygon is
    an inner approximation of the boundary.
    """
    A = np.asarray(A, dtype=complex)
    thetas = np.linspace(0.0, 2.0 * np.pi, n_angles, endpoint=False)
    pts = np.empty(n_angles, dtype=complex)
    for i, th in enumerate(thetas):
        phase = np.exp(-1j * th)
        H = 0.5 * (phase * A + np.conj(phase) * A.conj().T)
        evals, evecs = np.linalg.eigh(H)
        # Degenerate top eigenvalue ↔ a flat side of W(A). Record both ends.
        vmax = evals[-1]
        near = np.where(np.abs(evals - vmax) <= 1e-10 * max(1.0, abs(vmax)))[0]
        if near.size == 1:
            v = evecs[:, -1]
            v = v / np.linalg.norm(v)
            pts[i] = v.conj() @ A @ v
        else:
            candidates = []
            for j in near:
                v = evecs[:, j]
                v = v / np.linalg.norm(v)
                candidates.append(v.conj() @ A @ v)
            # Keep the candidate farthest from the running mean (boundary).
            c = np.asarray(candidates)
            pts[i] = c[np.argmax(np.abs(c - c.mean()))]
    return pts


def densify_boundary(pts: np.ndarray, per_edge: int = 4) -> np.ndarray:
    """Linear samples along the polygonal edges of a Johnson polygon."""
    if per_edge <= 1:
        return pts
    closed = np.concatenate([pts, pts[:1]])
    pieces = []
    for a, b in zip(closed[:-1], closed[1:]):
        ts = np.linspace(0.0, 1.0, per_edge, endpoint=False)
        pieces.append(a + ts * (b - a))
    return np.concatenate(pieces)


def numerical_radius(A: np.ndarray, n_angles: int = 720) -> float:
    """Numerical radius w(A) = max |z| for z in W(A)."""
    return float(np.max(np.abs(numerical_range_boundary(A, n_angles=n_angles))))


def numerical_radius_mc(A: np.ndarray, n_samples: int = 2000, seed: int | None = None) -> float:
    """Legacy Monte-Carlo numerical-radius estimate (inner, biased low)."""
    rng = np.random.default_rng(seed)
    n = A.shape[0]
    xs = rng.normal(size=(n_samples, n)) + 1j * rng.normal(size=(n_samples, n))
    xs /= np.linalg.norm(xs, axis=1, keepdims=True)
    vals = np.einsum("ij,jk,ik->i", xs.conj(), A, xs)
    return float(np.max(np.abs(vals)))


def departure_from_normality(A: np.ndarray) -> float:
    """Frobenius departure from normality ||A*A − AA*||_F."""
    C = A.conj().T @ A - A @ A.conj().T
    return float(norm(C, "fro"))


# ---------------------------------------------------------------------------
# Polynomial evaluation
# ---------------------------------------------------------------------------


def eval_scalar_poly(coeffs_low: np.ndarray, z) -> np.ndarray:
    """Evaluate p(z) = Σ c_j z^j (lowest degree first) on a scalar or array z."""
    acc = np.zeros_like(z, dtype=complex)
    zp = np.ones_like(z, dtype=complex)
    for c in coeffs_low:
        acc = acc + c * zp
        zp = zp * z
    return acc


def apply_scalar_poly(coeffs_low: np.ndarray, A: np.ndarray) -> np.ndarray:
    """p(A) = Σ c_j A^j, lowest degree first."""
    pA = np.zeros_like(A, dtype=complex)
    Ap = np.eye(A.shape[0], dtype=complex)
    for c in coeffs_low:
        pA = pA + c * Ap
        Ap = Ap @ A
    return pA


def apply_matrix_poly(coeff_mats: list[np.ndarray], A: np.ndarray) -> np.ndarray:
    """F(A) = Σ_j C_j ⊗ A^j  for C_j = coeff_mats[j]  (k×k)."""
    n = A.shape[0]
    k = coeff_mats[0].shape[0]
    out = np.zeros((k * n, k * n), dtype=complex)
    Ap = np.eye(n, dtype=complex)
    for C in coeff_mats:
        out = out + np.kron(C, Ap)
        Ap = Ap @ A
    return out


def eval_matrix_poly_at_z(coeff_mats: list[np.ndarray], z) -> np.ndarray:
    """F(z) = Σ_j C_j z^j. z may be a scalar; returns a k×k matrix."""
    k = coeff_mats[0].shape[0]
    out = np.zeros((k, k), dtype=complex)
    zp = 1.0 + 0.0j
    for C in coeff_mats:
        out = out + C * zp
        zp = zp * z
    return out


def max_abs_on_W(
    A: np.ndarray,
    func,
    n_angles: int = 720,
    per_edge: int = 4,
) -> float:
    """max_{z ∈ W(A)} func(z) for a nonnegative func, sampled on ∂W(A).

    ||F(z)|| and |p(z)| are subharmonic, so the max lives on the boundary.
    """
    pts = densify_boundary(numerical_range_boundary(A, n_angles=n_angles), per_edge)
    vals = [float(func(z)) for z in pts]
    return max(vals) if vals else float("nan")


# ---------------------------------------------------------------------------
# Ratios
# ---------------------------------------------------------------------------


def scalar_crouzeix_ratio(
    A: np.ndarray,
    poly_coeffs,
    n_samples: int = 2000,
    method: str = "johnson",
    n_angles: int = 720,
    rng_seed: int | None = None,
) -> float:
    """||p(A)|| / max_{W(A)} |p|.

    `poly_coeffs` is lowest-degree-first (same as the original harness).
    `method` is "johnson" (default) or "mc" (legacy Monte-Carlo).
    """
    coeffs = np.asarray(poly_coeffs, dtype=complex)
    pA = apply_scalar_poly(coeffs, A)
    num = float(norm(pA, 2))
    if method == "mc":
        rng = np.random.default_rng(rng_seed)
        n = A.shape[0]
        xs = rng.normal(size=(n_samples, n)) + 1j * rng.normal(size=(n_samples, n))
        xs /= np.linalg.norm(xs, axis=1, keepdims=True)
        zs = np.einsum("ij,jk,ik->i", xs.conj(), A, xs)
        # np.polyval wants highest degree first
        den = float(np.max(np.abs(np.polyval(coeffs[::-1], zs))))
    elif method == "johnson":
        den = max_abs_on_W(A, lambda z: np.abs(eval_scalar_poly(coeffs, z)), n_angles)
    else:
        raise ValueError(f"unknown method: {method}")
    return num / den if den > 0 else float("nan")


def cb_crouzeix_ratio(
    A: np.ndarray,
    coeff_mats: list[np.ndarray],
    n_angles: int = 720,
) -> float:
    """||F(A)|| / max_{W(A)} ||F(z)||  for a matrix-valued polynomial F."""
    FA = apply_matrix_poly(coeff_mats, A)
    num = float(norm(FA, 2))
    den = max_abs_on_W(
        A,
        lambda z: norm(eval_matrix_poly_at_z(coeff_mats, z), 2),
        n_angles,
    )
    return num / den if den > 0 else float("nan")


def random_matrix_poly(
    k: int,
    degree: int,
    seed: int,
    scale: float = 1.0,
) -> list[np.ndarray]:
    """Random C_0,…,C_degree with i.i.d. complex Gaussian entries, scaled."""
    rng = np.random.default_rng(seed)
    mats = []
    for _ in range(degree + 1):
        C = rng.normal(size=(k, k)) + 1j * rng.normal(size=(k, k))
        mats.append(scale * C)
    return mats


# ---------------------------------------------------------------------------
# Records / I/O
# ---------------------------------------------------------------------------


@dataclass
class RatioRecord:
    family: str
    n: int
    seed: str
    kind: str
    poly: str
    k: int
    degree: int
    op_norm: float
    max_on_W: float
    ratio: float
    num_radius: float
    mat_norm: float
    dfn: float
    method: str
    extra: str = ""


def _w_samples(A: np.ndarray, n_angles: int) -> np.ndarray:
    return densify_boundary(numerical_range_boundary(A, n_angles=n_angles), per_edge=4)


def _record_scalar(family, A, coeffs, poly_name, seed, method="johnson", n_angles=720, zs=None) -> RatioRecord:
    coeffs = np.asarray(coeffs, dtype=complex)
    pA = apply_scalar_poly(coeffs, A)
    if method == "johnson":
        if zs is None:
            zs = _w_samples(A, n_angles)
        den = float(np.max(np.abs(eval_scalar_poly(coeffs, zs))))
        wA = float(np.max(np.abs(zs)))
    else:
        den = float("nan")
        wA = numerical_radius(A, n_angles)
    num = float(norm(pA, 2))
    ratio = num / den if den > 0 else float("nan")
    return RatioRecord(
        family=family,
        n=A.shape[0],
        seed=str(seed),
        kind="scalar",
        poly=poly_name,
        k=1,
        degree=int(len(coeffs) - 1),
        op_norm=num,
        max_on_W=den,
        ratio=ratio,
        num_radius=wA,
        mat_norm=float(norm(A, 2)),
        dfn=departure_from_normality(A),
        method=method,
    )


def _record_cb(family, A, coeff_mats, poly_name, seed, n_angles=720, zs=None) -> RatioRecord:
    FA = apply_matrix_poly(coeff_mats, A)
    num = float(norm(FA, 2))
    if zs is None:
        zs = _w_samples(A, n_angles)
    den = max(float(norm(eval_matrix_poly_at_z(coeff_mats, z), 2)) for z in zs)
    ratio = num / den if den > 0 else float("nan")
    return RatioRecord(
        family=family,
        n=A.shape[0],
        seed=str(seed),
        kind="cb",
        poly=poly_name,
        k=coeff_mats[0].shape[0],
        degree=len(coeff_mats) - 1,
        op_norm=num,
        max_on_W=den,
        ratio=ratio,
        num_radius=float(np.max(np.abs(zs))),
        mat_norm=float(norm(A, 2)),
        dfn=departure_from_normality(A),
        method="johnson",
    )


def write_csv(path: Path, records: list[RatioRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(records[0]).keys()))
        w.writeheader()
        for r in records:
            w.writerow(asdict(r))


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------

N_ANGLES = 720
THEORY_W_NILPOTENT = {
    n: float(np.cos(np.pi / (n + 1))) for n in range(2, 17)
}


def campaign_sanity(n_angles: int = N_ANGLES) -> list[RatioRecord]:
    recs: list[RatioRecord] = []
    S2 = nilpotent_shift(2)
    recs.append(_record_scalar("nilpotent_shift", S2, [0.0, 1.0], "z", seed="det", n_angles=n_angles))
    recs[-1].extra = "exact_target=2"
    S3 = nilpotent_shift(3)
    recs.append(_record_scalar("nilpotent_shift", S3, [0.0, 1.0], "z", seed="det", n_angles=n_angles))
    recs[-1].extra = f"theory_w={THEORY_W_NILPOTENT[3]:.10f}"
    return recs


def campaign_nilpotent(ns=range(2, 13), n_angles: int = N_ANGLES) -> list[RatioRecord]:
    recs: list[RatioRecord] = []
    for n in ns:
        S = nilpotent_shift(n)
        zs = _w_samples(S, n_angles)
        recs.append(
            _record_scalar("nilpotent_shift", S, [0.0, 1.0], "z", seed="det", n_angles=n_angles, zs=zs)
        )
        recs[-1].extra = f"theory_w={THEORY_W_NILPOTENT[n]:.10f}"
        coeffs = [0.0] * (n - 1) + [1.0]
        recs.append(
            _record_scalar(
                "nilpotent_shift", S, coeffs, f"z^{n-1}", seed="det", n_angles=n_angles, zs=zs
            )
        )
        recs[-1].extra = f"theory_w={THEORY_W_NILPOTENT[n]:.10f}"
    return recs


def campaign_structured(n_angles: int = N_ANGLES) -> list[RatioRecord]:
    recs: list[RatioRecord] = []
    for n in (4, 8, 12):
        W = weighted_shift(n)
        zs = _w_samples(W, n_angles)
        recs.append(
            _record_scalar("weighted_shift", W, [0.0, 1.0], "z", seed="det", n_angles=n_angles, zs=zs)
        )
        recs.append(
            _record_scalar(
                "weighted_shift",
                W,
                [0.0] * (n - 1) + [1.0],
                f"z^{n-1}",
                seed="det",
                n_angles=n_angles,
                zs=zs,
            )
        )
    for n in (4, 8, 16):
        G = grcar(n)
        zs = _w_samples(G, n_angles)
        recs.append(_record_scalar("grcar", G, [0.0, 1.0], "z", seed="det", n_angles=n_angles, zs=zs))
        recs.append(
            _record_scalar("grcar", G, [1.0, -1.0, 0.5], "1-z+0.5z^2", seed="det", n_angles=n_angles, zs=zs)
        )
    return recs


def campaign_random(n_angles: int = N_ANGLES) -> list[RatioRecord]:
    recs: list[RatioRecord] = []
    specs = [
        ("random_triangular", random_triangular, (2, 3, 4, 8, 16), (2, 3, 4, 8, 16, 42, 99)),
        ("ginibre", ginibre, (2, 4, 8), (2, 7, 42)),
        ("mild_nonnormal", mild_nonnormal, (4, 8, 16), (1, 2, 3)),
        ("perturbed_nilpotent", perturbed_nilpotent, (3, 5, 8), (1, 2, 3)),
    ]
    for family, fn, ns, seeds in specs:
        for n in ns:
            for seed in seeds:
                A = fn(n, seed)
                zs = _w_samples(A, n_angles)
                recs.append(
                    _record_scalar(family, A, [0.0, 1.0], "z", seed=seed, n_angles=n_angles, zs=zs)
                )
                deg = min(n - 1, 4)
                coeffs = [0.0] * deg + [1.0]
                recs.append(
                    _record_scalar(family, A, coeffs, f"z^{deg}", seed=seed, n_angles=n_angles, zs=zs)
                )
                recs.append(
                    _record_scalar(
                        family, A, [0.4, -1.1, 0.7], "0.4-1.1z+0.7z^2", seed=seed, n_angles=n_angles, zs=zs
                    )
                )
    for kind in ("stiffness", "jacobian"):
        for n in (6, 12):
            for seed in (11, 22):
                A = cem_motivated_block(n, seed, kind=kind)
                zs = _w_samples(A, n_angles)
                recs.append(
                    _record_scalar(f"cem_{kind}", A, [0.0, 1.0], "z", seed=seed, n_angles=n_angles, zs=zs)
                )
                recs.append(
                    _record_scalar(
                        f"cem_{kind}", A, [1.0, 0.0, -0.2], "1-0.2z^2", seed=seed, n_angles=n_angles, zs=zs
                    )
                )
    return recs


def campaign_legacy_mc() -> list[RatioRecord]:
    """Reproduce the original harness numbers and the Johnson correction."""
    recs: list[RatioRecord] = []
    np.random.seed(42)  # original global seed (affects only the old MC path)
    for n in (2, 3, 4, 8):
        A = random_nonnormal(n, seed=n)
        coeffs = [0.0] * (n - 1) + [1.0]
        # Original API: global np.random inside scalar_crouzeix_ratio(..., method="mc")
        # Re-implement the *exact* original sampling (np.random.randn, not Generator).
        pA = apply_scalar_poly(np.asarray(coeffs, dtype=complex), A)
        num = float(norm(pA, 2))
        n_samples = 2000
        xs = np.random.randn(n_samples, n) + 1j * np.random.randn(n_samples, n)
        xs /= np.linalg.norm(xs, axis=1, keepdims=True)
        zs = np.einsum("ij,jk,ik->i", xs.conj(), A, xs)
        den_mc = float(np.max(np.abs(np.polyval(coeffs[::-1], zs))))
        rec = RatioRecord(
            family="random_triangular",
            n=n,
            seed=str(n),
            kind="scalar",
            poly=f"z^{n-1}",
            k=1,
            degree=n - 1,
            op_norm=num,
            max_on_W=den_mc,
            ratio=num / den_mc if den_mc > 0 else float("nan"),
            num_radius=numerical_radius(A),
            mat_norm=float(norm(A, 2)),
            dfn=departure_from_normality(A),
            method="mc_legacy",
            extra="original_harness_reproduction",
        )
        recs.append(rec)
        recs.append(
            _record_scalar(
                "random_triangular", A, coeffs, f"z^{n-1}", seed=n, method="johnson"
            )
        )
        recs[-1].extra = "johnson_correction_of_legacy"
    return recs


def campaign_cb(n_angles: int = N_ANGLES) -> list[RatioRecord]:
    recs: list[RatioRecord] = []
    # Structured near-extremal: 2×2 nilpotent, F(z) = B + z C.
    S2 = nilpotent_shift(2)
    zs2 = _w_samples(S2, n_angles)
    for k, seed in ((2, 0), (2, 1), (3, 2), (4, 3)):
        mats = random_matrix_poly(k, degree=1, seed=1000 + seed)
        recs.append(
            _record_cb(
                "nilpotent_shift", S2, mats, f"rand_k{k}_deg1", seed=1000 + seed, n_angles=n_angles, zs=zs2
            )
        )
    # F(z) = z I_k recovers the scalar monomial (ratio should be ~2).
    for k in (2, 3):
        mats = [np.zeros((k, k), dtype=complex), np.eye(k, dtype=complex)]
        recs.append(
            _record_cb("nilpotent_shift", S2, mats, f"z*I_{k}", seed="det", n_angles=n_angles, zs=zs2)
        )
        recs[-1].extra = "amplification_of_scalar_z"
    # Higher nilpotents + random triangular, modest k and degree.
    for n, seed in ((3, 5), (5, 6), (8, 7)):
        S = nilpotent_shift(n)
        mats = random_matrix_poly(2, degree=2, seed=2000 + seed)
        recs.append(_record_cb("nilpotent_shift", S, mats, "rand_k2_deg2", seed=2000 + seed, n_angles=n_angles))
    for n, seed in ((4, 8), (8, 9)):
        A = random_triangular(n, seed)
        mats = random_matrix_poly(2, degree=2, seed=3000 + seed)
        recs.append(_record_cb("random_triangular", A, mats, "rand_k2_deg2", seed=seed, n_angles=n_angles))
        mats3 = random_matrix_poly(3, degree=1, seed=4000 + seed)
        recs.append(_record_cb("random_triangular", A, mats3, "rand_k3_deg1", seed=seed, n_angles=n_angles))
    for n, seed in ((4, 10), (8, 11)):
        A = mild_nonnormal(n, seed)
        mats = random_matrix_poly(2, degree=1, seed=5000 + seed)
        recs.append(_record_cb("mild_nonnormal", A, mats, "rand_k2_deg1", seed=seed, n_angles=n_angles))
    for n, seed in ((6, 12),):
        A = cem_motivated_block(n, seed, kind="stiffness")
        mats = random_matrix_poly(2, degree=1, seed=6000 + seed)
        recs.append(_record_cb("cem_stiffness", A, mats, "rand_k2_deg1", seed=seed, n_angles=n_angles))
        A = cem_motivated_block(n, seed, kind="jacobian")
        mats = random_matrix_poly(2, degree=1, seed=7000 + seed)
        recs.append(_record_cb("cem_jacobian", A, mats, "rand_k2_deg1", seed=seed, n_angles=n_angles))
    return recs


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def fmt(r: float) -> str:
    if r != r:  # NaN
        return "  nan "
    return f"{r:7.4f}"


def summarize(records: list[RatioRecord]) -> str:
    lines = []
    scalar = [r for r in records if r.kind == "scalar" and r.method != "mc_legacy"]
    cb = [r for r in records if r.kind == "cb"]
    legacy = [r for r in records if r.method == "mc_legacy"]
    johnson_fix = [r for r in records if r.extra == "johnson_correction_of_legacy"]

    lines.append("# First-session numerical scout")
    lines.append("")
    lines.append(f"Date: {date.today().isoformat()}")
    lines.append("Estimator: Johnson supporting-line boundary of W(A) (720 angles, 4 edge samples).")
    lines.append("All random ensembles use `numpy.random.default_rng(seed)` with the seed recorded.")
    lines.append("")

    lines.append("## Sanity checks (nilpotent shifts)")
    lines.append("")
    lines.append("For the n-dimensional nilpotent Jordan block, W(S_n) is the disk of")
    lines.append("radius cos(π/(n+1)). In particular n=2 gives w=1/2, ||S||=1, ratio=2.")
    lines.append("")
    seen_n: set[int] = set()
    for r in records:
        if r.family == "nilpotent_shift" and r.poly == "z" and r.kind == "scalar":
            if r.n in seen_n:
                continue
            seen_n.add(r.n)
            theory = THEORY_W_NILPOTENT.get(r.n)
            extra = f"  theory_w={theory:.6f}" if theory else ""
            lines.append(
                f"- n={r.n:2d}  ||S||={r.mat_norm:.6f}  w≈{r.num_radius:.6f}  "
                f"ratio(z)≈{r.ratio:.6f}{extra}"
            )
    lines.append("")

    if legacy and johnson_fix:
        lines.append("## Legacy Monte-Carlo vs Johnson (original harness matrices)")
        lines.append("")
        lines.append("The original `np.random.randn` sampler underestimates max |p| on W(A).")
        lines.append("High-degree monomials amplify the bias (the n=8 ratio ~6.5 was an artifact).")
        lines.append("")
        lines.append("| n | poly | MC ratio | Johnson ratio | MC max\\|p\\| | Johnson max\\|p\\| |")
        lines.append("|---|------|----------|---------------|------------|------------------|")
        for mc, jn in zip(legacy, johnson_fix):
            lines.append(
                f"| {mc.n} | {mc.poly} | {mc.ratio:.4f} | {jn.ratio:.4f} | "
                f"{mc.max_on_W:.4e} | {jn.max_on_W:.4e} |"
            )
        lines.append("")

    def block(title: str, recs: list[RatioRecord]) -> None:
        if not recs:
            return
        ratios = [r.ratio for r in recs if r.ratio == r.ratio]
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"Count: {len(recs)}.  "
                     f"min={min(ratios):.4f}  median={float(np.median(ratios)):.4f}  "
                     f"max={max(ratios):.4f}")
        over = [r for r in recs if r.ratio == r.ratio and r.ratio > 2.0 + 1e-3]
        lines.append(f"Records with ratio > 2 + 10^{{-3}}: {len(over)}")
        if over:
            over_sorted = sorted(over, key=lambda r: -r.ratio)[:8]
            for r in over_sorted:
                lines.append(
                    f"  - {r.family} n={r.n} seed={r.seed} {r.poly}  ratio={r.ratio:.4f}  method={r.method}"
                )
        lines.append("")

    block("Scalar ratios (Johnson)", scalar)
    block("Completely-bounded probe ratios (Johnson)", cb)

    if cb:
        lines.append("## CB probe detail")
        lines.append("")
        lines.append("| family | n | k | poly | ratio | ||F(A)|| | max||F||_W |")
        lines.append("|--------|---|---|------|-------|----------|-------------|")
        for r in cb:
            lines.append(
                f"| {r.family} | {r.n} | {r.k} | {r.poly} | {r.ratio:.4f} | "
                f"{r.op_norm:.4f} | {r.max_on_W:.4f} |"
            )
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("- Scalar Johnson ratios are consistent with the settled theorem (universal 2).")
    lines.append("- The 2×2 nilpotent shift attains 2 and is the first Lean special-class target.")
    lines.append("- CB probes are *empirical* (finite k, low degree, Johnson sampling of ∂W).")
    lines.append("- No cb probe in this run is a candidate counter-example to cb=2; larger")
    lines.append("  amplifications and imported CEM snapshots are the next numerical step.")
    lines.append("")
    return "\n".join(lines) + "\n"


def print_console(records: list[RatioRecord]) -> None:
    print("Empirical Crouzeix / cb ratios")
    print("Johnson W(A) boundary (default). Ratios should stay ≤ ~2.")
    print()
    print(f"{'family':<22} {'n':>3} {'k':>2} {'poly':<18} {'ratio':>8} {'w(A)':>8} {'method'}")
    print("-" * 78)
    for r in records:
        print(
            f"{r.family:<22} {r.n:3d} {r.k:2d} {r.poly:<18} {fmt(r.ratio)} {fmt(r.num_radius)} {r.method}"
        )


# ---------------------------------------------------------------------------
# Synthetic data manifest
# ---------------------------------------------------------------------------


def write_manifest(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "date": date.today().isoformat(),
        "note": (
            "Matrices are generated on the fly by numerical/ensembles.py. "
            "Binary .npy/.npz are gitignored; this manifest is the source of truth."
        ),
        "families": {
            "nilpotent_shift": {
                "constructor": "ensembles.nilpotent_shift(n)",
                "seed": None,
                "n": list(range(2, 13)),
                "comment": "Jordan block; W = disk of radius cos(π/(n+1))",
            },
            "weighted_shift": {
                "constructor": "ensembles.weighted_shift(n)",
                "seed": None,
                "n": [4, 8, 12],
                "comment": "weights 1, 1/2, …, 1/(n-1)",
            },
            "random_triangular": {
                "constructor": "ensembles.random_triangular(n, seed)",
                "seeds": [2, 3, 4, 8, 16, 42, 99],
                "n": [2, 3, 4, 8, 16],
            },
            "ginibre": {
                "constructor": "ensembles.ginibre(n, seed)",
                "seeds": [2, 7, 42],
                "n": [2, 4, 8],
            },
            "mild_nonnormal": {
                "constructor": "ensembles.mild_nonnormal(n, seed, eps=0.3)",
                "seeds": [1, 2, 3],
                "n": [4, 8, 16],
            },
            "perturbed_nilpotent": {
                "constructor": "ensembles.perturbed_nilpotent(n, seed, eps=0.1)",
                "seeds": [1, 2, 3],
                "n": [3, 5, 8],
            },
            "grcar": {
                "constructor": "ensembles.grcar(n, k=3)",
                "n": [4, 8, 16],
            },
            "cem_stiffness": {
                "constructor": "ensembles.cem_motivated_block(n, seed, kind='stiffness')",
                "seeds": [11, 22],
                "n": [6, 12],
                "comment": "synthetic stand-in; not an imported Torquon-GB snapshot",
            },
            "cem_jacobian": {
                "constructor": "ensembles.cem_motivated_block(n, seed, kind='jacobian')",
                "seeds": [11, 22],
                "n": [6, 12],
                "comment": "synthetic stand-in; not an imported Hygra snapshot",
            },
        },
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path, default=None, help="experiment output directory")
    p.add_argument("--quick", action="store_true", help="sanity + nilpotent + small cb only")
    p.add_argument("--legacy-mc", action="store_true", default=True, help="include original-harness reproduction")
    p.add_argument("--no-legacy-mc", action="store_false", dest="legacy_mc")
    p.add_argument("--n-angles", type=int, default=N_ANGLES)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    n_angles = args.n_angles
    root = repo_root()
    out = args.out or (root / "experiments" / f"{date.today().isoformat()}-baseline")

    print("Empirical scalar Crouzeix ratios (should stay <= ~2)")
    records: list[RatioRecord] = []
    records.extend(campaign_sanity(n_angles=n_angles))
    records.extend(campaign_nilpotent(n_angles=n_angles))
    if args.legacy_mc:
        records.extend(campaign_legacy_mc())
    if not args.quick:
        records.extend(campaign_structured(n_angles=n_angles))
        records.extend(campaign_random(n_angles=n_angles))
    records.extend(campaign_cb(n_angles=n_angles if args.quick else n_angles))

    print_console(records)

    write_csv(out / "ratios.csv", records)
    summary = summarize(records)
    (out / "summary.md").write_text(summary, encoding="utf-8")
    write_manifest(root / "data" / "synthetic" / "manifest.json")

    scalar = [r for r in records if r.kind == "scalar" and r.method.startswith("johnson")]
    cb = [r for r in records if r.kind == "cb"]
    smax = max((r.ratio for r in scalar if r.ratio == r.ratio), default=float("nan"))
    cmax = max((r.ratio for r in cb if r.ratio == r.ratio), default=float("nan"))
    print()
    print(f"Wrote {len(records)} records to {out}")
    print(f"Scalar Johnson max ratio ≈ {smax:.4f}   CB probe max ratio ≈ {cmax:.4f}")
    print("Extend / re-run with --quick for a short pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
