"""Geometry orchestration controller.

Bridges the UI (geometry selector, calculate button) with the geometry
modules and the plot builder. Framed Qt-free so the math/state logic is
independent of the NiceGUI front end.
"""

from __future__ import annotations

from typing import Any

import numpy as np

GEOMETRY_NAMES = ("Euclidean", "Spherical", "Hyperbolic")


class GeometryController:
    """Orchestrates geometry selection, triangle calculation, and rendering.

    Usage:
        ctrl = GeometryController()
        ctrl.set_geometry("Euclidean")
        ctrl.set_points(A, B, C)
        result, geodesics = ctrl.calculate_triangle()
    """

    def __init__(self) -> None:
        self._geometry: Any = None        # Set once geometry/ modules are implemented
        self._points: dict[str, np.ndarray] = {}
        self._current_geometry_name: str = "Euclidean"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_geometry(self, name: str) -> None:
        """Switch to a different geometry type.

        Args:
            name: One of "Euclidean", "Spherical", "Hyperbolic".
        """
        if name not in GEOMETRY_NAMES:
            raise ValueError(f"Unknown geometry: {name!r}. "
                             f"Valid options: {list(GEOMETRY_NAMES)}")
        self._current_geometry_name = name
        # TODO: swap self._geometry once team implements geometry classes

    def set_points(
        self,
        A: np.ndarray,
        B: np.ndarray,
        C: np.ndarray,
    ) -> None:
        """Store the three triangle vertices."""
        self._points = {"A": A, "B": B, "C": C}

    def calculate_triangle(self) -> tuple[Any, list[np.ndarray] | None]:
        """Run the triangle calculation for the current geometry.

        Returns:
            (result, geodesics). Both are None until the geometry modules
            are implemented; the UI then renders just the raw points.

        Raises:
            RuntimeError: If points have not been set yet.
        """
        if len(self._points) < 3:
            raise RuntimeError("Set points A, B, C before calculating.")

        A, B, C = self._points["A"], self._points["B"], self._points["C"]

        if self._geometry is None:
            return None, None

        result = self._geometry.triangle(A, B, C)
        geodesics = [
            self._geometry.geodesic(A, B),
            self._geometry.geodesic(B, C),
            self._geometry.geodesic(C, A),
        ]
        return result, geodesics

    def get_current_geometry_name(self) -> str:
        """Return the name of the currently selected geometry."""
        return self._current_geometry_name

    def get_points(self) -> list[np.ndarray]:
        """Return the currently stored vertex arrays [A, B, C]."""
        return [self._points[label] for label in ("A", "B", "C")]
