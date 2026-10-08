"""
Core Linear Algebra Operations
Contains pure matrix and vector calculations.
"""

import numpy as np

# Standard 3D Minkowski Metric Tensor H = diag(1, 1, -1)
H_METRIC = np.array([
    [1.0,  0.0,  0.0],
    [0.0,  1.0,  0.0],
    [0.0,  0.0, -1.0]
])

def matrix_vector_mult(A: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Computes matrix-vector product A * v."""
    return A @ v

def dot_product(u: np.ndarray, v: np.ndarray) -> float:
    """Computes standard Euclidean dot product u^T * v."""
    return float(np.dot(u, v))

def vector_norm(v: np.ndarray) -> float:
    """Computes Euclidean L2 norm ||v|| = sqrt(v^T * v)."""
    return float(np.linalg.norm(v))

def minkowski_product(u: np.ndarray, v: np.ndarray) -> float:
    """
    Computes Minkowski bilinear inner product <u, v>_H = u^T H v
    where H = diag(1, 1, -1).
    """
    return float(u @ H_METRIC @ v)

def check_matrix_preservation(R: np.ndarray, M: np.ndarray) -> tuple[np.ndarray, float]:
    """
    Evaluates R^T * M * R and computes maximum absolute deviation from M:
        deviation = max |R^T * M * R - M|
    """
    R_T_M_R = R.T @ M @ R
    max_diff = float(np.max(np.abs(R_T_M_R - M)))
    return R_T_M_R, max_diff
