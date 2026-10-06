"""Vector operations for finite one-dimensional numeric arrays."""

from __future__ import annotations

import numpy as np


def _vector(value: object, name: str = "vector") -> np.ndarray:
    try:
        result = np.asarray(value, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite one-dimensional vector.") from exc
    if result.ndim != 1 or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be a finite one-dimensional vector.")
    return result


def _pair(a: object, b: object) -> tuple[np.ndarray, np.ndarray]:
    left, right = _vector(a, "a"), _vector(b, "b")
    if left.shape != right.shape:
        raise ValueError("Vectors must have the same dimension.")
    return left, right


def dot(a: object, b: object) -> float:
    """Return the scalar dot product of two equal-length vectors."""
    left, right = _pair(a, b)
    return float(np.dot(left, right))


def cross(a: object, b: object) -> np.ndarray:
    """Return the 3D cross product of two three-component vectors."""
    left, right = _pair(a, b)
    if left.shape != (3,):
        raise ValueError("Cross product is defined here for 3D vectors.")
    return np.cross(left, right)


def norm(vector: object) -> float:
    """Return the Euclidean length of a vector."""
    return float(np.linalg.norm(_vector(vector)))


def normalize(vector: object) -> np.ndarray:
    """Return a unit vector in the same direction; reject the zero vector."""
    value = _vector(vector)
    length = float(np.linalg.norm(value))
    if length == 0.0:
        raise ValueError("The zero vector cannot be normalized.")
    return value / length


def distance(a: object, b: object) -> float:
    """Return the Euclidean distance between two equal-length vectors."""
    left, right = _pair(a, b)
    return float(np.linalg.norm(left - right))


def angle_between(a: object, b: object) -> float:
    """Return the unsigned angle in radians between two nonzero vectors."""
    left, right = _pair(a, b)
    denominator = float(np.linalg.norm(left) * np.linalg.norm(right))
    if denominator == 0.0:
        raise ValueError("Angle is undefined for a zero vector.")
    cosine = float(np.dot(left, right) / denominator)
    return float(np.arccos(np.clip(cosine, -1.0, 1.0)))
