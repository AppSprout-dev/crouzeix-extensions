#!/usr/bin/env python3
"""Static CEM snapshot export (read-only of published CEM algorithms).

Rebuilds the operators that Torquon-GB and Hygra actually use, from the
formulas in those repositories, and writes SCHEMA.md JSON under
data/imported/. This script never writes into a CEM repository.

Provenance (read 2026-08-16):
- Torquon-GB @ 2be4790  src/Generative/TopologyField.cs (Sigmund Q4 + assemble)
                         src/Domain/Analysis/BodyStiffness.cs (VDI flange k)
                         src/Generative/IntegratedBody.cs (EndPlateLoadCase BCs)
- Hygra     @ 9e71ce9  EnvelopeTakeoffModel, PhysicsConstants, MaterialSeedLibrary,
                         operator-intake.synthetic.json, OperatorUnitConversion
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
TORQUON_DIR = REPO / "data" / "imported" / "torquon-gb"
HYGRA_DIR = REPO / "data" / "imported" / "hygra"

TORQUON_SHA = "2be4790"
HYGRA_SHA = "9e71ce9"


def write_matrix(
    folder: Path,
    filename: str,
    *,
    ident: str,
    cem: str,
    kind: str,
    A: np.ndarray,
    units: str,
    notes: str,
) -> str:
    A = np.asarray(A, dtype=complex)
    n = int(A.shape[0])
    if A.shape != (n, n):
        raise ValueError(f"{ident}: expected square, got {A.shape}")
    if n > 32:
        raise ValueError(f"{ident}: n={n} exceeds first-export cap of 32")
    payload = {
        "id": ident,
        "cem": cem,
        "kind": kind,
        "n": n,
        "dtype": "complex128",
        "real": A.real.tolist(),
        "imag": A.imag.tolist(),
        "units": units,
        "notes": notes,
    }
    folder.mkdir(parents=True, exist_ok=True)
    (folder / filename).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return filename


# ---------------------------------------------------------------------------
# Torquon-GB — TopologyField.ElementK + Assemble (solid ρ=1)
# ---------------------------------------------------------------------------


def sigmund_q4_element_k(nu: float = 0.3) -> np.ndarray:
    """Canonical Sigmund Q4 plane-stress KE, E0=1. TopologyField.ElementK."""
    k = np.array(
        [
            1.0 / 2 - nu / 6,
            1.0 / 8 + nu / 8,
            -1.0 / 4 - nu / 12,
            -1.0 / 8 + 3 * nu / 8,
            -1.0 / 4 + nu / 12,
            -1.0 / 8 - nu / 8,
            nu / 6,
            1.0 / 8 - 3 * nu / 8,
        ],
        dtype=float,
    )
    idx = np.array(
        [
            [0, 1, 2, 3, 4, 5, 6, 7],
            [1, 0, 7, 6, 5, 4, 3, 2],
            [2, 7, 0, 5, 6, 3, 4, 1],
            [3, 6, 5, 0, 7, 2, 1, 4],
            [4, 5, 6, 7, 0, 1, 2, 3],
            [5, 4, 3, 2, 1, 0, 7, 6],
            [6, 3, 4, 1, 2, 7, 0, 5],
            [7, 2, 1, 4, 3, 6, 5, 0],
        ],
        dtype=int,
    )
    f = 1.0 / (1.0 - nu * nu)
    return f * k[idx]


def node_id(i: int, j: int, nely: int) -> int:
    return j * (nely + 1) + i


def edof(ei: int, ej: int, nely: int) -> np.ndarray:
    tL = node_id(ei, ej, nely)
    tR = node_id(ei, ej + 1, nely)
    bR = node_id(ei + 1, ej + 1, nely)
    bL = node_id(ei + 1, ej, nely)
    return np.array([2 * tL, 2 * tL + 1, 2 * tR, 2 * tR + 1, 2 * bR, 2 * bR + 1, 2 * bL, 2 * bL + 1])


def assemble_solid_k(nelx: int, nely: int, nu: float = 0.3) -> np.ndarray:
    ke = sigmund_q4_element_k(nu)
    ndof = 2 * (nelx + 1) * (nely + 1)
    K = np.zeros((ndof, ndof), dtype=float)
    for ej in range(nelx):
        for ei in range(nely):
            ed = edof(ei, ej, nely)
            K[np.ix_(ed, ed)] += ke
    return K


def reduce_free(K: np.ndarray, fixed: list[int]) -> np.ndarray:
    n = K.shape[0]
    free = [i for i in range(n) if i not in set(fixed)]
    return K[np.ix_(free, free)]


def mbb_fixed(nelx: int, nely: int) -> list[int]:
    fixed = [2 * node_id(i, 0, nely) for i in range(nely + 1)]
    fixed.append(2 * node_id(nely, nelx, nely) + 1)
    return fixed


def endplate_corner_fixed(nelx: int, nely: int) -> list[int]:
    """4-corner ground (both dofs), matching EndPlateLoadCase's always-on supports."""
    corners = [
        node_id(0, 0, nely),
        node_id(0, nelx, nely),
        node_id(nely, 0, nely),
        node_id(nely, nelx, nely),
    ]
    fixed: list[int] = []
    for n in corners:
        fixed.extend([2 * n, 2 * n + 1])
    return fixed


