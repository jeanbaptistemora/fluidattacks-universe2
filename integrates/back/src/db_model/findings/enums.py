from enum import (
    Enum,
)


class DraftRejectionReason(Enum):
    CONSISTENCY: str = "CONSISTENCY"
    EVIDENCE: str = "EVIDENCE"
    NAMING: str = "NAMING"
    OMISSION: str = "OMISSION"
    OTHER: str = "OTHER"
    SCORING: str = "SCORING"
    WRITING: str = "WRITING"


class FindingCvssVersion(Enum):
    V31: str = "3.1"
    V20: str = "2.0"


class FindingEvidenceName(Enum):
    # pylint: disable=invalid-name
    animation: str = "animation"
    evidence1: str = "evidence1"
    evidence2: str = "evidence2"
    evidence3: str = "evidence3"
    evidence4: str = "evidence4"
    evidence5: str = "evidence5"
    exploitation: str = "exploitation"
    records: str = "records"


class FindingSorts(Enum):
    NO: str = "NO"
    YES: str = "YES"


class FindingStateStatus(Enum):
    APPROVED: str = "APPROVED"
    CREATED: str = "CREATED"
    DELETED: str = "DELETED"
    MASKED: str = "MASKED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class FindingStatus(Enum):
    CLOSED: str = "CLOSED"
    OPEN: str = "OPEN"


class FindingVerificationStatus(Enum):
    MASKED: str = "MASKED"
    REQUESTED: str = "REQUESTED"
    ON_HOLD: str = "ON_HOLD"
    VERIFIED: str = "VERIFIED"
