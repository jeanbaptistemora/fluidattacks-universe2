from enum import (
    Enum,
)


class Channel(str, Enum):
    CALL = "CALL"
    SMS = "SMS"
