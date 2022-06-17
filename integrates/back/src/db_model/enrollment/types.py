from typing import (
    NamedTuple,
)


class Trial(NamedTuple):
    completed: bool
    extension_date: str
    extension_days: int
    start_date: str


class Enrollment(NamedTuple):
    email: str
    enrolled: bool
    trial: Trial
