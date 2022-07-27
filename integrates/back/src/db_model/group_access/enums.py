from enum import (
    Enum,
)


class GroupInvitiationState(str, Enum):
    PENDING: str = "PENDING"
    UNREGISTERED: str = "UNREGISTERED"
    REGISTERED: str = "REGISTERED"
