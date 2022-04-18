from returns.io import (
    IO,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from typing import (
    Any,
    FrozenSet,
)


def select_fields(selection: Any, props: FrozenSet[str]) -> IO[None]:
    for attr in props:
        getattr(selection, attr)()
    return IO(None)


def select_page_fields(page_selection: Any) -> IO[None]:
    props = frozenset(DataPage.__annotations__) - frozenset(["items"])
    return select_fields(page_selection, props)
