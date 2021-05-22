from enum import Enum


class FindingStateStatus(Enum):
    APPROVED: str = "APPROVED"
    CREATED: str = "CREATED"
    DELETED: str = "DELETED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class FindingSorts(Enum):
    NO: str = "NO"
    YES: str = "YES"


class FindingStatus(Enum):
    CLOSED: str = "CLOSED"
    OPEN: str = "OPEN"


class FindingVerificationStatus(Enum):
    REQUESTED: str = "REQUESTED"
    VERIFIED: str = "VERIFIED"
