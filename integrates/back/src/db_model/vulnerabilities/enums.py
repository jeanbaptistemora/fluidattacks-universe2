from enum import (
    Enum,
)


class VulnerabilityType(Enum):
    INPUTS: str = "INPUTS"
    LINES: str = "LINES"
    PORTS: str = "PORTS"


class VulnerabilityStateStatus(Enum):
    CLOSED: str = "CLOSED"
    DELETED: str = "DELETED"
    OPEN: str = "OPEN"


class VulnerabilityTreatmentStatus(Enum):
    ACCEPTED: str = "ACCEPTED"
    ACCEPTED_UNDEFINED: str = "ACCEPTED_UNDEFINED"
    IN_PROGRESS: str = "IN_PROGRESS"


class VulnerabilityAcceptanceStatus(Enum):
    APPROVED: str = "APPROVED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class VulnerabilityVerificationStatus(Enum):
    MASKED: str = "MASKED"
    REQUESTED: str = "REQUESTED"
    VERIFIED: str = "VERIFIED"


class VulnerabilityZeroRiskStatus(Enum):
    CONFIRMED: str = "CONFIRMED"
    REJECTED: str = "REJECTED"
    REQUESTED: str = "REQUESTED"
