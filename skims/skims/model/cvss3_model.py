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


class Exploitability(Enum):
    unproven: float = 0.91
    poc: float = 0.94
    functional: float = 0.97
    high: float = 1.0


class IntegrityImpact(Enum):
    none: float = 0.00
    low: float = 0.22
    high: float = 0.56


class PrivilegesRequired(Enum):
    none: float = 0.27
    low: float = 0.62
    high: float = 0.85


class RemediationLevel(Enum):
    official_fix: float = 0.95
    temporary_fix: float = 0.96
    workaround: float = 0.97
    unavailable: float = 1.00


class ReportConfidence(Enum):
    unknown: float = 0.92
    reasonable: float = 0.96
    confirmed: float = 1.00


class SeverityScope(Enum):
    unchanged: float = 0.0
    changed: float = 1.0


class UserInteraction(Enum):
    required: float = 0.62
    none: float = 0.85
