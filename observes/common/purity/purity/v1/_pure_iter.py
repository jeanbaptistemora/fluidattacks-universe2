from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from purity.v1._patch import (
    Patch,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from typing import (
    Callable,
    Iterator,
    TypeVar,
)

_DataTVar = TypeVar("_DataTVar")
_ReturnTVar = TypeVar("_ReturnTVar")


@dataclass(frozen=True)
class PureIter(
    SupportsKind1["PureIter", _DataTVar],
):
    _iter_obj: Patch[Callable[[], Iterator[_DataTVar]]]

    def __init__(self, iter_obj: Callable[[], Iterator[_DataTVar]]) -> None:
        object.__setattr__(self, "_iter_obj", Patch(iter_obj))

    @property
    def iter_obj(self) -> Iterator[_DataTVar]:
        return self._iter_obj.unwrap()

    def map(
        self, function: Callable[[_DataTVar], _ReturnTVar]
    ) -> PureIter[_ReturnTVar]:
        return PureIter(lambda: map(function, self.iter_obj))
