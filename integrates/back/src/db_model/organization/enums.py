from enum import (
    Enum,
)


class OrganizationStateStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    DELETED: str = "DELETED"
