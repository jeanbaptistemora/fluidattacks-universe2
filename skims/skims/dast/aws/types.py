from typing import (
    Any,
    NamedTuple,
)


class Location(NamedTuple):
    arn: str
    access_pattern: str
    description: str
    value: Any
