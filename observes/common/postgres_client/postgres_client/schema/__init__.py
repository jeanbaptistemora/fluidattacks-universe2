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
    delete_on_db: Callable[[], None]
    exist_on_db: Callable[[], bool]
    get_tables: Callable[[], Iterable[str]]
