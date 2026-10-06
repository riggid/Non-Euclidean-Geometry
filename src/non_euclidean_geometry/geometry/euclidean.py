"""Euclidean geometry in the ordinary two-dimensional plane."""

from __future__ import annotations

import numpy as np

from ..core.constants import DEFAULT_GEODESIC_SAMPLES, EPSILON, PI
from ..core.exceptions import DegenerateTriangleError, InvalidPointError
from ..core.types import TriangleResult


class EuclideanGeometry:
    """Distance, angle, geodesic, and triangle operations in the plane."""

    curvature_value = 0.0

    @staticmethod
    def _point(point: np.ndarray, name: str = "point") -> np.ndarray:
        """Return a validated finite two-dimensional point."""
        try:
            value = np.asarray(point, dtype=float)
        except (TypeError, ValueError) as exc:
            raise InvalidPointError(f"{name} must be a finite 2-D point.") from exc
        if value.shape != (2,) or not np.all(np.isfinite(value)):
            raise InvalidPointError(f"{name} must be a finite 2-D point.")
        return value

    def curvature(self) -> float:
        """Return the constant Gaussian curvature of the Euclidean plane."""
        return self.curvature_value

    def distance(self, P: np.ndarray, Q: np.ndarray) -> float:
        """Return the Euclidean distance between two points."""
        p = self._point(P, "P")
        q = self._point(Q, "Q")
        return float(np.linalg.norm(q - p))

    def angle(self, A: np.ndarray, B: np.ndarray, C: np.ndarray) -> float:
        """Return angle ABC in radians, with B as the vertex."""
        a = self._point(A, "A") - self._point(B, "B")
        c = self._point(C, "C") - self._point(B, "B")
        norm_a = float(np.linalg.norm(a))
        norm_c = float(np.linalg.norm(c))
        norm_product = norm_a * norm_c
        if norm_a <= EPSILON or norm_c <= EPSILON:
            raise DegenerateTriangleError("An angle cannot have coincident vertices.")
        cosine = float(np.dot(a, c) / norm_product)
        return float(np.arccos(np.clip(cosine, -1.0, 1.0)))

    def geodesic(
        self,
        P: np.ndarray,
        Q: np.ndarray,
        n_samples: int = DEFAULT_GEODESIC_SAMPLES,
    ) -> np.ndarray:
        """Sample the straight-line geodesic from P to Q, including endpoints."""
        p = self._point(P, "P")
        q = self._point(Q, "Q")
        if isinstance(n_samples, bool) or not isinstance(n_samples, (int, np.integer)) or n_samples < 2:
            raise ValueError("n_samples must be an integer of at least 2.")
        t = np.linspace(0.0, 1.0, int(n_samples))[:, None]
        return p + t * (q - p)

    def triangle(self, A: np.ndarray, B: np.ndarray, C: np.ndarray) -> TriangleResult:
        """Measure a nondegenerate triangle and return its three sides and angles."""
        a = self._point(A, "A")
        b = self._point(B, "B")
        c = self._point(C, "C")
        ab = self.distance(a, b)
        bc = self.distance(b, c)
        ca = self.distance(c, a)
        ab_vector = b - a
        ac_vector = c - a
        twice_area = abs(float(ab_vector[0] * ac_vector[1] - ab_vector[1] * ac_vector[0]))
        if (
            min(ab, bc, ca) <= EPSILON
            or twice_area <= EPSILON * ab * ca
        ):
            raise DegenerateTriangleError("Triangle vertices must be distinct and non-collinear.")
        angles = {
            "A": self.angle(b, a, c),
            "B": self.angle(a, b, c),
            "C": self.angle(a, c, b),
        }
        return TriangleResult(
            side_lengths={"AB": ab, "BC": bc, "CA": ca},
            angles=angles,
            angle_sum=PI,
            curvature=self.curvature(),
        )
