from __future__ import (
    annotations,
)

from collections import (
    deque,
)
from dataclasses import (
    dataclass,
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
    SupportsKind1["IOiter", _D],
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
class PureIter(
    SupportsKind1["PureIter[_D]", _D],
):
    _iter_obj: Patch[Callable[[], Iterator[_D]]]

    def __init__(self, iter_obj: Callable[[], Iterator[_D]]) -> None:
        object.__setattr__(self, "_iter_obj", Patch(iter_obj))

    @property
    def iter_obj(self) -> Iterator[_D]:
        return self._iter_obj.unwrap()

    def map_each(self, function: Callable[[_D], _R]) -> PureIter[_R]:
        return PureIter(lambda: map(function, self.iter_obj))

    def bind_io_each(self, function: Callable[[_D], IO[_R]]) -> IOiter[_R]:
        transform = pipe(function, unsafe_perform_io)

        def _internal() -> IO[Iterator[_R]]:
            items = iter(transform(item) for item in self.iter_obj)
            return IO(items)

        return IOiter(_internal)


@dataclass(frozen=True)
class PureIterFactory:
    @staticmethod
    def map_range(function: Callable[[int], _R], items: range) -> PureIter[_R]:
        def gen() -> Iterable[_R]:
            return (function(i) for i in items)

        return PureIter(lambda: iter(gen()))

    @staticmethod
    def map_list(
        function: Callable[[_I], _R], items: List[_I]
    ) -> PureIter[_R]:
        def gen() -> Iterable[_R]:
            return (function(i) for i in items)

        return PureIter(lambda: iter(gen()))

    @staticmethod
    def filter_range(
        function: Callable[[int], Optional[_R]], items: range
    ) -> PureIter[_R]:
        def filtered() -> Iterable[_R]:
            raw = (function(i) for i in items)
            return (i for i in raw if i is not None)

        return PureIter(lambda: iter(filtered()))
