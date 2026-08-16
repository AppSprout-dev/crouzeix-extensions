#!/usr/bin/env python3
"""Sanity checks for the ratio harness (no third-party test runner required)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ensembles import nilpotent_shift
from ratio_harness import (
    THEORY_W_NILPOTENT,
    cb_crouzeix_ratio,
    numerical_radius,
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

    print("all passed" if ok else "SOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
