from enum import (
    Enum,
)


class EventStatus(Enum):
    APPROVED: str = "APPROVED"
    CREATED: str = "CREATED"
    DELETED: str = "DELETED"
    MASKED: str = "MASKED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"
    CLOSED: str = "CLOSED"
    OPEN: str = "OPEN"
