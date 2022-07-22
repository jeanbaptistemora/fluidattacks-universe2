from typing import (
    NamedTuple,
)


class ApiDeprecation(NamedTuple):
    parent: str
    field: str
    reason: str
    type: str
