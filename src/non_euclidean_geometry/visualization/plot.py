"""Plotly figure builders for the geometry visualizer.

Replaces the old Qt QGraphicsScene renderers: all grid, boundary, point,
and geodesic drawing now happens declaratively as Plotly traces/shapes.
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

# Palette sampled from "Pasted image.png" (the dark SPC dashboard reference).
_GEOMETRY_COLORS = {
    "Euclidean": "#f0da76",   # soft yellow sparklines/markers
    "Spherical": "#c3ede4",   # pale mint-teal pass bars
    "Hyperbolic": "#d76569",  # salmon-red pie wedges / OOC markers
}
_POINT_LABELS = ["A", "B", "C"]

_BG = "#080d1b"
_GRID = "#39475c"
_AXIS = "#4a577a"


def build_figure(
    geometry: str,
    points: list[np.ndarray] | None = None,
    geodesics: list[np.ndarray] | None = None,
) -> go.Figure:
    """Build a Plotly figure for the given geometry.

    Args:
        geometry: "Euclidean", "Spherical", or "Hyperbolic".
        points:   Optional list of vertex coordinate arrays.
        geodesics: Optional list of (n, 2) sampled geodesic paths.
    """
    color = _GEOMETRY_COLORS.get(geometry, "#f7dc6f")
    is_disk = geometry in ("Hyperbolic", "Spherical")
    half = 1.3 if is_disk else 10.5
    step = 0.25 if is_disk else 2.0

    fig = go.Figure()

    # --- Grid + axes (permanent background) ---
    for k in np.arange(-half + step, half, step):
        fig.add_shape(type="line", x0=k, y0=-half, x1=k, y1=half,
                      line=dict(color=_GRID, width=1), layer="below")
        fig.add_shape(type="line", x0=-half, y0=k, x1=half, y1=k,
                      line=dict(color=_GRID, width=1), layer="below")
    fig.add_shape(type="line", x0=-half, y0=0, x1=half, y1=0,
                  line=dict(color=_AXIS, width=1.5), layer="below")
    fig.add_shape(type="line", x0=0, y0=-half, x1=0, y1=half,
                  line=dict(color=_AXIS, width=1.5), layer="below")

    # --- Geometry boundary ---
    if is_disk:
        dash = "dot" if geometry == "Spherical" else "solid"
        fig.add_shape(type="circle", x0=-1, y0=-1, x1=1, y1=1,
                      line=dict(color="#4a577a", width=2, dash=dash),
                      fillcolor="rgba(57,71,92,0.30)", layer="below")

    # --- Geodesics ---
    if geodesics:
        for path in geodesics:
            arr = np.asarray(path, dtype=float)
            if len(arr) < 2:
                continue
            fig.add_trace(go.Scatter(
                x=arr[:, 0], y=arr[:, 1], mode="lines",
                line=dict(color=color, width=2.5),
                name=geometry, showlegend=False,
            ))

    # --- Points ---
    if points:
        pts = np.asarray(points, dtype=float)
        labels = [_POINT_LABELS[i] if i < len(_POINT_LABELS) else str(i)
                  for i in range(len(pts))]
        fig.add_trace(go.Scatter(
            x=pts[:, 0], y=pts[:, 1], mode="markers+text",
            marker=dict(color=color, size=12, line=dict(color="white", width=1)),
            text=labels, textposition="top right",
            textfont=dict(color="white", size=14),
            name="Vertices", showlegend=False,
        ))

    fig.update_layout(
        plot_bgcolor=_BG,
        paper_bgcolor=_BG,
        xaxis=dict(range=[-half, half], showgrid=False, zeroline=False,
                   tickfont=dict(color="#b1b0b2"), constrain="domain"),
        yaxis=dict(range=[-half, half], showgrid=False, zeroline=False,
                   tickfont=dict(color="#b1b0b2"), scaleanchor="x",
                   scaleratio=1),
        margin=dict(l=20, r=20, t=20, b=20),
        dragmode="pan",
    )
    return fig
