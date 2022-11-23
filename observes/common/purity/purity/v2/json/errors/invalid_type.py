from typing import (
    Any,
)


class _InvalidType(Exception):
    pass


class InvalidType(_InvalidType):
    def __init__(self, obj: _InvalidType) -> None:
        super().__init__(obj)


def new(caller: str, expected: str, item: Any) -> InvalidType:
    draft = _InvalidType(
        f"{caller} expected `{expected}` not `{str(type(item))}`"
    )
    return InvalidType(draft)
