"""
Hyperbolic Geometry Module
Models hyperboloid points p = [x, y, z]^T in R^3 (Minkowski space)
satisfying p^T H p = -1 with z > 0, Lorentz boost transformations B(t)
preserving R^T H R = H, hyperbolic distance d(p,q) = arccosh(-p^T H q),
Poincaré disk projection (u, v) = (x / (1+z), y / (1+z)),
hyperbolic geodesics, hyperbolic triangle angles, and angular defect D = 180° - (A + B + C).
"""

import numpy as np
from .linalg import minkowski_product

def lorentz_boost_x(t: float) -> np.ndarray:
    """
    Constructs a 3D Lorentz Boost Matrix along X-axis with rapidity t:
        [ cosh(t)   0   sinh(t) ]
        [    0      1      0    ]
        [ sinh(t)   0   cosh(t) ]

    Satisfies B^T * H * B = H where H = diag(1, 1, -1).
    """
    ch = np.cosh(t)
    sh = np.sinh(t)
    return np.array([
        [ch,  0.0, sh],
        [0.0, 1.0, 0.0],
        [sh,  0.0, ch]
    ])

def hyperboloid_point_from_disk(u: float, v: float) -> np.ndarray:
    """
    Converts a point (u, v) inside the 2D Poincaré disk (u^2 + v^2 < 1)
    to a point p = [x, y, z]^T on the hyperboloid upper sheet (z > 0, p^T H p = -1).
    Inverse Poincaré projection:
        denom = 1 - u^2 - v^2
        x = 2u / denom
        y = 2v / denom
        z = (1 + u^2 + v^2) / denom
    """
    r_sq = u**2 + v**2
    if r_sq >= 1.0:
        # Clamp to strictly inside the unit disk
        scale = 0.95 / np.sqrt(r_sq)
        u, v = u * scale, v * scale
        r_sq = u**2 + v**2
    
    denom = 1.0 - r_sq
    x = 2.0 * u / denom
    y = 2.0 * v / denom
    z = (1.0 + r_sq) / denom
    return np.array([x, y, z])

def hyperbolic_distance(p: np.ndarray, q: np.ndarray) -> float:
    """
    Computes hyperbolic geodesic distance d(p,q) = arccosh(-p^T H q)
    for points on the upper sheet of the hyperboloid (z > 0).
    """
    val = -minkowski_product(p, q)
    val = max(1.0, float(val))
    return float(np.arccosh(val))

def poincare_projection(p: np.ndarray) -> np.ndarray:
    """
    Projects a point p = [x, y, z]^T on the hyperboloid upper sheet (z > 0)
    onto the 2D Poincaré disk: (u, v) = (x / (1+z), y / (1+z)).
    """
    x, y, z = p[0], p[1], p[2]
    denom = 1.0 + z
    return np.array([x / denom, y / denom])

def poincare_geodesic_arc(p1: np.ndarray, p2: np.ndarray, n_pts: int = 50) -> np.ndarray:
    """
    Generates n_pts projected onto 2D Poincaré disk along the hyperbolic geodesic between
    hyperboloid points p1 and p2. Uses exact hyperboloid geodesic parametrization:
        p(t) = (sinh((1-t)d)/sinh(d)) * p1 + (sinh(t*d)/sinh(d)) * p2
    """
    d = hyperbolic_distance(p1, p2)
    if d < 1e-6:
        u_pt = poincare_projection(p1)
        return np.tile(u_pt, (n_pts, 1))

    t_vals = np.linspace(0, 1, n_pts)
    arc_disk = []
    for t in t_vals:
        p_t = (np.sinh((1 - t) * d) / np.sinh(d)) * p1 + (np.sinh(t * d) / np.sinh(d)) * p2
        arc_disk.append(poincare_projection(p_t))

    return np.array(arc_disk)

def hyperbolic_triangle_angles(A: np.ndarray, B: np.ndarray, C: np.ndarray) -> tuple[float, float, float, float, float]:
    """
    Computes interior angles (degrees), angle sum (degrees), and angular defect for hyperbolic triangle ABC.
    Uses Hyperbolic Law of Cosines:
        cos(A) = (cosh(b)*cosh(c) - cosh(a)) / (sinh(b)*sinh(c))
    Returns: (angle_A_deg, angle_B_deg, angle_C_deg, angle_sum_deg, angular_defect_deg)
    """
    # Hyperbolic side lengths
    a = hyperbolic_distance(B, C)
    b = hyperbolic_distance(A, C)
    c = hyperbolic_distance(A, B)

    # Hyperbolic Law of Cosines for angles
    cos_A = np.clip((np.cosh(b) * np.cosh(c) - np.cosh(a)) / (np.sinh(b) * np.sinh(c) + 1e-12), -1.0, 1.0)
    cos_B = np.clip((np.cosh(a) * np.cosh(c) - np.cosh(b)) / (np.sinh(a) * np.sinh(c) + 1e-12), -1.0, 1.0)
    cos_C = np.clip((np.cosh(a) * np.cosh(b) - np.cosh(c)) / (np.sinh(a) * np.sinh(b) + 1e-12), -1.0, 1.0)

    angle_A = np.degrees(np.arccos(cos_A))
    angle_B = np.degrees(np.arccos(cos_B))
    angle_C = np.degrees(np.arccos(cos_C))

    angle_sum = angle_A + angle_B + angle_C
    angular_defect = 180.0 - angle_sum

    return float(angle_A), float(angle_B), float(angle_C), float(angle_sum), float(angular_defect)
