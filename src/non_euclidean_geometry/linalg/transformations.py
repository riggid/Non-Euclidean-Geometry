"""Three-dimensional rotations and homogeneous transformations."""

from __future__ import annotations

import numpy as np


def rotation_x(angle: float) -> np.ndarray:
    """Return the 3x3 right-handed rotation about the x axis."""
    c, s = np.cos(_angle(angle)), np.sin(_angle(angle))
    return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])


def rotation_y(angle: float) -> np.ndarray:
    """Return the 3x3 right-handed rotation about the y axis."""
    c, s = np.cos(_angle(angle)), np.sin(_angle(angle))
    return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])


def rotation_z(angle: float) -> np.ndarray:
    """Return the 3x3 right-handed rotation about the z axis."""
    c, s = np.cos(_angle(angle)), np.sin(_angle(angle))
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def _angle(value: float) -> float:
    try:
        angle = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("angle must be a finite number of radians.") from exc
    if not np.isfinite(angle):
        raise ValueError("angle must be a finite number of radians.")
    return angle


def _triple(value: object, name: str) -> np.ndarray:
    try:
        result = np.asarray(value, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain three finite numbers.") from exc
    if result.shape != (3,) or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain three finite numbers.")
    return result


def translation(x: float, y: float, z: float) -> np.ndarray:
    """Return a 4x4 homogeneous translation matrix."""
    offset = _triple((x, y, z), "translation")
    result = np.eye(4)
    result[:3, 3] = offset
    return result


def scale(x: float, y: float | None = None, z: float | None = None) -> np.ndarray:
    """Return a 4x4 homogeneous scale matrix (uniform when only x is given)."""
    if y is None and z is None:
        factors = np.full(3, float(x))
    elif y is None or z is None:
        raise ValueError("Provide either one uniform scale or all three axis scales.")
    else:
        factors = _triple((x, y, z), "scale")
    if not np.all(np.isfinite(factors)):
        raise ValueError("scale factors must be finite.")
    result = np.eye(4)
    result[:3, :3] = np.diag(factors)
    return result


def transform(matrix: object, point: object) -> np.ndarray:
    """Apply a 4x4 homogeneous transform to a 3D point or an array of points."""
    try:
        value = np.asarray(matrix, dtype=float)
        points = np.asarray(point, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("matrix and point(s) must contain finite numbers.") from exc
    if value.shape != (4, 4) or not np.all(np.isfinite(value)):
        raise ValueError("matrix must be a finite 4x4 homogeneous matrix.")
    if points.ndim == 1:
        if points.shape != (3,):
            raise ValueError("point must have three coordinates.")
        single = True
        points = points[None, :]
    elif points.ndim == 2 and points.shape[1] == 3:
        single = False
    else:
        raise ValueError("points must have shape (3,) or (n, 3).")
    if not np.all(np.isfinite(points)):
        raise ValueError("point(s) must be finite.")
    homogeneous = np.column_stack((points, np.ones(len(points))))
    result = (value @ homogeneous.T).T
    w = result[:, 3]
    if np.any(np.isclose(w, 0.0)):
        raise ValueError("Transform maps a point to infinity.")
    cartesian = result[:, :3] / w[:, None]
    return cartesian[0] if single else cartesian
