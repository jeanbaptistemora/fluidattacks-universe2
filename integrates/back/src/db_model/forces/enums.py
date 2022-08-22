from enum import (
    Enum,
)


class VulnerabilityExploitState(str, Enum):
    ACCEPTED = "ACCEPTED"
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    UNKNOWN = "UNKNOWN"
