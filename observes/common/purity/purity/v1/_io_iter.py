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

_D = TypeVar("_D")
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
