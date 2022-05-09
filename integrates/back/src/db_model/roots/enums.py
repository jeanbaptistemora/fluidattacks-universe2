from enum import (
    Enum,
)


class RootStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    INACTIVE: str = "INACTIVE"
