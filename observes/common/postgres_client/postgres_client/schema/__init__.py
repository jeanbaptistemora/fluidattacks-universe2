# Standard libraries
from typing import (
    Callable,
    Iterable,
    NamedTuple,
)
# Third party libraries
# Local libraries


class Schema(NamedTuple):
    name: str
    get_tables: Callable[[], Iterable[str]]
