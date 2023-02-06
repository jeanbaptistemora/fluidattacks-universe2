from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
    Optional,
)


class Trial(NamedTuple):
    email: str
    completed: bool
    extension_date: Optional[datetime]
    extension_days: int
    start_date: Optional[datetime]


class TrialMetadataToUpdate(NamedTuple):
    completed: Optional[bool] = None
