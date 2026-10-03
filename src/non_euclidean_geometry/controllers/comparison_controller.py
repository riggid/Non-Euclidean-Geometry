"""Comparison controller.

Runs all three geometry implementations on the same three points and
collects the results for side-by-side display.

The actual geometry instances are injected after the team implements
geometry/euclidean.py, spherical.py, and hyperbolic.py.
"""

from __future__ import annotations

from typing import Any

import numpy as np


class ComparisonController:
    """Runs all three geometries on the same points and returns a result dict.

    Usage (once the team has implemented the geometry modules):
        from ..geometry.euclidean import EuclideanGeometry
        from ..geometry.spherical import SphericalGeometry
        from ..geometry.hyperbolic import HyperbolicGeometry

        ctrl = ComparisonController(
            euclidean=EuclideanGeometry(),
            spherical=SphericalGeometry(),
            hyperbolic=HyperbolicGeometry(),
        )
        results = ctrl.compare(A, B, C)
        # results == {
        #     "Euclidean":  TriangleResult(...),
        #     "Spherical":  TriangleResult(...),
        #     "Hyperbolic": TriangleResult(...),
        # }

    Args:
        euclidean:  EuclideanGeometry instance (or None until implemented).
        spherical:  SphericalGeometry instance (or None until implemented).
        hyperbolic: HyperbolicGeometry instance (or None until implemented).
    """

    def __init__(
        self,
        euclidean: Any = None,
        spherical: Any = None,
        hyperbolic: Any = None,
    ) -> None:
        self._geometries: dict[str, Any] = {
            "Euclidean": euclidean,
            "Spherical": spherical,
            "Hyperbolic": hyperbolic,
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register_geometry(self, name: str, geometry: Any) -> None:
        """Register or replace a geometry instance.

        Call this from main.py once the team's geometry classes are ready:

            ctrl.register_geometry("Euclidean", EuclideanGeometry())

        Args:
            name:     Display name — "Euclidean", "Spherical", or "Hyperbolic".
            geometry: An object implementing the Geometry interface.
        """
        self._geometries[name] = geometry

    def compare(
        self,
        A: np.ndarray,
        B: np.ndarray,
        C: np.ndarray,
    ) -> dict[str, Any]:
        """Run triangle analysis across all registered geometries.

        Args:
            A, B, C: The three triangle vertices as 2-D arrays.

        Returns:
            Dict mapping geometry name → TriangleResult (or None if that
            geometry hasn't been implemented yet).
        """
        results: dict[str, Any] = {}
        for name, geometry in self._geometries.items():
            if geometry is None:
                results[name] = None
            else:
                try:
                    results[name] = geometry.triangle(A, B, C)
                except Exception as exc:  # noqa: BLE001
                    results[name] = f"Error: {exc}"
        return results

    def available_geometries(self) -> list[str]:
        """Return names of geometry instances that have been registered."""
        return [name for name, g in self._geometries.items() if g is not None]
