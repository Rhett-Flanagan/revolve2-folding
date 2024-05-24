from dataclasses import dataclass

from .._aabb import AABB
from ._geometry import Geometry


@dataclass(kw_only=True)
class GeometryTriangle(Geometry):
    """Box geometry."""

    aabb: AABB
    """AABB describing the box's shape."""
