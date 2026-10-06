"""Application entry point — NiceGUI front end."""

import numpy as np
from nicegui import ui

from .controllers.comparison_controller import ComparisonController
from .controllers.geometry_controller import GEOMETRY_NAMES, GeometryController
from .controllers.point_controller import PointController
from .visualization.plot import build_figure

_POINT_LABELS = ["A", "B", "C"]
_RESULT_LABELS = ["Dist AB", "Dist BC", "Dist CA", "Angle Sum", "Curvature"]


def _result_rows() -> list[dict]:
    return [
        {"prop": label, "value": "—", "prop2": "", "value2": ""}
        for label in _RESULT_LABELS
    ]


@ui.page("/")
def _index() -> None:
    point_ctrl = PointController()
    geo_ctrl = GeometryController()
    comp_ctrl = ComparisonController()

    ui.dark_mode().enable()
    ui.page_title("Non-Euclidean Geometry Visualizer")
    ui.add_css("""
        body { background-color: #080d1b; }
        .card { background-color: #080d1b; border: 1px solid #1a1c30;
                border-radius: 8px; padding: 16px; }
        .accent-btn { background-color: #f0da76 !important; color: #080d1b !important; }
        .accent-btn:hover { background-color: #f7e69a !important; }
        .q-table th { background-color: #080d1b; color: #b1b0b2; }
        .q-table td { color: #e8e8f0; }
    """)

    with ui.row().classes("w-full items-start"):
        # ---------------- Control column ----------------
        with ui.column().classes("w-96 card"):
            ui.label("Geometry Type").classes("font-bold")
            combo = ui.select(list(GEOMETRY_NAMES), value="Euclidean").classes("w-full")

            spins: dict[str, tuple] = {}
            defaults = point_ctrl.get_all_points()
            for label in _POINT_LABELS:
                ui.label(f"Point {label}").classes("font-bold mt-4")
                with ui.row():
                    ui.label("X:")
                    sx = ui.number(
                        value=float(defaults[label][0]), min=-10, max=10, step=0.1,
                        format="%.2f",
                    ).classes("w-28")
                    ui.label("Y:")
                    sy = ui.number(
                        value=float(defaults[label][1]), min=-10, max=10, step=0.1,
                        format="%.2f",
                    ).classes("w-28")
                spins[label] = (sx, sy)

            ui.button("Calculate", on_click=lambda: on_calculate()).classes("mt-4 accent-btn")
            ui.button("Compare All", on_click=lambda: on_compare()).classes("accent-btn")

            results = ui.table(
                columns=[
                    {"name": "prop", "label": "Property", "field": "prop"},
                    {"name": "value", "label": "Value", "field": "value"},
                    {"name": "prop2", "label": "Property", "field": "prop2"},
                    {"name": "value2", "label": "Value", "field": "value2"},
                ],
                rows=_result_rows(),
                row_key="prop",
            ).classes("w-full mt-4")

        # ---------------- Plot column ----------------
        with ui.column().classes("grow card"):
            plot = ui.plotly(build_figure(geo_ctrl.get_current_geometry_name()))
            plot.classes("w-full h-[70vh]")

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def read_points() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return tuple(
            np.array([spins[label][0].value, spins[label][1].value], dtype=float)
            for label in _POINT_LABELS
        )

    def redraw(points=None, geodesics=None) -> None:
        plot.update_figure(
            build_figure(geo_ctrl.get_current_geometry_name(), points, geodesics)
        )

    def on_geometry_changed(event) -> None:
        geo_ctrl.set_geometry(event.value)
        redraw()

    def on_calculate() -> None:
        A, B, C = read_points()
        point_ctrl.set_point("A", A)
        point_ctrl.set_point("B", B)
        point_ctrl.set_point("C", C)
        geo_ctrl.set_points(A, B, C)
        result, geodesics = geo_ctrl.calculate_triangle()
        if result is not None:
            _populate_results(results, result)
        redraw(points=[A, B, C], geodesics=geodesics)

    def on_compare() -> None:
        A, B, C = read_points()
        comp_results = comp_ctrl.compare(A, B, C)
        available = comp_ctrl.available_geometries()
        if not available:
            ui.notify(
                "Geometry modules not yet implemented — comparison unavailable.",
                type="warning",
            )
        else:
            ui.notify(f"Compared across: {', '.join(available)}", type="info")

    combo.on_value_change(on_geometry_changed)


def main() -> None:
    """Launch the Non-Euclidean Geometry Visualizer."""
    ui.run(title="Non-Euclidean Geometry Visualizer", reload=False)


def _populate_results(table: ui.table, result) -> None:
    """Fill the results table from a TriangleResult object."""
    values = [
        result.side_lengths["AB"],
        result.side_lengths["BC"],
        result.side_lengths["CA"],
        result.angle_sum,
        result.curvature,
    ]
    for row, value in enumerate(values):
        table.setItem(row, 1, QTableWidgetItem(f"{value:.6g}"))


if __name__ == "__main__":
    main()
