"""Abstract base renderer interface.

All concrete renderers (Euclidean, Spherical, Hyperbolic) inherit from this class.
Renderers receive pre-computed data from geometry modules — they never do math themselves.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from PySide6.QtWidgets import QGraphicsScene


class GeometryRenderer(ABC):
    """Interface every geometry-specific renderer must implement.

    A renderer takes a QGraphicsScene and draws points, geodesics and triangles
    onto it using Qt graphics items. It does not compute any geometry.

    Args:
        scene: The QGraphicsScene to draw into.
    """

    def __init__(self, scene: QGraphicsScene) -> None:
        self._scene = scene

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    def render_points(self, points: list[np.ndarray]) -> None:
        """Draw a collection of labelled points onto the scene.

        Args:
            points: List of 2-D coordinate arrays, one per point.
        """

    @abstractmethod
    def render_geodesic(self, path_points: np.ndarray) -> None:
        """Draw a single geodesic curve given its sampled points.

        Args:
            path_points: Shape (n, 2) array of scene coordinates along
                the geodesic.
        """

    @abstractmethod
    def render_triangle(
        self,
        points: list[np.ndarray],
        geodesics: list[np.ndarray],
    ) -> None:
        """Draw a complete triangle: three vertices and the three geodesic sides.

        Args:
            points:    [A, B, C] coordinate arrays.
            geodesics: Three (n, 2) arrays for sides AB, BC, CA.
        """

    @abstractmethod
    def clear(self) -> None:
        """Remove all items this renderer has added to the scene."""
