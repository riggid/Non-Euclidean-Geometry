"""Mathematical and application-wide constants."""

import numpy as np

EPSILON: float = 1e-10
PI: float = np.pi

# Spherical geometry
DEFAULT_SPHERE_RADIUS: float = 1.0

# Hyperbolic geometry (Poincaré disk)
POINCARE_DISK_RADIUS: float = 1.0

# Number of sample points along a geodesic curve
DEFAULT_GEODESIC_SAMPLES: int = 100

# Canvas / rendering
CANVAS_SIZE: int = 600
POINT_RADIUS: float = 5.0
