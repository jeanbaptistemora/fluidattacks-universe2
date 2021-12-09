from dataclasses import (
    dataclass,
)
from purity.v2.frozen import (
    FrozenList,
)
from returns.converters import (
    flatten,
)
from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    TypeVar,
)

_D = TypeVar("_D")


@dataclass(frozen=True)
class Flattener:
    @staticmethod
    def list_io(items: FrozenList[IO[_D]]) -> IO[FrozenList[_D]]:
        return IO(tuple(map(unsafe_perform_io, items)))

    @staticmethod
    def denest(items: IO[IO[_D]]) -> IO[_D]:
        # this wrapper improves type signature clarity
        return flatten(items)
