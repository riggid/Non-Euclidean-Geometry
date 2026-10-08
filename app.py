"""
Streamlit Scientific Dashboard Application
Linear Algebraic Transformations in Euclidean and Non-Euclidean Geometries
UE25MA242A - Mathematical Foundations for AI & Data Science
"""

import streamlit as st
import numpy as np
import pandas as pd

from geometry_linear_algebra.linalg import (
    matrix_vector_mult,
    dot_product,
    vector_norm,
    minkowski_product,
    check_matrix_preservation,
    H_METRIC
)
from geometry_linear_algebra.euclidean import (
    euclidean_rotation_matrix,
    euclidean_distance,
    euclidean_triangle_angles,
    euclidean_triangle_area
)
from geometry_linear_algebra.spherical import (
    spherical_rotation_matrix_z,
    spherical_rotation_matrix_y,
    latlon_to_cartesian,
    spherical_distance,
    elliptic_distance,
    spherical_triangle_angles
)
from geometry_linear_algebra.hyperbolic import (
    lorentz_boost_x,
    hyperboloid_point_from_disk,
    hyperbolic_distance,
    poincare_projection,
    hyperbolic_triangle_angles
)
from geometry_linear_algebra.visualization import (
    create_euclidean_plotly_fig,
    create_spherical_plotly_fig,
    create_hyperbolic_plotly_fig
)

