from dataclasses import (
    dataclass,
)
from purity.v1._io_iter import (
    IOiter,
)
from purity.v1._pure_iter import (
    PureIter,
)
from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Iterator,
    List,
    TypeVar,
)

_DataTVar = TypeVar("_DataTVar")


@dataclass(frozen=True)
class Flattener:
    @staticmethod
    def pure_iter_io(items: PureIter[IO[_DataTVar]]) -> IOiter[_DataTVar]:
        def _internal() -> IO[Iterator[_DataTVar]]:
            return IO(iter(map(unsafe_perform_io, items.iter_obj)))

        return IOiter(_internal)

    @staticmethod
    def list_io(items: List[IO[_DataTVar]]) -> IO[List[_DataTVar]]:
        return IO(list(map(unsafe_perform_io, items)))
