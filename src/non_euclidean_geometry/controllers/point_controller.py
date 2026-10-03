"""Point state management controller.

Maintains the current A/B/C coordinate state and notifies listeners
when a point moves (e.g. from a spin box change or a mouse drag).
"""

from __future__ import annotations

from typing import Callable

import numpy as np


class PointController:
    """Manages the state of points A, B, C.

    Consumers register a callback via ``on_change`` which is called whenever
    any point moves. The GeometryController registers itself so that the
    canvas re-renders automatically on every spin-box change.

    Args:
        default_A: Initial coordinates for point A. Defaults to (-0.5, -0.5).
        default_B: Initial coordinates for point B. Defaults to (0.5, -0.5).
        default_C: Initial coordinates for point C. Defaults to (0.0,  0.5).
    """

    _DEFAULTS: dict[str, list[float]] = {
        "A": [-0.5, -0.5],
        "B": [0.5, -0.5],
        "C": [0.0, 0.5],
    }

    def __init__(
        self,
        default_A: list[float] | None = None,
        default_B: list[float] | None = None,
        default_C: list[float] | None = None,
    ) -> None:
        self._points: dict[str, np.ndarray] = {
            "A": np.array(default_A or self._DEFAULTS["A"], dtype=float),
            "B": np.array(default_B or self._DEFAULTS["B"], dtype=float),
            "C": np.array(default_C or self._DEFAULTS["C"], dtype=float),
        }
        self._callbacks: list[Callable[[], None]] = []

    # ------------------------------------------------------------------
    # Callback registration
    # ------------------------------------------------------------------

    def on_change(self, callback: Callable[[], None]) -> None:
        """Register a callable to be called whenever any point changes.

        Args:
            callback: A zero-argument callable.
        """
        self._callbacks.append(callback)

    def _notify(self) -> None:
        for cb in self._callbacks:
            cb()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_point(self, label: str, coords: np.ndarray) -> None:
        """Set the coordinates of a named point.

        Args:
            label:  "A", "B", or "C".
            coords: 2-element array.
        """
        if label not in self._points:
            raise KeyError(f"Unknown point label: {label!r}")
        self._points[label] = np.asarray(coords, dtype=float)
        self._notify()

    def get_point(self, label: str) -> np.ndarray:
        """Return the coordinates of a named point.

        Args:
            label: "A", "B", or "C".
        """
        if label not in self._points:
            raise KeyError(f"Unknown point label: {label!r}")
        return self._points[label].copy()

    def move_point(self, label: str, new_coords: np.ndarray) -> None:
        """Alias for ``set_point`` — used for drag interactions.

        Args:
            label:      "A", "B", or "C".
            new_coords: New 2-element coordinate array.
        """
        self.set_point(label, new_coords)

    def get_all_points(self) -> dict[str, np.ndarray]:
        """Return a copy of all current point coordinates keyed by label."""
        return {label: arr.copy() for label, arr in self._points.items()}

    def reset_points(self) -> None:
        """Reset all three points to their default coordinates."""
        for label, default in self._DEFAULTS.items():
            self._points[label] = np.array(default, dtype=float)
        self._notify()
