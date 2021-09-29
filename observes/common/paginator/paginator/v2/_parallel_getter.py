# pylint: skip-file

from dataclasses import (
    dataclass,
)
from multiprocessing.pool import (
    Pool,
)
from paginator.v2._core import (
    PageGetterIO,
    PageResult,
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
    SupportsKind3,
)
from typing import (
    List,
    TypeVar,
)

_PageTVar = TypeVar("_PageTVar")
_DataTVar = TypeVar("_DataTVar")
_MetaTVar = TypeVar("_MetaTVar")
_thread_pool = Pool()


@dataclass(frozen=True)
class _ParallelGetter(
    SupportsKind3[
        "_ParallelGetter[_PageTVar, _DataTVar, _MetaTVar]",
        _PageTVar,
        _DataTVar,
        _MetaTVar,
    ],
):
    _getter: Patch[PageGetterIO[_PageTVar, _DataTVar, _MetaTVar]]  # type: ignore


@dataclass(frozen=True)
class ParallelGetter(
    _ParallelGetter[_PageTVar, _DataTVar, _MetaTVar],
):
    def __init__(
        self, getter: PageGetterIO[_PageTVar, _DataTVar, _MetaTVar]  # type: ignore
    ) -> None:
        super().__init__(Patch(getter))

    def getter(
        self, page: _PageTVar
    ) -> IO[Maybe[PageResult[_DataTVar, _MetaTVar]]]:
        return self._getter.unwrap(page)

    def get_pages(
        self,
        pages: List[_PageTVar],
    ) -> IO[List[Maybe[PageResult[_DataTVar, _MetaTVar]]]]:
        return Flattener.list_io(_thread_pool.map(self.getter, pages))
