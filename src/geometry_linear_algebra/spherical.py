"""
Spherical & Elliptic Geometry Module
Models points p in R^3 on the unit sphere S^2 (p^T p = 1),
3D rotation matrices in SO(3), spherical geodesic distance d(p,q) = arccos(p^T q),
elliptic distance d([p],[q]) = arccos(|p^T q|) under antipodal identification p ~ -p,
great-circle arcs, spherical triangle angles, and spherical excess E = A + B + C - 180°.
"""

import numpy as np

def spherical_rotation_matrix_z(theta_deg: float) -> np.ndarray:
    """Constructs 3D Rotation Matrix around Z-axis."""
    rad = np.radians(theta_deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, -s, 0.0],
        [s,  c, 0.0],
        [0.0, 0.0, 1.0]
    ])

def spherical_rotation_matrix_y(theta_deg: float) -> np.ndarray:
    """Constructs 3D Rotation Matrix around Y-axis."""
    rad = np.radians(theta_deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [ c, 0.0, s],
        [0.0, 1.0, 0.0],
        [-s, 0.0, c]
    ])

def latlon_to_cartesian(lat_deg: float, lon_deg: float) -> np.ndarray:
    """Converts latitude and longitude (degrees) to 3D unit vector on S^2."""
    lat_rad = np.radians(lat_deg)
    lon_rad = np.radians(lon_deg)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    return np.array([x, y, z])

def spherical_distance(p: np.ndarray, q: np.ndarray) -> float:
    """
    Computes spherical geodesic distance d(p,q) = arccos(p^T q)
    on the unit sphere in radians.
    """
    p_unit = p / np.linalg.norm(p)
    q_unit = q / np.linalg.norm(q)
    dot_val = np.clip(np.dot(p_unit, q_unit), -1.0, 1.0)
    return float(np.arccos(dot_val))

def elliptic_distance(p: np.ndarray, q: np.ndarray) -> float:
    """
    Computes elliptic distance d([p],[q]) = arccos(|p^T q|)
    under antipodal identification p ~ -p in RP^2 (Spherical Model).
    """
    p_unit = p / np.linalg.norm(p)
    q_unit = q / np.linalg.norm(q)
    dot_val = np.clip(abs(np.dot(p_unit, q_unit)), 0.0, 1.0)
    return float(np.arccos(dot_val))

def spherical_great_circle_arc(p: np.ndarray, q: np.ndarray, n_pts: int = 50) -> np.ndarray:
    """
    Generates n_pts along the great-circle geodesic arc between p and q on S^2
    using Spherical Linear Interpolation (SLERP).
    """
    p_unit = p / np.linalg.norm(p)
    q_unit = q / np.linalg.norm(q)
    dot_val = np.clip(np.dot(p_unit, q_unit), -1.0, 1.0)
    omega = np.arccos(dot_val)
    
    if omega < 1e-6:
        return np.tile(p_unit, (n_pts, 1))

    t_vals = np.linspace(0, 1, n_pts)
    arc = np.array([
        (np.sin((1 - t) * omega) / np.sin(omega)) * p_unit + (np.sin(t * omega) / np.sin(omega)) * q_unit
        for t in t_vals
    ])
    return arc

def spherical_triangle_angles(A: np.ndarray, B: np.ndarray, C: np.ndarray) -> tuple[float, float, float, float, float]:
    """
    Computes interior angles (degrees), angle sum (degrees), and spherical excess for spherical triangle ABC.
    Uses the Spherical Law of Cosines:
        cos(A) = (cos(a) - cos(b)*cos(c)) / (sin(b)*sin(c))
    Returns: (angle_A_deg, angle_B_deg, angle_C_deg, angle_sum_deg, spherical_excess_deg)
    """
    a = spherical_distance(B, C)
    b = spherical_distance(A, C)
    c = spherical_distance(A, B)

    cos_A = np.clip((np.cos(a) - np.cos(b) * np.cos(c)) / (np.sin(b) * np.sin(c) + 1e-12), -1.0, 1.0)
    cos_B = np.clip((np.cos(b) - np.cos(a) * np.cos(c)) / (np.sin(a) * np.sin(c) + 1e-12), -1.0, 1.0)
    cos_C = np.clip((np.cos(c) - np.cos(a) * np.cos(b)) / (np.sin(a) * np.sin(b) + 1e-12), -1.0, 1.0)

    angle_A = np.degrees(np.arccos(cos_A))
    angle_B = np.degrees(np.arccos(cos_B))
    angle_C = np.degrees(np.arccos(cos_C))

    angle_sum = angle_A + angle_B + angle_C
    spherical_excess = angle_sum - 180.0

    return float(angle_A), float(angle_B), float(angle_C), float(angle_sum), float(spherical_excess)
