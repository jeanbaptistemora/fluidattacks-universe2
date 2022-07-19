from enum import (
    Enum,
)


class InvitiationState(str, Enum):
    PENDING: str = "PENDING"
    UNREGISTERED: str = "UNREGISTERED"
    REGISTERED: str = "REGISTERED"
