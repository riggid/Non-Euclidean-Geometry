"""
Euclidean Geometry Module
Models points v in R^2, 2D triangle properties, Euclidean rotation matrices R(theta),
orthogonal matrix property R^T R = I, vector norms, and vector projections.
"""

import numpy as np
from .linalg import dot_product, vector_norm

def euclidean_rotation_matrix(theta_deg: float) -> np.ndarray:
    """
    Constructs 2D Rotation Matrix R(theta):
        [ cos(theta)  -sin(theta) ]
        [ sin(theta)   cos(theta) ]
    """
    rad = np.radians(theta_deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, -s],
        [s,  c]
    ])

def project_vector(v: np.ndarray, u: np.ndarray) -> np.ndarray:
    """
    Computes orthogonal projection of vector v onto u:
        proj_u(v) = ((v^T u) / (u^T u)) * u
    """
    u_norm_sq = dot_product(u, u)
    if u_norm_sq == 0:
        raise ValueError("Cannot project onto a zero vector.")
    scalar_proj = dot_product(v, u) / u_norm_sq
    return scalar_proj * u

def euclidean_distance(p: np.ndarray, q: np.ndarray) -> float:
    """Computes Euclidean distance ||p - q||_2."""
    return vector_norm(p - q)

def euclidean_triangle_angles(A: np.ndarray, B: np.ndarray, C: np.ndarray) -> tuple[float, float, float, float]:
    """
    Computes side lengths and interior angles (in degrees) for a 2D Euclidean triangle ABC.
    Returns: (angle_A_deg, angle_B_deg, angle_C_deg, angle_sum_deg)
    """
    u_A = B - A
    v_A = C - A
    cos_A = np.clip(dot_product(u_A, v_A) / (vector_norm(u_A) * vector_norm(v_A)), -1.0, 1.0)
    angle_A = np.degrees(np.arccos(cos_A))

    u_B = A - B
    v_B = C - B
    cos_B = np.clip(dot_product(u_B, v_B) / (vector_norm(u_B) * vector_norm(v_B)), -1.0, 1.0)
    angle_B = np.degrees(np.arccos(cos_B))

    u_C = A - C
    v_C = B - C
    cos_C = np.clip(dot_product(u_C, v_C) / (vector_norm(u_C) * vector_norm(v_C)), -1.0, 1.0)
    angle_C = np.degrees(np.arccos(cos_C))

    angle_sum = angle_A + angle_B + angle_C
    return float(angle_A), float(angle_B), float(angle_C), float(angle_sum)

def euclidean_triangle_area(A: np.ndarray, B: np.ndarray, C: np.ndarray) -> float:
    """Computes area of 2D Euclidean triangle using cross product determinant formula."""
    return 0.5 * abs(float(A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1])))
