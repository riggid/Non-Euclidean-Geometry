"""
Geometry Linear Algebra Package
Linear Algebraic Transformations in Euclidean and Non-Euclidean Geometries
"""

from .linalg import (
    matrix_vector_mult,
    dot_product,
    vector_norm,
    minkowski_product,
    check_matrix_preservation,
    H_METRIC,
)
from .euclidean import (
    euclidean_rotation_matrix,
    project_vector,
    euclidean_distance,
    euclidean_triangle_angles,
    euclidean_triangle_area,
)
from .spherical import (
    spherical_rotation_matrix_z,
    spherical_rotation_matrix_y,
    latlon_to_cartesian,
    spherical_distance,
    elliptic_distance,
    spherical_great_circle_arc,
    spherical_triangle_angles,
)
from .hyperbolic import (
    lorentz_boost_x,
    hyperboloid_point_from_disk,
    hyperbolic_distance,
    poincare_projection,
    poincare_geodesic_arc,
    hyperbolic_triangle_angles,
)

__all__ = [
    "matrix_vector_mult",
    "dot_product",
    "vector_norm",
    "minkowski_product",
    "check_matrix_preservation",
    "H_METRIC",
    "euclidean_rotation_matrix",
    "project_vector",
    "euclidean_distance",
    "euclidean_triangle_angles",
    "euclidean_triangle_area",
    "spherical_rotation_matrix_z",
    "spherical_rotation_matrix_y",
    "latlon_to_cartesian",
    "spherical_distance",
    "elliptic_distance",
    "spherical_great_circle_arc",
    "spherical_triangle_angles",
    "lorentz_boost_x",
    "hyperboloid_point_from_disk",
    "hyperbolic_distance",
    "poincare_projection",
    "poincare_geodesic_arc",
    "hyperbolic_triangle_angles",
]
