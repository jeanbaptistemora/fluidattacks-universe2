from datetime import (
    date,
)
from typing import (
    NamedTuple,
)


class ApiDeprecation(NamedTuple):
    parent: str
    field: str
    reason: str
    due_date: date
    type: str
