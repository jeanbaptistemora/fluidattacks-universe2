from __future__ import (
    annotations,
)

from collections import (
    deque,
)
from dataclasses import (
    dataclass,
)
from purity.v1._frozen import (
    FrozenList,
)
from purity.v1._patch import (
    Patch,
)
from returns.io import (
    IO,
)
from returns.pipeline import (
    pipe,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Callable,
    Iterable,
    Iterator,
    List,
    Optional,
    TypeVar,
)

_D = TypeVar("_D")
_I = TypeVar("_I")
_R = TypeVar("_R")


@dataclass(frozen=True)
class IOiter(
    SupportsKind1["IOiter[_D]", _D],
):
    _io_iter_obj: Patch[Callable[[], IO[Iterator[_D]]]]

    def __init__(self, io_iter_obj: Callable[[], IO[Iterator[_D]]]) -> None:
        object.__setattr__(self, "_io_iter_obj", Patch(io_iter_obj))

    @property
    def io_iter_obj(self) -> IO[Iterator[_D]]:
        return self._io_iter_obj.unwrap()

    def map_each(self, function: Callable[[_D], _R]) -> IOiter[_R]:
        return IOiter(
            lambda: self.io_iter_obj.map(
                lambda iter_obj: map(function, iter_obj)
            )
        )

    def bind_each(self, function: Callable[[_D], IO[_R]]) -> IOiter[_R]:
        transform = pipe(function, unsafe_perform_io)
        return IOiter(
            lambda: self.io_iter_obj.bind(
                lambda iter_obj: IO(iter(map(transform, iter_obj)))
            )
        )

    def consume(self) -> IO[None]:
        return self.io_iter_obj.map(
            lambda iter_obj: deque(iter_obj, maxlen=0)
        ).map(lambda _: None)


@dataclass(frozen=True)
class _PureIter(
    SupportsKind1["_PureIter[_D]", _D],
):
    _iter_obj: Patch[Callable[[], Iterable[_D]]]


class PureIter(_PureIter[_D]):
    def __init__(self, obj: _PureIter[_D]):
        super().__init__(obj._iter_obj)

    def __iter__(self) -> Iterator[_D]:
        return iter(self._iter_obj.unwrap())

    def map_each(self, function: Callable[[_D], _R]) -> PureIter[_R]:
        draft = _PureIter(Patch(lambda: map(function, self)))
        return PureIter(draft)

    def bind_io_each(self, function: Callable[[_D], IO[_R]]) -> IOiter[_R]:
        transform = pipe(function, unsafe_perform_io)

        def _internal() -> IO[Iterator[_R]]:
            items = iter(transform(item) for item in self)
            return IO(items)

        return IOiter(_internal)


@dataclass(frozen=True)
class PureIterFactory:
    @staticmethod
    def from_flist(items: FrozenList[_I]) -> PureIter[_I]:
        draft = _PureIter(Patch(lambda: items))
        return PureIter(draft)

    @staticmethod
    def map_range(function: Callable[[int], _R], items: range) -> PureIter[_R]:
        def gen() -> Iterable[_R]:
            return (function(i) for i in items)

        draft = _PureIter(Patch(lambda: iter(gen())))
        return PureIter(draft)

    @staticmethod
    def map_flist(
        function: Callable[[_I], _R], items: FrozenList[_I]
    ) -> PureIter[_R]:
        def gen() -> Iterable[_R]:
            return (function(i) for i in items)

        draft = _PureIter(Patch(lambda: iter(gen())))
        return PureIter(draft)

    @staticmethod
    def filter_range(
        function: Callable[[int], Optional[_R]], items: range
    ) -> PureIter[_R]:
        def filtered() -> Iterable[_R]:
            raw = (function(i) for i in items)
            return (i for i in raw if i is not None)

        draft = _PureIter(Patch(lambda: iter(filtered())))
        return PureIter(draft)
