"""Matrix operations for finite numeric arrays."""

from __future__ import annotations

import numpy as np


def _matrix(value: object, name: str = "matrix") -> np.ndarray:
    try:
        result = np.asarray(value, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite two-dimensional matrix.") from exc
    if result.ndim != 2 or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be a finite two-dimensional matrix.")
    return result


def matmul(a: object, b: object) -> np.ndarray:
    """Multiply two compatible matrices."""
    left, right = _matrix(a, "a"), _matrix(b, "b")
    if left.shape[1] != right.shape[0]:
        raise ValueError("Matrix dimensions are not compatible for multiplication.")
    return left @ right


def transpose(matrix: object) -> np.ndarray:
    """Return the transpose of a matrix."""
    return _matrix(matrix).T


def inverse(matrix: object) -> np.ndarray:
    """Return the inverse of a square nonsingular matrix."""
    value = _matrix(matrix)
    if value.shape[0] != value.shape[1]:
        raise ValueError("Only square matrices can be inverted.")
    try:
        return np.linalg.inv(value)
    except np.linalg.LinAlgError as exc:
        raise ValueError("The matrix is singular and cannot be inverted.") from exc


def determinant(matrix: object) -> float:
    """Return the determinant of a square matrix."""
    value = _matrix(matrix)
    if value.shape[0] != value.shape[1]:
        raise ValueError("A determinant is defined only for square matrices.")
    return float(np.linalg.det(value))


def identity(size: int) -> np.ndarray:
    """Return the identity matrix of the requested positive size."""
    if isinstance(size, bool) or not isinstance(size, (int, np.integer)) or size < 1:
        raise ValueError("size must be a positive integer.")
    return np.eye(int(size))


def is_orthogonal(matrix: object, *, atol: float = 1e-8) -> bool:
    """Return whether a square matrix has orthonormal columns."""
    value = _matrix(matrix)
    if value.shape[0] != value.shape[1]:
        return False
    if not np.isfinite(atol) or atol < 0:
        raise ValueError("atol must be a finite nonnegative number.")
    return bool(np.allclose(value.T @ value, np.eye(value.shape[0]), atol=atol, rtol=0.0))