def export_torquon() -> list[str]:
    files: list[str] = []
    ke = sigmund_q4_element_k(0.3)
    files.append(
        write_matrix(
            TORQUON_DIR,
            "q4-element-k.json",
            ident="torquon-gb/q4-element-k",
            cem="torquon-gb",
            kind="stiffness",
            A=ke,
            units="E0=1 (TopologyField unit-modulus plane-stress)",
            notes=(
                f"Sigmund Q4 element stiffness, ν=0.3, E0=1. Exact transcription of "
                f"Torquon-GB@{TORQUON_SHA} TopologyField.ElementK. DOF order "
                "[tL(x,y), tR, bR, bL]. Anonymized: no part numbers."
            ),
        )
    )

    K = assemble_solid_k(2, 2)
    Kf = reduce_free(K, mbb_fixed(2, 2))
    files.append(
        write_matrix(
            TORQUON_DIR,
            "mbb-2x2-free-stiffness.json",
            ident="torquon-gb/mbb-2x2-free-stiffness",
            cem="torquon-gb",
            kind="stiffness",
            A=Kf,
            units="E0=1 solid ρ=1 (same as TopologyField.SolveLinear)",
            notes=(
                f"2×2 solid MBB beam, free-DOF stiffness after the published half-MBB "
                f"supports (left-edge x, bottom-right y roller). Torquon-GB@{TORQUON_SHA} "
                "TopologyField.OptimizeMBB / SolveLinear. Downscaled for n≤32; same BCs."
            ),
        )
    )

    K = assemble_solid_k(3, 2)
    Kf = reduce_free(K, endplate_corner_fixed(3, 2))
    files.append(
        write_matrix(
            TORQUON_DIR,
            "endplate-3x2-corner-grounded.json",
            ident="torquon-gb/endplate-3x2-corner-grounded",
            cem="torquon-gb",
            kind="stiffness",
            A=Kf,
            units="E0=1 solid ρ=1 plane-stress",
            notes=(
                f"3×2 solid plate, four corners grounded in both dofs — the always-on "
                f"supports of IntegratedBody.EndPlateLoadCase (Torquon-GB@{TORQUON_SHA}). "
                "Production end-plate mesh is larger (nelx≈24); this is the same operator "
                "family at first-export dimension."
            ),
        )
    )

    # VDI-2230 flange member: k = E A / L, two-node axial spring (housing vs mate).
    e_mpa = 200_000.0  # steel, BodyStiffness.SelfTest cantilever
    flange_w, flange_t, plate_t = 10.0, 5.0, 8.0  # IntegratedSpec.Default + self-test t
    a_mm2 = 2.0 * flange_w * flange_t
    l_mm = plate_t + flange_t
    k_n_per_mm = e_mpa * a_mm2 / l_mm
    k_flange = np.array([[k_n_per_mm, -k_n_per_mm], [-k_n_per_mm, k_n_per_mm]], dtype=float)
    files.append(
        write_matrix(
            TORQUON_DIR,
            "vdi-flange-axial-spring.json",
            ident="torquon-gb/vdi-flange-axial-spring",
            cem="torquon-gb",
            kind="stiffness",
            A=k_flange,
            units="N/mm",
            notes=(
                f"BodyStiffness.FlangeGapMicron k=E·A/L with IntegratedSpec.Default "
                f"flange 10×5 mm, two long-side runs, L=plate+flange=13 mm, E=200 GPa "
                f"(Torquon-GB@{TORQUON_SHA}). Singular rigid-body pair — the CEM spring."
            ),
        )
    )
    return files


