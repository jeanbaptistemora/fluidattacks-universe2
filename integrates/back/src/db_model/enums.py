from enum import (
    Enum,
)


class Source(str, Enum):
    ASM: str = "ASM"
    ESCAPE: str = "ESCAPE"
    MACHINE: str = "MACHINE"


class StateRemovalJustification(str, Enum):
    DUPLICATED: str = "DUPLICATED"
    EXCLUSION: str = "EXCLUSION"
    FALSE_POSITIVE: str = "FALSE_POSITIVE"
    NO_JUSTIFICATION: str = "NO_JUSTIFICATION"
    NOT_REQUIRED: str = "NOT_REQUIRED"
    REPORTING_ERROR: str = "REPORTING_ERROR"


class CredentialType(str, Enum):
    SSH: str = "SSH"


class GitCloningStatus(str, Enum):
    CLONING: str = "CLONING"
    FAILED: str = "FAILED"
    OK: str = "OK"
    UNKNOWN: str = "UNKNOWN"


class Notification(str, Enum):
    NEW_DRAFT: str = "NEW_DRAFT"
    UPDATED_TREATMENT: str = "UPDATED_TREATMENT"
    VULNERABILITY_ASSIGNED: str = "VULNERABILITY_ASSIGNED"
