from typing import (
    NamedTuple,
    Optional,
)


class Enrollment(NamedTuple):
    email: str
    enrolled: bool


class EnrollmentMetadataToUpdate(NamedTuple):
    enrolled: Optional[bool] = None
