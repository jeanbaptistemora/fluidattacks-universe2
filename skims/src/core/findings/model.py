# Standard library
from typing import (
    NamedTuple,
    Tuple,
)


class Finding(NamedTuple):
    asserts_exploit: str
    rules: Tuple[str, ...]
    title: str
