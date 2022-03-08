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
    ACCESS_GRANTED: str = "ACCESS_GRANTED"
    CHARTS_REPORT: str = "CHARTS_REPORT"
    DAILY_DIGEST: str = "DAILY_DIGEST"
    FILE_UPLOADED: str = "FILE_UPLOADED"
    GROUP_REPORT: str = "GROUP_REPORT"
    NEW_COMMENT: str = "NEW_COMMENT"
    NEW_DRAFT: str = "NEW_DRAFT"
    REMEDIATE_FINDING: str = "REMEDIATE_FINDING"
    ROOT_MOVED: str = "ROOT_MOVED"
    UPDATED_TREATMENT: str = "UPDATED_TREATMENT"
    VULNERABILITY_ASSIGNED: str = "VULNERABILITY_ASSIGNED"
