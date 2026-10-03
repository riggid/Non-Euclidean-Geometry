"""Hyperbolic geometry renderer — Poincaré disk model.

Draws the unit disk boundary and geodesic arcs (circular arcs orthogonal to
the boundary) as QPainterPath curves.
"""

from __future__ import annotations

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPainterPath, QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsScene

from ..core.constants import CANVAS_SIZE, POINT_RADIUS
from .renderer import GeometryRenderer

_ARC_COLOR = QColor("#ff9f43")
_BOUNDARY_COLOR = QColor("#555555")
_POINT_COLOR = QColor("#ff9f43")
_LABEL_COLOR = QColor("#ffffff")
_POINT_LABELS = ["A", "B", "C"]

_DISK_RADIUS = CANVAS_SIZE * 0.45


class HyperbolicRenderer(GeometryRenderer):
    """Renders hyperbolic geometry inside the Poincaré disk.

    The unit disk boundary is drawn as a permanent circle. Geodesics are
    rendered as smooth curves by connecting the pre-computed sample points
    (already projected into disk coordinates by the geometry module) with
    a QPainterPath.

    Coordinates received from the geometry module are expected to be in
    the range (-1, 1) (Poincaré disk coordinates) and are scaled to
    ``_DISK_RADIUS`` for display.
    """

    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__(scene)
        self._items: list[QGraphicsItem] = []
        self._draw_boundary()

    # ------------------------------------------------------------------
    # Boundary
    # ------------------------------------------------------------------

    def _draw_boundary(self) -> None:
        """Draw the Poincaré disk boundary circle."""
        pen = QPen(_BOUNDARY_COLOR, 2.0)
        brush = QBrush(QColor(20, 20, 35, 200))
        r = _DISK_RADIUS
        circle = self._scene.addEllipse(-r, -r, 2 * r, 2 * r, pen, brush)
        circle.setZValue(-1)

    # ------------------------------------------------------------------
    # Coordinate helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_scene(point: np.ndarray) -> tuple[float, float]:
        """Scale a Poincaré disk point to scene pixel coordinates."""
        return float(point[0]) * _DISK_RADIUS, float(point[1]) * _DISK_RADIUS

    # ------------------------------------------------------------------
    # GeometryRenderer interface
    # ------------------------------------------------------------------

    def render_points(self, points: list[np.ndarray]) -> None:
        pen = QPen(Qt.NoPen)
        brush = QBrush(_POINT_COLOR)
        r = POINT_RADIUS

        for i, p in enumerate(points):
            sx, sy = self._to_scene(p)
            ellipse = self._scene.addEllipse(sx - r, sy - r, 2 * r, 2 * r, pen, brush)
            self._items.append(ellipse)

            label_text = _POINT_LABELS[i] if i < len(_POINT_LABELS) else str(i)
            text = self._scene.addText(label_text)
            text.setDefaultTextColor(_LABEL_COLOR)
            text.setPos(sx + r + 2, sy - r)
            self._items.append(text)

    def render_geodesic(self, path_points: np.ndarray) -> None:
        """Draw a hyperbolic geodesic as a smooth path through the disk."""
        if len(path_points) < 2:
            return

        path = QPainterPath()
        sx, sy = self._to_scene(path_points[0])
        path.moveTo(sx, sy)
        for pt in path_points[1:]:
            sx, sy = self._to_scene(pt)
            path.lineTo(sx, sy)

        pen = QPen(_ARC_COLOR, 2.0)
        item = self._scene.addPath(path, pen)
        self._items.append(item)

    def render_triangle(
        self,
        points: list[np.ndarray],
        geodesics: list[np.ndarray],
    ) -> None:
        for geodesic in geodesics:
            self.render_geodesic(geodesic)
        self.render_points(points)

    def clear(self) -> None:
        for item in self._items:
            self._scene.removeItem(item)
        self._items.clear()
