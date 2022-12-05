from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
    Optional,
)


class Trial(NamedTuple):
    completed: bool
    extension_date: Optional[datetime]
    extension_days: int
    start_date: Optional[datetime]


class Company(NamedTuple):
    domain: str
    trial: Trial
