"""Geometry orchestration controller.

Bridges the UI (geometry selector, calculate button) with the geometry
modules and the renderer. When the team implements a geometry class,
register it in GEOMETRY_REGISTRY below.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from ..visualization.canvas import GeometryCanvas
from ..visualization.euclidean_renderer import EuclideanRenderer
from ..visualization.hyperbolic_renderer import HyperbolicRenderer
from ..visualization.spherical_renderer import SphericalRenderer
from ..geometry.euclidean import EuclideanGeometry

# Map combo-box display names to renderer classes.
# Geometry instances (from geometry/) are injected after the team implements them.
_RENDERER_MAP = {
    "Euclidean": EuclideanRenderer,
    "Spherical": SphericalRenderer,
    "Hyperbolic": HyperbolicRenderer,
}


class GeometryController:
    """Orchestrates geometry selection, triangle calculation, and rendering.

    Usage (from main.py after load_ui):
        canvas = GeometryCanvas()
        ctrl = GeometryController(canvas)
        ctrl.set_geometry("Euclidean")
        ctrl.set_points(A, B, C)
        result = ctrl.calculate_triangle()

    Args:
        canvas: The central GeometryCanvas widget.
    """

    def __init__(self, canvas: GeometryCanvas) -> None:
        self._canvas = canvas
        self._geometry: Any = EuclideanGeometry()
        self._points: dict[str, np.ndarray] = {}
        self._current_geometry_name: str = "Euclidean"
        self._renderer = EuclideanRenderer(canvas.scene())
        canvas.set_renderer(self._renderer)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_geometry(self, name: str) -> None:
        """Switch to a different geometry type and swap the renderer.

        Args:
            name: One of "Euclidean", "Spherical", "Hyperbolic".
        """
        if name not in _RENDERER_MAP:
            raise ValueError(f"Unknown geometry: {name!r}. "
                             f"Valid options: {list(_RENDERER_MAP)}")

        self._current_geometry_name = name
        renderer_cls = _RENDERER_MAP[name]
        self._renderer = renderer_cls(self._canvas.scene())
        self._canvas.set_renderer(self._renderer)
        # Only the Euclidean model is implemented so far; other selections
        # retain the existing preview behavior until their geometry is added.
        self._geometry = EuclideanGeometry() if name == "Euclidean" else None

    def set_points(
        self,
        A: np.ndarray,
        B: np.ndarray,
        C: np.ndarray,
    ) -> None:
        """Store the three triangle vertices.

        Args:
            A, B, C: 2-D coordinate arrays.
        """
        self._points = {"A": A, "B": B, "C": C}

    def calculate_triangle(self) -> Any:
        """Run the triangle calculation for the current geometry.

        Returns:
            A TriangleResult (once the team implements geometry/base.py and
            the concrete geometry classes). Currently returns None.

        Raises:
            RuntimeError: If points have not been set yet.
        """
        if len(self._points) < 3:
            raise RuntimeError("Set points A, B, C before calculating.")

        if self._geometry is None:
            # Geometry not yet implemented — render the raw points as a preview
            pts = [self._points["A"], self._points["B"], self._points["C"]]
            self._renderer.clear()
            self._renderer.render_points(pts)
            return None

        A, B, C = self._points["A"], self._points["B"], self._points["C"]
        result = self._geometry.triangle(A, B, C)

        geodesics = [
            self._geometry.geodesic(A, B),
            self._geometry.geodesic(B, C),
            self._geometry.geodesic(C, A),
        ]

        self._renderer.clear()
        self._renderer.render_triangle([A, B, C], geodesics)
        return result

    def get_current_geometry_name(self) -> str:
        """Return the name of the currently selected geometry."""
        return self._current_geometry_name
