"""
Visualization Helpers using Plotly
Provides interactive 2D and 3D plotting routines for Streamlit.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .spherical import spherical_great_circle_arc
from .hyperbolic import poincare_projection, poincare_geodesic_arc

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
        line=dict(color='blue', width=3),
        marker=dict(size=10, color='blue'),
        text=['A', 'B', 'C', ''],
        textposition='top center'
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
            line=dict(color='red', width=3, dash='dash'),
            marker=dict(size=10, color='red'),
            text=["A'", "B'", "C'", ''],
            textposition='top center'
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='white')),
        xaxis=dict(range=[-2.5, 2.5], zeroline=True, zerolinecolor='gray', gridcolor='#333333'),
        yaxis=dict(range=[-2.5, 2.5], zeroline=True, zerolinecolor='gray', gridcolor='#333333', scaleanchor="x", scaleratio=1),
        paper_bgcolor='#111111',
        plot_bgcolor='#1e1e1e',
        legend=dict(font=dict(color='white')),
        margin=dict(l=20, r=20, t=40, b=20),
        height=450
    )
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
        opacity=0.2,
        colorscale=[[0, 'lightblue'], [1, 'lightblue']],
        showscale=False,
        name='Unit Sphere S²'
    ))

    # Vertices A, B, C
    pts = np.array([A, B, C])
    fig.add_trace(go.Scatter3d(
        x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
        mode='markers+text',
        name='Vertices A, B, C',
        marker=dict(size=8, color=['yellow', 'orange', 'cyan']),
        text=['A', 'B', 'C'],
        textposition='top center'
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
            line=dict(color='red', width=6)
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='white')),
        scene=dict(
            xaxis=dict(range=[-1.2, 1.2], backgroundcolor='#1e1e1e', gridcolor='#333333'),
            yaxis=dict(range=[-1.2, 1.2], backgroundcolor='#1e1e1e', gridcolor='#333333'),
            zaxis=dict(range=[-1.2, 1.2], backgroundcolor='#1e1e1e', gridcolor='#333333'),
            aspectmode='cube'
        ),
        paper_bgcolor='#111111',
        legend=dict(font=dict(color='white')),
        margin=dict(l=10, r=10, t=40, b=10),
        height=450
    )
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
        line=dict(color='white', width=2, dash='dash')
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
        marker=dict(size=12, color=['yellow', 'orange', 'cyan']),
        text=['A', 'B', 'C'],
        textposition='top center'
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
            line=dict(color='magenta', width=3)
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='white')),
        xaxis=dict(range=[-1.15, 1.15], zeroline=True, zerolinecolor='gray', gridcolor='#333333'),
        yaxis=dict(range=[-1.15, 1.15], zeroline=True, zerolinecolor='gray', gridcolor='#333333', scaleanchor="x", scaleratio=1),
        paper_bgcolor='#111111',
        plot_bgcolor='#1e1e1e',
        legend=dict(font=dict(color='white')),
        margin=dict(l=20, r=20, t=40, b=20),
        height=450
    )
    return fig
