# pylint: skip-file

from dataclasses import (
    dataclass,
)
from multiprocessing.pool import (
    Pool,
)
from purity.v1 import (
    Flattener,
    Patch,
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
_thread_pool = Pool()


@dataclass(frozen=True)
class _ParallelGetter(
    SupportsKind2[
        "_ParallelGetter[_PageTVar, _DataTVar]",
        _PageTVar,
        _DataTVar,
    ],
):
    _getter: Patch[Callable[[_PageTVar], IO[Maybe[_DataTVar]]]]


@dataclass(frozen=True)
class ParallelGetter(
    _ParallelGetter[_PageTVar, _DataTVar],
):
    def __init__(
        self, getter: Callable[[_PageTVar], IO[Maybe[_DataTVar]]]
    ) -> None:
        super().__init__(Patch(getter))

    def getter(self, page: _PageTVar) -> IO[Maybe[_DataTVar]]:
        return self._getter.unwrap(page)

    def get_pages(
        self,
        pages: List[_PageTVar],
    ) -> IO[List[Maybe[_DataTVar]]]:
        return Flattener.list_io(_thread_pool.map(self.getter, pages))
