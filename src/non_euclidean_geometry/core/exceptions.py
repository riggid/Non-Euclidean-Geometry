"""Project-specific exceptions."""


class InvalidPointError(Exception):
    """Raised when a point is invalid for the given geometry.

    For example: a point outside the Poincaré disk in hyperbolic geometry.
    """


class DegenerateTriangleError(Exception):
    """Raised when three points don't form a valid triangle.

    For example: collinear points, or two identical points.
    """


class OutOfBoundsError(Exception):
    """Raised when a point lies outside the valid domain of a geometry."""