# ---------------------------------------------------------------------------
# Hygra — EnvelopeTakeoff + RoomHvacd linearizations
# ---------------------------------------------------------------------------

SF_PER_M2 = 10.76391041671
LATENT_J_PER_KG = 2.45e6
SECONDS_PER_DAY = 86400.0
ET_KG_M2_DAY = {"flower": 5.0, "veg": 3.5, "dry": 0.2}
LIGHT_LATENT_FRAC = {"flower": 0.45, "veg": 0.35, "dry": 0.0}


def assembly_u(series_r: float, rsi: float, rse: float) -> float:
    return 1.0 / (rsi + series_r + rse)


def imp100_series_r() -> float:
    # 0.5 mm steel + 100 mm PU + 0.5 mm steel
    return 0.0005 / 50.0 + 0.100 / 0.024 + 0.0005 / 50.0


def slab_series_r() -> float:
    return 0.150 / 1.4 + 0.003 / 0.20


def room_ua_and_inf(floor_m2: float, *, sealed: bool = True) -> tuple[float, float]:
    """EnvelopeTakeoffModel UA + infiltration conductance (W/K) at DefaultPeak."""
    height = 3.0
    length = np.sqrt(floor_m2 * 1.5)
    width = np.sqrt(floor_m2 / 1.5)
    perimeter = 2.0 * (length + width)
    wall_area = perimeter * height
    roof_area = floor_m2
    slab_area = floor_m2
    if sealed:
        wall_glazed, roof_glazed, fen_u, ach = 0.02, 0.0, 2.0, 0.15
    else:
        wall_glazed, roof_glazed, fen_u, ach = 0.25, 0.70, 3.5, 0.60
    r_imp = imp100_series_r()
    r_slab = slab_series_r()
    u_wall = assembly_u(r_imp, 0.13, 0.04)
    u_roof = assembly_u(r_imp, 0.10, 0.04)
    u_slab = assembly_u(r_slab, 0.17, 0.0)
    wall_ua = 1.15 * u_wall * wall_area * (1.0 - wall_glazed)
    roof_ua = 1.15 * u_roof * roof_area * (1.0 - roof_glazed)
    slab_ua = 0.5 * u_slab * slab_area
    fen_ua = fen_u * (wall_area * wall_glazed + roof_area * roof_glazed)
    ua = wall_ua + roof_ua + slab_ua + fen_ua
    volume = floor_m2 * height
    inf_g = ach * volume / 3600.0 * 1.20 * 1006.0
    return float(ua), float(inf_g)


def hvacd_jacobian(
    floor_m2: float, canopy_m2: float, role: str, t_in: float, p_light: float
) -> np.ndarray:
    """∂(qNetSens, qLatPrimary)/∂(T_in, P_light) at DefaultPeak lights-on.

    RoomHvacdLoadModel + LatentEtProxyModel (primary ET, not lighting-alt):
      qLat = ET·A·L_v / 86400
      qEnv = G·(T_out − T_in)
      qGross = P_light + max(0, qEnv)
      qNet  = max(0, qGross − α·qLat)
    """
    ua, inf_g = room_ua_and_inf(floor_m2)
    g = ua + inf_g
    t_out = 35.0
    alpha = 1.0
    q_lat = ET_KG_M2_DAY[role] * canopy_m2 / SECONDS_PER_DAY * LATENT_J_PER_KG
    q_env = g * (t_out - t_in)
    q_gross = p_light + max(0.0, q_env)
    interior = q_gross - alpha * q_lat > 0
    dqnet_dt = (-g if q_env > 0 else 0.0) if interior else 0.0
    dqnet_dp = 1.0 if interior else 0.0
    return np.array([[dqnet_dt, dqnet_dp], [0.0, 0.0]], dtype=float)


def hvacd_jacobian_alt_latent(floor_m2: float, role: str, t_in: float, p_light: float) -> np.ndarray:
    """Same map using the *alternate* lighting-power latent fraction."""
    ua, inf_g = room_ua_and_inf(floor_m2)
    g = ua + inf_g
    frac = LIGHT_LATENT_FRAC[role]
    alpha = 1.0
    t_out = 35.0
    q_env = g * (t_out - t_in)
    q_lat = frac * p_light
    q_gross = p_light + max(0.0, q_env)
    interior = q_gross - alpha * q_lat > 0
    dqnet_dt = (-g if q_env > 0 else 0.0) if interior else 0.0
    dqnet_dp = (1.0 - alpha * frac) if interior else 0.0
    dqlat_dp = frac
    return np.array([[dqnet_dt, dqnet_dp], [0.0, dqlat_dp]], dtype=float)


