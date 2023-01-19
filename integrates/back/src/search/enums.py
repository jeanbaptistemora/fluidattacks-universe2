from enum import (
    Enum,
)


class Sort(str, Enum):
    ASCENDING: str = "asc"
    DESCENDING: str = "desc"
