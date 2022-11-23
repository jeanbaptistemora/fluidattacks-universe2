from enum import (
    Enum,
)


class OrganizationInvitiationState(str, Enum):
    PENDING: str = "PENDING"
    UNREGISTERED: str = "UNREGISTERED"
    REGISTERED: str = "REGISTERED"
