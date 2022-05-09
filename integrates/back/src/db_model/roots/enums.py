from enum import (
    Enum,
)


class RootStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    INACTIVE: str = "INACTIVE"


class RootType(str, Enum):
    GIT: str = "Git"
    IP: str = "IP"
    URL: str = "URL"
