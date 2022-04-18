from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenList,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class DataPage(SupportsKind1["DataPage[_T]", _T]):
    page: int
    pages: int
    count: int
    items: FrozenList[_T]
