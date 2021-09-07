from enum import (
    Enum,
)


class FindingCvssVersion(Enum):
    V31: str = "3.1"
    V20: str = "2.0"


class FindingSorts(Enum):
    NO: str = "NO"
    YES: str = "YES"


class FindingStateJustification(Enum):
    DUPLICATED: str = "DUPLICATED"
    FALSE_POSITIVE: str = "FALSE_POSITIVE"
    NOT_REQUIRED: str = "NOT_REQUIRED"
    NO_JUSTIFICATION: str = "NO_JUSTIFICATION"


class FindingStateStatus(Enum):
    APPROVED: str = "APPROVED"
    CREATED: str = "CREATED"
    DELETED: str = "DELETED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class FindingStatus(Enum):
    CLOSED: str = "CLOSED"
    OPEN: str = "OPEN"


class FindingVerificationStatus(Enum):
    MASKED: str = "MASKED"
    REQUESTED: str = "REQUESTED"
    VERIFIED: str = "VERIFIED"
