# pylint: skip-file

from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from returns.primitives.hkt import (
    SupportsKind2,
)
from typing import (
    Callable,
    List,
    TypeVar,
)

_PageTVar = TypeVar("_PageTVar")
_DataTVar = TypeVar("_DataTVar")
_MetaTVar = TypeVar("_MetaTVar")


@dataclass(frozen=True)
class PageResult(
    SupportsKind2["PageResult[_DataTVar, _MetaTVar]", _DataTVar, _MetaTVar],
):
    data: List[_DataTVar]
    metadata: _MetaTVar


NextPageGetter = Callable[[PageResult[_DataTVar, _MetaTVar]], Maybe[_PageTVar]]
PageGetter = Callable[[_PageTVar], Maybe[PageResult[_DataTVar, _MetaTVar]]]
PageGetterIO = Callable[
    [_PageTVar], IO[Maybe[PageResult[_DataTVar, _MetaTVar]]]
]
