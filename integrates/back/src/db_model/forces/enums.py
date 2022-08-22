from enum import (
    Enum,
)


class VulnerabilityExploitState(str, Enum):
    ACCEPTED: str = "ACCEPTED"
    CLOSED: str = "CLOSED"
    OPEN: str = "OPEN"
    UNKNOWN: str = "UNKNOWN"
