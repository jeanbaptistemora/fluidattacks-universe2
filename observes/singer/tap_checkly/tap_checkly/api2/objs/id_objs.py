from dataclasses import (
    dataclass,
)
from returns.primitives.hkt import (
    SupportsKind2,
)
from typing import (
    TypeVar,
)

_ID = TypeVar("_ID")
_T = TypeVar("_T")


@dataclass(frozen=True)
class CheckId:
    id_str: str


@dataclass(frozen=True)
class IndexedObj(SupportsKind2["IndexedObj[_ID, _T]", _ID, _T]):
    id_obj: _ID
    obj: _T
