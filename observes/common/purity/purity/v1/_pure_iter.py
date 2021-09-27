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
    Iterator,
    TypeVar,
)

_DataTVar = TypeVar("_DataTVar")
_ReturnTVar = TypeVar("_ReturnTVar")


@dataclass(frozen=True)
class IOiter(
    SupportsKind1["IOiter", _DataTVar],
):
    _io_iter_obj: Patch[Callable[[], IO[Iterator[_DataTVar]]]]

    def __init__(
        self, io_iter_obj: Callable[[], IO[Iterator[_DataTVar]]]
    ) -> None:
        object.__setattr__(self, "_io_iter_obj", Patch(io_iter_obj))

    @property
    def io_iter_obj(self) -> IO[Iterator[_DataTVar]]:
        return self._io_iter_obj.unwrap()

    def map_each(
        self, function: Callable[[_DataTVar], _ReturnTVar]
    ) -> IOiter[_ReturnTVar]:
        return IOiter(
            lambda: self.io_iter_obj.map(
                lambda iter_obj: map(function, iter_obj)
            )
        )

    def bind_each(
        self, function: Callable[[_DataTVar], IO[_ReturnTVar]]
    ) -> IOiter[_ReturnTVar]:
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
    SupportsKind1["PureIter", _DataTVar],
):
    _iter_obj: Patch[Callable[[], Iterator[_DataTVar]]]

    def __init__(self, iter_obj: Callable[[], Iterator[_DataTVar]]) -> None:
        object.__setattr__(self, "_iter_obj", Patch(iter_obj))

    @property
    def iter_obj(self) -> Iterator[_DataTVar]:
        return self._iter_obj.unwrap()

    def map_each(
        self, function: Callable[[_DataTVar], _ReturnTVar]
    ) -> PureIter[_ReturnTVar]:
        return PureIter(lambda: map(function, self.iter_obj))

    def bind_io_each(
        self, function: Callable[[_DataTVar], IO[_ReturnTVar]]
    ) -> IOiter[_ReturnTVar]:
        transform = pipe(function, unsafe_perform_io)

        def _internal() -> IO[Iterator[_ReturnTVar]]:
            items = iter(transform(item) for item in self.iter_obj)
            return IO(items)

        return IOiter(_internal)
