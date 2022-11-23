from typing import (
    NamedTuple,
)


class Trial(NamedTuple):
    completed: bool
    extension_date: str
    extension_days: int
    start_date: str


class Company(NamedTuple):
    domain: str
    trial: Trial
