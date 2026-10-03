"""Tests for cross-geometry comparison (analysis/comparison.py).

Key property to assert once implemented:
  - Euclidean angle sum == PI, Spherical > PI, Hyperbolic < PI
  - All three return a result for the same input points
"""

import pytest


class TestGeometryComparison:
    def test_returns_all_three_results(self):
        pytest.skip("not yet implemented")

    def test_angle_sum_ordering(self):
        """hyperbolic < pi < euclidean == pi < spherical"""
        pytest.skip("not yet implemented")
