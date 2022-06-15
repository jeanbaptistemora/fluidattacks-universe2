from enum import (
    Enum,
)


class EventAccessibility(str, Enum):
    ENVIRONMENT: str = "ENVIRONMENT"
    REPOSITORY: str = "REPOSITORY"
    VPN_CONNECTION: str = "VPN_CONNECTION"


class EventActionsAfterBlocking(str, Enum):
    EXECUTE_OTHER_GROUP_OTHER_CLIENT: str = "EXECUTE_OTHER_GROUP_OTHER_CLIENT"
    EXECUTE_OTHER_GROUP_SAME_CLIENT: str = "EXECUTE_OTHER_GROUP_SAME_CLIENT"
    NONE: str = "NONE"
    OTHER: str = "OTHER"
    TRAINING: str = "TRAINING"


class EventActionsBeforeBlocking(str, Enum):
    DOCUMENT_GROUP: str = "DOCUMENT_GROUP"
    NONE: str = "NONE"
    OTHER: str = "OTHER"
    TEST_OTHER_PART_TOE: str = "TEST_OTHER_PART_TOE"


class EventAffectedComponents(str, Enum):
    CLIENT_STATION: str = "CLIENT_STATION"
    COMPILE_ERROR: str = "COMPILE_ERROR"
    DOCUMENTATION: str = "DOCUMENTATION"
    FLUID_STATION: str = "FLUID_STATION"
    INTERNET_CONNECTION: str = "INTERNET_CONNECTION"
    LOCAL_CONNECTION: str = "LOCAL_CONNECTION"
    OTHER: str = "OTHER"
    SOURCE_CODE: str = "SOURCE_CODE"
    TEST_DATA: str = "TEST_DATA"
    TOE_ALTERATION: str = "TOE_ALTERATION"
    TOE_CREDENTIALS: str = "TOE_CREDENTIALS"
    TOE_EXCLUSSION: str = "TOE_EXCLUSSION"
    TOE_LOCATION: str = "TOE_LOCATION"
    TOE_PRIVILEGES: str = "TOE_PRIVILEGES"
    TOE_UNACCESSIBLE: str = "TOE_UNACCESSIBLE"
    TOE_UNAVAILABLE: str = "TOE_UNAVAILABLE"
    TOE_UNSTABLE: str = "TOE_UNSTABLE"
    VPN_CONNECTION: str = "VPN_CONNECTION"


class EventEvidenceType(str, Enum):
    FILE: str = "FILE"
    IMAGE: str = "IMAGE"


class EventStateStatus(str, Enum):
    CLOSED: str = "CLOSED"
    CREATED: str = "CREATED"
    OPEN: str = "OPEN"
    SOLVED: str = "SOLVED"


class EventType(str, Enum):
    AUTHORIZATION_SPECIAL_ATTACK: str = "AUTHORIZATION_SPECIAL_ATTACK"
    DATA_UPDATE_REQUIRED: str = "DATA_UPDATE_REQUIRED"
    INCORRECT_MISSING_SUPPLIES: str = "INCORRECT_MISSING_SUPPLIES"
    OTHER: str = "OTHER"
    TOE_DIFFERS_APPROVED: str = "TOE_DIFFERS_APPROVED"
