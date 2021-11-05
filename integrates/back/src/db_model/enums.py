from enum import (
    Enum,
)


class Source(Enum):
    ASM: str = "ASM"
    ESCAPE: str = "ESCAPE"
    MACHINE: str = "MACHINE"


class StateRemovalJustification(Enum):
    DUPLICATED: str = "DUPLICATED"
    EXCLUSION: str = "EXCLUSION"
    FALSE_POSITIVE: str = "FALSE_POSITIVE"
    NO_JUSTIFICATION: str = "NO_JUSTIFICATION"
    NOT_REQUIRED: str = "NOT_REQUIRED"
    REPORTING_ERROR: str = "REPORTING_ERROR"
