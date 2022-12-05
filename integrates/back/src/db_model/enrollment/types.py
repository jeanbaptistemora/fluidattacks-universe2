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


class Enrollment(NamedTuple):
    email: str
    enrolled: bool
    trial: Trial


class EnrollmentMetadataToUpdate(NamedTuple):
    enrolled: Optional[bool] = None
    trial: Optional[Trial] = None