# Streamlit Page Config
st.set_page_config(
    page_title="Linear Algebra & Geometries",
    page_icon="📐",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e222d; padding: 15px; border-radius: 8px; }
    h1, h2, h3 { color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

st.title("📐 Linear Algebraic Transformations in Geometries")
st.caption("UE25MA242A – Mathematical Foundations for AI & Data Science")

# Main Navigation Tabs
tab_euc, tab_sph, tab_hyp, tab_cmp = st.tabs([
    "📐 1. Euclidean", 
    "🌐 2. Elliptic (Spherical Model)", 
    "🌀 3. Hyperbolic", 
    "📊 4. Compare All"
])

# ==============================================================================
# TAB 1: EUCLIDEAN GEOMETRY
# ==============================================================================
with tab_euc:
    st.header(r"1. Euclidean Geometry ($\mathbb{E}^2$) — Orthogonal Transformations")
    st.markdown(r"Demonstrates 2D vector transformations under orthogonal rotation matrices $R(\theta) \in SO(2)$ where $R^T R = I_2$.")

    col_ctrl, col_viz = st.columns([1, 2])

    with col_ctrl:
        st.subheader("Interactive Control")
        theta_deg = st.slider("Rotation Angle θ (degrees):", min_value=-180.0, max_value=180.0, value=45.0, step=5.0)

        # Base Triangle
        A = np.array([0.0, 0.0])
        B = np.array([1.5, 0.0])
        C = np.array([0.5, 1.2])

        R = euclidean_rotation_matrix(theta_deg)
        R_T_R, max_diff = check_matrix_preservation(R, np.eye(2))

        st.markdown(r"### Matrix Preservation ($R^T R = I_2$)")
        st.code(f"R(θ) =\n{R}\n\nRᵀ R =\n{R_T_R}\nMax Dev = {max_diff:.2e}", language="text")

    with col_viz:
        fig_euc = create_euclidean_plotly_fig(A, B, C, R=R, title=f"Euclidean Triangle Rotation ({theta_deg:.1f}°)")
        st.plotly_chart(fig_euc, width="stretch")

    st.markdown("---")
    st.subheader("Mathematical Results & Isometry Verification")
    
    A_rot, B_rot, C_rot = R @ A, R @ B, R @ C
    ang_A, ang_B, ang_C, sum_orig = euclidean_triangle_angles(A, B, C)
    r_A, r_B, r_C, sum_rot = euclidean_triangle_angles(A_rot, B_rot, C_rot)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Angle Sum Σ", f"{sum_orig:.1f}°", "Always 180°")
    m2.metric("Side Length ||B - A||", f"{euclidean_distance(A, B):.4f}", f"Rotated: {euclidean_distance(A_rot, B_rot):.4f}")
    m3.metric("Side Length ||C - B||", f"{euclidean_distance(B, C):.4f}", f"Rotated: {euclidean_distance(B_rot, C_rot):.4f}")
    m4.metric("Orthogonality RᵀR", "TRUE", f"Dev: {max_diff:.1e}")

    st.success(r"✅ **Linear Algebra Rule**: Orthogonal matrix $R^T R = I_2$ guarantees length and angle preservation ($\|Rv\| = \|v\|$).")


# ==============================================================================
# TAB 2: ELLIPTIC GEOMETRY (SPHERICAL MODEL)
# ==============================================================================
with tab_sph:
    st.header(r"2. Elliptic Geometry ($\mathbb{RP}^2$) — Spherical Model ($S^2, p^T p = 1$)")
    st.markdown(r"Demonstrates spherical/elliptic geometry ($p^T p = 1$) where great circles are geodesics and triangle angle sums exceed 180°.")

    col_ctrl_sph, col_viz_sph = st.columns([1, 2])

    with col_ctrl_sph:
        st.subheader("Vertex Positions (Lat / Lon)")
        lat_A = st.slider("A Latitude (°):", -80.0, 80.0, 45.0)
        lon_A = st.slider("A Longitude (°):", -180.0, 180.0, 0.0)
        lat_B = st.slider("B Latitude (°):", -80.0, 80.0, 0.0)
        lon_B = st.slider("B Longitude (°):", -180.0, 180.0, 60.0)
        lat_C = st.slider("C Latitude (°):", -80.0, 80.0, 60.0)
        lon_C = st.slider("C Longitude (°):", -180.0, 180.0, 30.0)

        A_sph = latlon_to_cartesian(lat_A, lon_A)
        B_sph = latlon_to_cartesian(lat_B, lon_B)
        C_sph = latlon_to_cartesian(lat_C, lon_C)

    with col_viz_sph:
        fig_sph = create_spherical_plotly_fig(A_sph, B_sph, C_sph, title="Spherical Model for Elliptic Geometry (S² Surface)")
        st.plotly_chart(fig_sph, width="stretch")

    st.markdown("---")
    st.subheader("Triangle Angles, Spherical Excess & Distance Measures")

    ang_A_s, ang_B_s, ang_C_s, sum_sph, excess_sph = spherical_triangle_angles(A_sph, B_sph, C_sph)
    d_sph_AB = spherical_distance(A_sph, B_sph)
    d_ell_AB = elliptic_distance(A_sph, B_sph)

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Angle A", f"{ang_A_s:.1f}°")
    s2.metric("Angle B", f"{ang_B_s:.1f}°")
    s3.metric("Angle C", f"{ang_C_s:.1f}°")
    s4.metric("Angle Sum Σ", f"{sum_sph:.1f}°", f"Excess E = +{excess_sph:.1f}°")

    st.info(f"💡 **Non-Euclidean Property**: Triangle Angle Sum = **{sum_sph:.1f}° > 180°**. Spherical Excess $E = {excess_sph:.1f}°$.")

    st.markdown("### Distance Formula Comparison")
    st.write(rf"- **Spherical Distance** $d_{{S^2}}(A,B) = \arccos(A^T B) = {d_sph_AB:.4f}\text{{ rad}} \equiv {np.degrees(d_sph_AB):.1f}^\circ$")
    st.write(rf"- **Elliptic Distance** $d_{{elliptic}}([A],[B]) = \arccos(|A^T B|) = {d_ell_AB:.4f}\text{{ rad}} \equiv {np.degrees(d_ell_AB):.1f}^\circ$")
    st.caption(r"📌 **Conceptual Model**: Spherical geometry on unit sphere $S^2$ is used as the computational engine. Real Projective Plane Elliptic Geometry $\mathbb{RP}^2$ identifies antipodal points $p \sim -p$, yielding distance $d([p],[q]) = \arccos(|p^T q|)$.")


# ==============================================================================
# TAB 3: HYPERBOLIC GEOMETRY
# ==============================================================================
with tab_hyp:
    st.header(r"3. Hyperbolic Geometry ($\mathbb{H}^2$) — Negative Curvature ($K = -1$)")
    st.markdown(r"Demonstrates hyperbolic geometry using the **Poincaré Disk** for visualization and **Minkowski Hyperboloid** ($p^T H p = -1, z > 0$) for linear algebra.")

    col_ctrl_hyp, col_viz_hyp = st.columns([1, 2])

    with col_ctrl_hyp:
        st.subheader("Poincaré Disk Vertices (u, v)")
        u_A = st.slider("A u-coord:", -0.8, 0.8, -0.4, step=0.05)
        v_A = st.slider("A v-coord:", -0.8, 0.8, 0.3, step=0.05)
        u_B = st.slider("B u-coord:", -0.8, 0.8, 0.5, step=0.05)
        v_B = st.slider("B v-coord:", -0.8, 0.8, -0.2, step=0.05)
        u_C = st.slider("C u-coord:", -0.8, 0.8, 0.0, step=0.05)
        v_C = st.slider("C v-coord:", -0.8, 0.8, -0.6, step=0.05)

        A_hyp = hyperboloid_point_from_disk(u_A, v_A)
        B_hyp = hyperboloid_point_from_disk(u_B, v_B)
        C_hyp = hyperboloid_point_from_disk(u_C, v_C)

        st.markdown(r"### Hyperboloid Linear Algebra ($H = \text{diag}(1,1,-1)$)")
        st.code(f"A^T H A = {minkowski_product(A_hyp, A_hyp):.4f}\nB^T H B = {minkowski_product(B_hyp, B_hyp):.4f}\nC^T H C = {minkowski_product(C_hyp, C_hyp):.4f}", language="text")

    with col_viz_hyp:
        fig_hyp = create_hyperbolic_plotly_fig(A_hyp, B_hyp, C_hyp, title="Hyperbolic Poincaré Disk (Curved Geodesics)")
        st.plotly_chart(fig_hyp, width="stretch")

    st.markdown("---")
    st.subheader("Hyperbolic Triangle Angles & Defect")

    ang_A_h, ang_B_h, ang_C_h, sum_hyp, defect_hyp = hyperbolic_triangle_angles(A_hyp, B_hyp, C_hyp)

    h1, h2, h3, h4 = st.columns(4)
    h1.metric("Angle A", f"{ang_A_h:.1f}°")
    h2.metric("Angle B", f"{ang_B_h:.1f}°")
    h3.metric("Angle C", f"{ang_C_h:.1f}°")
    h4.metric("Angle Sum Σ", f"{sum_hyp:.1f}°", f"Defect D = -{defect_hyp:.1f}°")

    st.warning(f"⚠️ **Non-Euclidean Property**: Triangle Angle Sum = **{sum_hyp:.1f}° < 180°**. Angular Defect $D = {defect_hyp:.1f}°$.")


# ==============================================================================
# TAB 4: COMPARE ALL GEOMETRIES
# ==============================================================================
with tab_cmp:
    st.header("4. Unified Curvature & Metric Comparison")
    st.markdown("Side-by-side visual comparison demonstrating how spatial curvature shifts the triangle angle sum and metric forms.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader(r"Euclidean ($\mathbb{E}^2$)")
        fig_e_c = create_euclidean_plotly_fig(A, B, C, title="Euclidean Plane")
        st.plotly_chart(fig_e_c, width="stretch")
        st.metric("Euclidean Angle Sum", f"{sum_orig:.1f}°", "Zero Curvature (K = 0)")

    with c2:
        st.subheader(r"Elliptic / Spherical ($\mathbb{RP}^2 / \mathbb{S}^2$)")
        fig_s_c = create_spherical_plotly_fig(A_sph, B_sph, C_sph, title="Spherical Model Surface")
        st.plotly_chart(fig_s_c, width="stretch")
        st.metric("Spherical Angle Sum", f"{sum_sph:.1f}°", f"Positive Curvature (+{excess_sph:.1f}°)")

    with c3:
        st.subheader(r"Hyperbolic ($\mathbb{H}^2$)")
        fig_h_c = create_hyperbolic_plotly_fig(A_hyp, B_hyp, C_hyp, title="Poincaré Disk")
        st.plotly_chart(fig_h_c, width="stretch")
        st.metric("Hyperbolic Angle Sum", f"{sum_hyp:.1f}°", f"Negative Curvature (-{defect_hyp:.1f}°)")

    st.markdown("---")
    st.subheader("Comprehensive Mathematical Comparison Table")

    cmp_df = pd.DataFrame({
        "Geometric Space": ["Euclidean (E²)", "Elliptic / Spherical (RP² / S²)", "Hyperbolic (H²)"],
        "Gaussian Curvature K": ["0", "+1", "-1"],
        "Triangle Angle Sum": [f"{sum_orig:.1f}° (= 180°)", f"{sum_sph:.1f}° (> 180°)", f"{sum_hyp:.1f}° (< 180°)"],
        "Geodesic Type": ["Straight Line", "Great Circle Arc", "Orthogonal Disk Arc"],
        "Metric Tensor M": ["Identity I₂", "Identity I₃ (on S²)", "Minkowski H = diag(1,1,-1)"],
        "Spatial Constraint": ["Unconstrained R²", "pᵀ p = 1 (p ~ -p)", "pᵀ H p = -1 (z > 0)"],
        "Preservation Matrix": ["Rᵀ R = I₂", "Rᵀ R = I₃", "Bᵀ H B = H"]
    })

    st.dataframe(cmp_df, use_container_width=True)
