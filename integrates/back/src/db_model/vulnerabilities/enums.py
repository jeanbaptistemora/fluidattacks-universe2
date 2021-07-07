from enum import (
    Enum,
)


class VulnerabilityType(Enum):
    INPUTS: str = "INPUTS"
    LINES: str = "LINES"
    PORTS: str = "PORTS"


class VulnerabilityDeletionJustification(Enum):
    DUPLICATED: str = "DUPLICATED"
    FALSE_POSITIVE: str = "FALSE_POSITIVE"
    REPORTING_ERROR: str = "REPORTING_ERROR"
    NO_JUSTIFICATION: str = "NO_JUSTIFICATION"


class VulnerabilityApprovalStatus(Enum):
    APPROVED: str = "APPROVED"
    PENDING: str = "PENDING"


class VulnerabilityStateStatus(Enum):
    CLOSED: str = "CLOSED"
    DELETED: str = "DELETED"
    OPEN: str = "OPEN"


class VulnerabilityTreatmentStatus(Enum):
    ACCEPTED: str = "ACCEPTED"
    ACCEPTED_UNDEFINED: str = "ACCEPTED_UNDEFINED"
    IN_PROGRESS: str = "IN_PROGRESS"
    NEW: str = "NEW"


class VulnerabilityAcceptanceStatus(Enum):
    APPROVED: str = "APPROVED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class VulnerabilityVerificationStatus(Enum):
    REQUESTED: str = "REQUESTED"
    VERIFIED: str = "VERIFIED"


class VulnerabilityZeroRiskStatus(Enum):
    CONFIRMED: str = "CONFIRMED"
    REJECTED: str = "REJECTED"
    REQUESTED: str = "REQUESTED"
