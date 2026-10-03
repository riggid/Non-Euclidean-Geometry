"""Application entry point."""

import sys
from pathlib import Path

import numpy as np
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTableWidgetItem

from .controllers.comparison_controller import ComparisonController
from .controllers.geometry_controller import GeometryController
from .controllers.point_controller import PointController
from .visualization.canvas import GeometryCanvas


def load_ui():
    """Load the main.ui file relative to this package."""
    ui_path = Path(__file__).parent / "ui" / "main.ui"
    ui_file = QFile(str(ui_path))
    if not ui_file.open(QIODevice.ReadOnly):
        raise RuntimeError(f"Cannot open {ui_path}: {ui_file.errorString()}")
    loader = QUiLoader()
    # Register the promoted widget class so QUiLoader can instantiate it
    loader.registerCustomWidget(GeometryCanvas)
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        raise RuntimeError(loader.errorString())
    return window


def main():
    """Launch the Non-Euclidean Geometry Visualizer."""
    app = QApplication(sys.argv)
    window = load_ui()

    # --- Wire up controllers ---
    canvas = window.graphicsView  # Already a GeometryCanvas via widget promotion
    point_ctrl = PointController()
    geo_ctrl = GeometryController(canvas)
    comp_ctrl = ComparisonController()

    # Populate results table with default labels
    _init_results_table(window.resultsTable)

    # --- Connect signals ---
    def on_geometry_changed(name: str) -> None:
        geo_ctrl.set_geometry(name)

    def on_calculate() -> None:
        A = np.array([window.spinAX.value(), window.spinAY.value()])
        B = np.array([window.spinBX.value(), window.spinBY.value()])
        C = np.array([window.spinCX.value(), window.spinCY.value()])
        point_ctrl.set_point("A", A)
        point_ctrl.set_point("B", B)
        point_ctrl.set_point("C", C)
        geo_ctrl.set_points(A, B, C)
        result = geo_ctrl.calculate_triangle()
        if result is not None:
            _populate_results(window.resultsTable, result)

    def on_compare() -> None:
        A = np.array([window.spinAX.value(), window.spinAY.value()])
        B = np.array([window.spinBX.value(), window.spinBY.value()])
        C = np.array([window.spinCX.value(), window.spinCY.value()])
        results = comp_ctrl.compare(A, B, C)
        # TODO: populate comparison view once team implements geometry modules

    window.comboGeometry.currentTextChanged.connect(on_geometry_changed)
    window.btnCalculate.clicked.connect(on_calculate)
    window.btnCompare.clicked.connect(on_compare)

    # Set initial geometry
    geo_ctrl.set_geometry(window.comboGeometry.currentText())

    window.show()
    sys.exit(app.exec())


def _init_results_table(table) -> None:
    """Set up the results table with default row labels."""
    labels = ["Dist AB", "Dist BC", "Dist CA", "Angle Sum", "Curvature"]
    for row, label in enumerate(labels):
        table.setItem(row, 0, QTableWidgetItem(label))
    table.setHorizontalHeaderLabels(["Property", "Value", "Property", "Value"])


def _populate_results(table, result) -> None:
    """Fill the results table from a TriangleResult object."""
    # TODO: adapt once team defines TriangleResult in core/types.py
    pass


if __name__ == "__main__":
    main()
