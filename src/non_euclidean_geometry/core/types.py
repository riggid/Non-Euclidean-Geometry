"""Core data types shared across all geometry modules."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TriangleResult:
    """Measurements for a triangle in a particular geometry.

    Side and angle mappings use the labels ``AB``, ``BC``, and ``CA`` and
    ``A``, ``B``, and ``C`` respectively. Angles and their sum are in radians.
    """

    side_lengths: dict[str, float]
    angles: dict[str, float]
    angle_sum: float
    curvature: float
