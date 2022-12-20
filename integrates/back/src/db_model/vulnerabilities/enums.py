from enum import (
    Enum,
)


class VulnerabilityToolImpact(str, Enum):
    DIRECT: str = "DIRECT"
    INDIRECT: str = "INDIRECT"


class VulnerabilityType(str, Enum):
    INPUTS: str = "INPUTS"
    LINES: str = "LINES"
    PORTS: str = "PORTS"


class VulnerabilityStateStatus(str, Enum):
    CLOSED: str = "CLOSED"
    CREATED: str = "CREATED"
    DELETED: str = "DELETED"
    MASKED: str = "MASKED"
    OPEN: str = "OPEN"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class VulnerabilityTreatmentStatus(str, Enum):
    ACCEPTED: str = "ACCEPTED"
    ACCEPTED_UNDEFINED: str = "ACCEPTED_UNDEFINED"
    IN_PROGRESS: str = "IN_PROGRESS"
    NEW: str = "NEW"


class VulnerabilityAcceptanceStatus(str, Enum):
    APPROVED: str = "APPROVED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class VulnerabilityVerificationStatus(str, Enum):
    MASKED: str = "MASKED"
    REQUESTED: str = "REQUESTED"
    ON_HOLD: str = "ON_HOLD"
    VERIFIED: str = "VERIFIED"


class VulnerabilityZeroRiskStatus(str, Enum):
    CONFIRMED: str = "CONFIRMED"
    REJECTED: str = "REJECTED"
    REQUESTED: str = "REQUESTED"
