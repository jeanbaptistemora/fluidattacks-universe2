from typing import (
    Any,
    NamedTuple,
    Tuple,
)


class Location(NamedTuple):
    arn: str
    access_patterns: Tuple[str, ...]
    description: str
    values: Tuple[Any, ...]
