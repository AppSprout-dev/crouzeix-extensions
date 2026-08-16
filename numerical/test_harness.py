#!/usr/bin/env python3
"""Sanity checks for the ratio harness (no third-party test runner required)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ensembles import list_imported, load_imported_matrix, nilpotent_shift
from ratio_harness import (
    THEORY_W_NILPOTENT,
    cb_crouzeix_ratio,
    numerical_radius,
    random_matrix_poly,
    scalar_crouzeix_ratio,
)


def check(name: str, cond: bool, detail: str = "") -> bool:
    status = "ok" if cond else "FAIL"
    extra = f"  {detail}" if detail else ""
    print(f"  [{status}] {name}{extra}")
    return cond


def main() -> int:
    print("Harness sanity checks")
    ok = True

    S2 = nilpotent_shift(2)
    w2 = numerical_radius(S2, n_angles=360)
    r2 = scalar_crouzeix_ratio(S2, [0.0, 1.0], n_angles=360)
    ok &= check("2x2 nilpotent ||S||", abs(np.linalg.norm(S2, 2) - 1.0) < 1e-12, f"||S||={np.linalg.norm(S2, 2)}")
    ok &= check("2x2 nilpotent w(S)≈1/2", abs(w2 - 0.5) < 1e-8, f"w={w2}")
    ok &= check("2x2 nilpotent ratio(z)≈2", abs(r2 - 2.0) < 1e-8, f"ratio={r2}")

    S3 = nilpotent_shift(3)
    w3 = numerical_radius(S3, n_angles=720)
    theory3 = THEORY_W_NILPOTENT[3]
    r3 = scalar_crouzeix_ratio(S3, [0.0, 1.0], n_angles=720)
    ok &= check("3x3 nilpotent w(S)≈cos(π/4)", abs(w3 - theory3) < 2e-3, f"w={w3} theory={theory3}")
    ok &= check("3x3 nilpotent ratio(z)≈√2", abs(r3 - np.sqrt(2.0)) < 5e-3, f"ratio={r3}")

    # Amplification F(z)=z I_k recovers the scalar ratio.
    mats = [np.zeros((2, 2), dtype=complex), np.eye(2, dtype=complex)]
    r_cb = cb_crouzeix_ratio(S2, mats, n_angles=360)
    ok &= check("cb amplification z I_2 recovers 2", abs(r_cb - 2.0) < 1e-8, f"ratio={r_cb}")

    # S^2 = 0
    ok &= check("2x2 S^2=0", np.linalg.norm(S2 @ S2) < 1e-15)

    # Shipped cb path: k ≥ 8, degree ≥ 3, seeded. Must be finite and ≤ 2 + 1e-3.
    S5 = nilpotent_shift(5)
    mats_large = random_matrix_poly(k=8, degree=3, seed=20260816)
    r_large = cb_crouzeix_ratio(S5, mats_large, n_angles=180)
    ok &= check("large cb k=8 deg=3 finite", np.isfinite(r_large), f"ratio={r_large}")
    ok &= check("large cb k=8 deg=3 ≤ 2+1e-3", np.isfinite(r_large) and r_large <= 2.0 + 1e-3, f"ratio={r_large}")
    ok &= check("large cb coeff count", len(mats_large) == 4 and mats_large[0].shape == (8, 8))

    tq = list_imported("torquon-gb")
    hy = list_imported("hygra")
    ok &= check("torquon-gb snapshots present", len(tq) >= 3, f"count={len(tq)}")
    ok &= check("hygra snapshots present", len(hy) >= 3, f"count={len(hy)}")
    if tq:
        Aimp = load_imported_matrix("torquon-gb", "q4-element-k.json")
        ok &= check("imported q4 is 8x8", Aimp.shape == (8, 8))
        r_imp = scalar_crouzeix_ratio(Aimp, [0.0, 1.0], n_angles=180)
        ok &= check(
            "imported q4 scalar ratio finite ≤ 2+1e-3",
            np.isfinite(r_imp) and r_imp <= 2.0 + 1e-3,
            f"ratio={r_imp}",
        )
    if hy:
        J = load_imported_matrix("hygra", "flower-hvacd-jacobian.json")
        ok &= check("hygra flower jacobian 2x2", J.shape == (2, 2))
        r_j = scalar_crouzeix_ratio(J, [0.0, 1.0], n_angles=180)
        ok &= check(
            "hygra flower jacobian ratio finite ≤ 2+1e-3",
            np.isfinite(r_j) and r_j <= 2.0 + 1e-3,
            f"ratio={r_j}",
        )

    print("all passed" if ok else "SOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
