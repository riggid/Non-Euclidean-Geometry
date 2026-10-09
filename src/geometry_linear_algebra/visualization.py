"""
Visualization Helpers using Plotly
Provides interactive 2D and 3D plotting routines for Streamlit.

Figures are styled to match the app's dark Streamlit theme
(background #0e1117, secondary #1e2129, text #fafafa) so that axes,
gridlines, labels, legends and annotations stay legible on dark panels.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .spherical import spherical_great_circle_arc
from .hyperbolic import poincare_projection, poincare_geodesic_arc

# --- Dark theme palette (mirrors .streamlit/config.toml) ---
BG_COLOR = '#0e1117'          # Streamlit backgroundColor
PANEL_COLOR = '#1e2129'       # Streamlit secondaryBackgroundColor
TEXT_COLOR = '#fafafa'        # Streamlit textColor
GRID_COLOR = '#2d3340'
ZEROLINE_COLOR = '#5a6270'
PRIMARY_COLOR = '#ff4b4b'     # Streamlit primaryColor

# Geometry-specific accents kept distinct from one another
ORIGINAL_BLUE = '#4da3ff'     # brightened for contrast on dark panels
SPHERE_BLUE = '#4da3ff'
GEODESIC_RED = PRIMARY_COLOR
GEODESIC_MAGENTA = '#ff6bd6'
VERTEX_COLORS = ['#ffd54a', '#ff9f45', '#4dd6e8']  # yellow / orange / cyan


def _base_layout(title: str, height: int = 450) -> dict:
    """Shared dark-theme layout options for all figures."""
    return dict(
        title=dict(text=title, font=dict(size=16, color=TEXT_COLOR)),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=PANEL_COLOR,
        font=dict(color=TEXT_COLOR),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=height,
    )


def create_euclidean_plotly_fig(A: np.ndarray, B: np.ndarray, C: np.ndarray, R: np.ndarray = None, title: str = "Euclidean 2D Plane"):
    """Creates a 2D Plotly figure for Euclidean triangle rotation."""
    fig = go.Figure()

    # Original Triangle
    orig_x = [A[0], B[0], C[0], A[0]]
    orig_y = [A[1], B[1], C[1], A[1]]

    fig.add_trace(go.Scatter(
        x=orig_x, y=orig_y,
        mode='lines+markers+text',
        name='Original Triangle ABC',
        line=dict(color=ORIGINAL_BLUE, width=3),
        marker=dict(size=10, color=ORIGINAL_BLUE),
        text=['A', 'B', 'C', ''],
        textposition='top center',
        textfont=dict(color=TEXT_COLOR)
    ))

    # Rotated Triangle if R provided
    if R is not None:
        A_rot = R @ A
        B_rot = R @ B
        C_rot = R @ C
        rot_x = [A_rot[0], B_rot[0], C_rot[0], A_rot[0]]
        rot_y = [A_rot[1], B_rot[1], C_rot[1], A_rot[1]]

        fig.add_trace(go.Scatter(
            x=rot_x, y=rot_y,
            mode='lines+markers+text',
            name="Rotated Triangle A'B'C'",
            line=dict(color=PRIMARY_COLOR, width=3, dash='dash'),
            marker=dict(size=10, color=PRIMARY_COLOR),
            text=["A'", "B'", "C'", ''],
            textposition='top center',
            textfont=dict(color=TEXT_COLOR)
        ))

    layout = _base_layout(title)
    layout.update(
        xaxis=dict(
            range=[-2.5, 2.5], zeroline=True, zerolinecolor=ZEROLINE_COLOR,
            gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR),
            title=dict(font=dict(color=TEXT_COLOR))
        ),
        yaxis=dict(
            range=[-2.5, 2.5], zeroline=True, zerolinecolor=ZEROLINE_COLOR,
            gridcolor=GRID_COLOR, scaleanchor="x", scaleratio=1,
            tickfont=dict(color=TEXT_COLOR), title=dict(font=dict(color=TEXT_COLOR))
        ),
    )
    fig.update_layout(**layout)
    return fig

def create_spherical_plotly_fig(A: np.ndarray, B: np.ndarray, C: np.ndarray, title: str = "Spherical Triangle on S² (pᵀp = 1)"):
    """Creates a 3D Plotly figure for spherical triangle with great-circle arcs on unit sphere."""
    fig = go.Figure()

    # Wireframe Sphere Surface
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        opacity=0.22,
        colorscale=[[0, SPHERE_BLUE], [1, SPHERE_BLUE]],
        showscale=False,
        name='Unit Sphere S²',
        hoverinfo='skip'
    ))

    # Vertices A, B, C
    pts = np.array([A, B, C])
    fig.add_trace(go.Scatter3d(
        x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
        mode='markers+text',
        name='Vertices A, B, C',
        marker=dict(size=8, color=VERTEX_COLORS),
        text=['A', 'B', 'C'],
        textposition='top center',
        textfont=dict(color=TEXT_COLOR, size=14)
    ))

    # Great-circle Geodesic Arcs AB, BC, CA
    arc_AB = spherical_great_circle_arc(A, B)
    arc_BC = spherical_great_circle_arc(B, C)
    arc_CA = spherical_great_circle_arc(C, A)

    for arc, label in zip([arc_AB, arc_BC, arc_CA], ['Arc AB', 'Arc BC', 'Arc CA']):
        fig.add_trace(go.Scatter3d(
            x=arc[:, 0], y=arc[:, 1], z=arc[:, 2],
            mode='lines',
            name=label,
            line=dict(color=GEODESIC_RED, width=6)
        ))

    layout = _base_layout(title)
    layout['margin'] = dict(l=10, r=10, t=40, b=10)
    axis_style = dict(
        range=[-1.2, 1.2], backgroundcolor=PANEL_COLOR, gridcolor=GRID_COLOR,
        zerolinecolor=ZEROLINE_COLOR, tickfont=dict(color=TEXT_COLOR),
        title=dict(font=dict(color=TEXT_COLOR)), showbackground=True
    )
    layout['scene'] = dict(
        xaxis=dict(axis_style), yaxis=dict(axis_style), zaxis=dict(axis_style),
        aspectmode='cube'
    )
    fig.update_layout(**layout)
    return fig

def create_hyperbolic_plotly_fig(A: np.ndarray, B: np.ndarray, C: np.ndarray, title: str = "Poincaré Disk (Hyperbolic Geodesics)"):
    """Creates a 2D Plotly figure for hyperbolic triangle on the Poincaré disk with curved geodesics."""
    fig = go.Figure()

    # Boundary Unit Circle |z| = 1
    theta = np.linspace(0, 2 * np.pi, 200)
    circle_x = np.cos(theta)
    circle_y = np.sin(theta)

    fig.add_trace(go.Scatter(
        x=circle_x, y=circle_y,
        mode='lines',
        name='Boundary Circle |z| = 1',
        line=dict(color=TEXT_COLOR, width=2, dash='dash')
    ))

    # Project vertices to Poincaré disk
    u_A = poincare_projection(A)
    u_B = poincare_projection(B)
    u_C = poincare_projection(C)

    pts = np.array([u_A, u_B, u_C])
    fig.add_trace(go.Scatter(
        x=pts[:, 0], y=pts[:, 1],
        mode='markers+text',
        name='Vertices A, B, C',
        marker=dict(size=12, color=VERTEX_COLORS),
        text=['A', 'B', 'C'],
        textposition='top center',
        textfont=dict(color=TEXT_COLOR)
    ))

    # Geodesic Arcs AB, BC, CA
    arc_AB = poincare_geodesic_arc(A, B)
    arc_BC = poincare_geodesic_arc(B, C)
    arc_CA = poincare_geodesic_arc(C, A)

    for arc, label in zip([arc_AB, arc_BC, arc_CA], ['Geodesic AB', 'Geodesic BC', 'Geodesic CA']):
        fig.add_trace(go.Scatter(
            x=arc[:, 0], y=arc[:, 1],
            mode='lines',
            name=label,
            line=dict(color=GEODESIC_MAGENTA, width=3)
        ))

    layout = _base_layout(title)
    layout.update(
        xaxis=dict(
            range=[-1.15, 1.15], zeroline=True, zerolinecolor=ZEROLINE_COLOR,
            gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR),
            title=dict(font=dict(color=TEXT_COLOR))
        ),
        yaxis=dict(
            range=[-1.15, 1.15], zeroline=True, zerolinecolor=ZEROLINE_COLOR,
            gridcolor=GRID_COLOR, scaleanchor="x", scaleratio=1,
            tickfont=dict(color=TEXT_COLOR), title=dict(font=dict(color=TEXT_COLOR))
        ),
    )
    fig.update_layout(**layout)
    return fig
