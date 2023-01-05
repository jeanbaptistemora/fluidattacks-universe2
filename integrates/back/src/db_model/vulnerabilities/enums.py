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


class VulnerabilityStateReason(str, Enum):
    CONSISTENCY: str = "CONSISTENCY"
    DUPLICATED: str = "DUPLICATED"
    EVIDENCE: str = "EVIDENCE"
    EXCLUSION: str = "EXCLUSION"
    FALSE_POSITIVE: str = "FALSE_POSITIVE"
    NAMING: str = "NAMING"
    NO_JUSTIFICATION: str = "NO_JUSTIFICATION"
    NOT_REQUIRED: str = "NOT_REQUIRED"
    OMISSION: str = "OMISSION"
    OTHER: str = "OTHER"
    REPORTING_ERROR: str = "REPORTING_ERROR"
    SCORING: str = "SCORING"
    WRITING: str = "WRITING"


class VulnerabilityStateStatus(str, Enum):
    SAFE: str = "SAFE"
    DELETED: str = "DELETED"
    MASKED: str = "MASKED"
    VULNERABLE: str = "VULNERABLE"
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
