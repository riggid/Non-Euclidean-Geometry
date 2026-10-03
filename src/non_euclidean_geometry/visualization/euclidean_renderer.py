"""Euclidean geometry renderer.

Draws straight lines and circular points — the simplest possible renderer.
"""

from __future__ import annotations

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsScene

from ..core.constants import POINT_RADIUS
from .renderer import GeometryRenderer

# Colour palette
_POINT_COLOR = QColor("#4a9eff")
_LINE_COLOR = QColor("#4a9eff")
_LABEL_COLOR = QColor("#ffffff")
_POINT_LABELS = ["A", "B", "C"]


class EuclideanRenderer(GeometryRenderer):
    """Renders Euclidean geometry using straight Qt graphics primitives.

    Geodesics are straight ``QGraphicsLineItem`` segments.
    Points are ``QGraphicsEllipseItem`` circles.
    """

    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__(scene)
        self._items: list[QGraphicsItem] = []

    # ------------------------------------------------------------------
    # GeometryRenderer interface
    # ------------------------------------------------------------------

    def render_points(self, points: list[np.ndarray]) -> None:
        """Draw filled circles at each point position with a letter label."""
        pen = QPen(Qt.NoPen)
        brush = QBrush(_POINT_COLOR)
        r = POINT_RADIUS

        for i, p in enumerate(points):
            x, y = float(p[0]), float(p[1])
            ellipse = self._scene.addEllipse(x - r, y - r, 2 * r, 2 * r, pen, brush)
            self._items.append(ellipse)

            label_text = _POINT_LABELS[i] if i < len(_POINT_LABELS) else str(i)
            text = self._scene.addText(label_text)
            text.setDefaultTextColor(_LABEL_COLOR)
            text.setPos(x + r + 2, y - r)
            self._items.append(text)

    def render_geodesic(self, path_points: np.ndarray) -> None:
        """Draw the geodesic as a single straight line from first to last point.

        In Euclidean geometry the geodesic is a straight line, so only the
        endpoints are needed regardless of how many samples are provided.
        """
        if len(path_points) < 2:
            return
        pen = QPen(_LINE_COLOR, 2.0)
        x1, y1 = float(path_points[0, 0]), float(path_points[0, 1])
        x2, y2 = float(path_points[-1, 0]), float(path_points[-1, 1])
        line = self._scene.addLine(x1, y1, x2, y2, pen)
        self._items.append(line)

    def render_triangle(
        self,
        points: list[np.ndarray],
        geodesics: list[np.ndarray],
    ) -> None:
        """Draw all three sides then the vertices on top."""
        for geodesic in geodesics:
            self.render_geodesic(geodesic)
        self.render_points(points)

    def clear(self) -> None:
        """Remove all items this renderer has added to the scene."""
        for item in self._items:
            self._scene.removeItem(item)
        self._items.clear()
