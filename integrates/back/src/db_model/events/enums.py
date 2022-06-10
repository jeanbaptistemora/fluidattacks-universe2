from enum import (
    Enum,
)


class EventAccessibility(str, Enum):
    ENVIRONMENT: str = "ENVIRONMENT"
    REPOSITORY: str = "REPOSITORY"


class EventStateStatus(str, Enum):
    APPROVED: str = "APPROVED"
    CREATED: str = "CREATED"
    DELETED: str = "DELETED"
    MASKED: str = "MASKED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"
    CLOSED: str = "CLOSED"
    OPEN: str = "OPEN"


class EventType(str, Enum):
    AUTHORIZATION_SPECIAL_ATTACK: str = "AUTHORIZATION_SPECIAL_ATTACK"
    DATA_UPDATE_REQUIRED: str = "DATA_UPDATE_REQUIRED"
    INCORRECT_MISSING_SUPPLIES: str = "INCORRECT_MISSING_SUPPLIES"
    OTHER: str = "OTHER"
    TOE_DIFFERS_APPROVED: str = "TOE_DIFFERS_APPROVED"
