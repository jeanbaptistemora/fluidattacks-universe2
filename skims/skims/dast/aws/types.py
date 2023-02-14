from typing import (
    Any,
    NamedTuple,
)


class Location(NamedTuple):
    arn: str
    access_patterns: tuple[str, ...]
    description: str
    values: tuple[Any, ...]