def export_hygra() -> list[str]:
    files: list[str] = []
    # operator-intake.synthetic.json, units=UsCustomary
    rooms = [
        ("flower", 400.0, 77.0, 12000.0),
        ("veg", 120.0, 78.0, 3000.0),
        ("dry", 100.0, 65.0, 0.0),
    ]
    canopy = []
    t_in = []
    p_light = []
    for _, area_ft2, t_f, watts in rooms:
        canopy.append(area_ft2 / SF_PER_M2)
        t_in.append((t_f - 32.0) * 5.0 / 9.0)
        p_light.append(watts)
    floors = list(canopy)  # tiers = 1

    g_tot = []
    for fl in floors:
        ua, inf_g = room_ua_and_inf(fl)
        g_tot.append(ua + inf_g)
    j_t = -np.diag(g_tot)
    files.append(
        write_matrix(
            HYGRA_DIR,
            "envelope-dqdt-3room.json",
            ident="hygra/envelope-dqdt-3room",
            cem="hygra",
            kind="jacobian",
            A=j_t,
            units="W/K",
            notes=(
                f"∂Q_env/∂T_in for flower/veg/dry from Hygra@{HYGRA_SHA} "
                "EnvelopeTakeoffModel on examples/operator-intake.synthetic.json "
                "(UsCustomary areas → m²). Sealed IMP-100 + slab-epoxy + infiltration. "
                "Rooms are thermally independent at first order (diagonal). "
                "Anonymized: synthetic demo grow, not a real site."
            ),
        )
    )

    jf = hvacd_jacobian(floors[0], canopy[0], "flower", t_in[0], p_light[0])
    files.append(
        write_matrix(
            HYGRA_DIR,
            "flower-hvacd-jacobian.json",
            ident="hygra/flower-hvacd-jacobian",
            cem="hygra",
            kind="jacobian",
            A=jf,
            units="W/K and W/W; rows (qNetSens, qLatPrimary), cols (T_in, P_light)",
            notes=(
                f"RoomHvacdLoadModel + LatentEtProxyModel primary ET path "
                f"(Hygra@{HYGRA_SHA}) on flower-01 at DefaultPeak (T_out=35 °C, α=1). "
                "Non-normal: temperature hits sensible only; ET latent is T-independent."
            ),
        )
    )

    jv = hvacd_jacobian(floors[1], canopy[1], "veg", t_in[1], p_light[1])
    files.append(
        write_matrix(
            HYGRA_DIR,
            "veg-hvacd-jacobian.json",
            ident="hygra/veg-hvacd-jacobian",
            cem="hygra",
            kind="jacobian",
            A=jv,
            units="W/K and W/W; rows (qNetSens, qLatPrimary), cols (T_in, P_light)",
            notes=(
                f"Same operator family as flower-hvacd-jacobian on veg-01 "
                f"(Hygra@{HYGRA_SHA}). Nearly-commuting pair for joint tests."
            ),
        )
    )

    jalt = hvacd_jacobian_alt_latent(floors[0], "flower", t_in[0], p_light[0])
    files.append(
        write_matrix(
            HYGRA_DIR,
            "flower-hvacd-jacobian-alt-latent.json",
            ident="hygra/flower-hvacd-jacobian-alt-latent",
            cem="hygra",
            kind="jacobian",
            A=jalt,
            units="W/K and W/W; rows (qNetSens, qLatAlt), cols (T_in, P_light)",
            notes=(
                f"Alternate lighting-power latent fraction "
                f"(PhysicsConstants.LightingToLatentFraction Flower=0.45), Hygra@{HYGRA_SHA}."
            ),
        )
    )
    return files


def write_manifests(torquon_files: list[str], hygra_files: list[str]) -> None:
    (TORQUON_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "cem": "torquon-gb",
                "exported": "2026-08-16",
                "source_sha": TORQUON_SHA,
                "matrices": torquon_files,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (HYGRA_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "cem": "hygra",
                "exported": "2026-08-16",
                "source_sha": HYGRA_SHA,
                "matrices": hygra_files,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    t = export_torquon()
    h = export_hygra()
    write_manifests(t, h)
    print("Torquon-GB:", ", ".join(t))
    print("Hygra:", ", ".join(h))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
