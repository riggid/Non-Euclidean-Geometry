"""QGraphicsView canvas with zoom, pan, and coordinate conversion."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QWheelEvent
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView

from ..core.constants import CANVAS_SIZE
from .renderer import GeometryRenderer


class GeometryCanvas(QGraphicsView):
    """Central visualization widget.

    Wraps a ``QGraphicsScene`` and provides:
    - Centred coordinate system (origin at canvas centre).
    - Smooth wheel zoom.
    - Middle-button pan.
    - A ``set_renderer()`` method to swap between geometry renderers.

    The canvas is designed to be embedded into the main window's
    ``graphicsView`` placeholder via ``QUiLoader`` — or used standalone.
    """

    _ZOOM_FACTOR = 1.15
    _MIN_ZOOM = 0.1
    _MAX_ZOOM = 20.0

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Scene centred on origin
        half = CANVAS_SIZE / 2
        self._scene = QGraphicsScene(-half, -half, CANVAS_SIZE, CANVAS_SIZE, self)
        self._scene.setBackgroundBrush(QBrush(QColor("#1a1a2e")))
        self.setScene(self._scene)

        self._renderer: GeometryRenderer | None = None
        self._zoom_level: float = 1.0
        self._pan_active: bool = False
        self._pan_start = None

        self._configure_view()
        self._draw_grid()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _configure_view(self) -> None:
        self.setRenderHints(self.renderHints())  # keep existing hints
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setDragMode(QGraphicsView.NoDrag)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def _draw_grid(self) -> None:
        """Draw a subtle coordinate grid as permanent background items."""
        pen_minor = self._scene.addLine(0, 0, 0, 0)  # placeholder colour
        pen_minor.hide()

        grid_color = QColor("#2a2a4a")
        step = 50
        half = CANVAS_SIZE // 2

        for x in range(-half, half + step, step):
            line = self._scene.addLine(x, -half, x, half)
            line.setPen(grid_color)
            line.setZValue(-2)

        for y in range(-half, half + step, step):
            line = self._scene.addLine(-half, y, half, y)
            line.setPen(grid_color)
            line.setZValue(-2)

        # Axis lines slightly brighter
        axis_color = QColor("#3a3a6a")
        for line_args in [
            (-half, 0, half, 0),
            (0, -half, 0, half),
        ]:
            line = self._scene.addLine(*line_args)
            line.setPen(axis_color)
            line.setZValue(-2)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_renderer(self, renderer: GeometryRenderer) -> None:
        """Swap the active renderer, clearing the previous one's items."""
        if self._renderer is not None:
            self._renderer.clear()
        self._renderer = renderer

    def scene(self) -> QGraphicsScene:  # type: ignore[override]
        return self._scene

    def to_scene_coords(self, view_x: float, view_y: float) -> tuple[float, float]:
        """Convert view (pixel) coordinates to scene coordinates."""
        pt = self.mapToScene(int(view_x), int(view_y))
        return pt.x(), pt.y()

    def to_normalised(self, scene_x: float, scene_y: float) -> tuple[float, float]:
        """Convert scene coordinates to [-1, 1] normalised coordinates."""
        half = CANVAS_SIZE / 2
        return scene_x / half, scene_y / half

    # ------------------------------------------------------------------
    # Zoom & pan event handlers
    # ------------------------------------------------------------------

    def wheelEvent(self, event: QWheelEvent) -> None:
        delta = event.angleDelta().y()
        if delta == 0:
            return

        factor = self._ZOOM_FACTOR if delta > 0 else 1.0 / self._ZOOM_FACTOR
        new_zoom = self._zoom_level * factor

        if self._MIN_ZOOM <= new_zoom <= self._MAX_ZOOM:
            self._zoom_level = new_zoom
            self.scale(factor, factor)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton:
            self._pan_active = True
            self._pan_start = event.position()
            self.setCursor(Qt.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._pan_active and self._pan_start is not None:
            delta = event.position() - self._pan_start
            self._pan_start = event.position()
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - int(delta.x())
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - int(delta.y())
            )
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton:
            self._pan_active = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)
