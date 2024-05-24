import math
from enum import Enum


class EquilateralAngles(Enum):
    """Standard angles at which  modular robot modules can be attached."""

    DEG_0 = 0
    DEG_60 = math.pi / 3.0
    DEG_90 = math.pi / 2.0
    DEG_120 = math.pi / 3.0 * 2
    DEG_180 = math.pi
    DEG_240 = math.pi / 3.0 * 4
    DEG_270 = math.pi / 2.0 * 3
    DEG_300 = math.pi / 3.0 * 5
    RAD_0 = 0
    RAD_HALFPI = math.pi / 2.0
    RAD_PI = math.pi
    RAD_ONEANDAHALFPI = math.pi / 2.0 * 3
