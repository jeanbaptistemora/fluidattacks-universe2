# Standard library
from enum import (
    Enum,
)


class AttackComplexity(Enum):
    low: float = 0.44
    high: float = 0.77


class AttackVector(Enum):
    physical: float = 0.20
    local: float = 0.55
    adjacent: float = 0.62
    network: float = 0.85


class AvailabilityImpact(Enum):
    none: float = 0.00
    low: float = 0.22
    high: float = 0.56


class ConfidentialityImpact(Enum):
    none: float = 0.00
    low: float = 0.22
    high: float = 0.56


class IntegrityImpact(Enum):
    none: float = 0.00
    low: float = 0.22
    high: float = 0.56
