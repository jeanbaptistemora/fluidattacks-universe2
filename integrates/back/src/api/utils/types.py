from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class ApiDeprecation(NamedTuple):
    parent: str
    field: str
    reason: str
    due_date: datetime
    type: str
