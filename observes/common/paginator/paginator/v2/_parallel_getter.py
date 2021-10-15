# pylint: skip-file

from dataclasses import (
    dataclass,
)
from pathos.threading import (
    ThreadPool,
)
from purity.v1 import (
    Flattener,
    FrozenList,
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
    TypeVar,
)

_PageTVar = TypeVar("_PageTVar")
_DataTVar = TypeVar("_DataTVar")
_thread_pool = ThreadPool()
# using pathos solves some issues of using multiprocessing:
# - pool scope: pool obj had to be created on specific scope
# - serialization: some pickle errors raise when mapping


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
        pages: FrozenList[_PageTVar],
    ) -> IO[FrozenList[Maybe[_DataTVar]]]:
        return Flattener.list_io(tuple(_thread_pool.map(self.getter, pages)))
