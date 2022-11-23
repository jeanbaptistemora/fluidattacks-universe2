from enum import (
    Enum,
)


class PolicyStateStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    APPROVED: str = "APPROVED"
    INACTIVE: str = "INACTIVE"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"
