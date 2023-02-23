from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class Trial(NamedTuple):
    email: str
    completed: bool
    extension_date: datetime | None
    extension_days: int
    start_date: datetime | None


class TrialMetadataToUpdate(NamedTuple):
    completed: bool | None = None
